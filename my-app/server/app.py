
import constants
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from time import sleep
from datetime import datetime  
import concurrent.futures
# import main
import multiprocessing
from syringepump import SyringePump as Pump
# import datetime
import matplotlib.pyplot as plt
from switchValve import SwitchValve

from textFileReader import readTextFiles
app = Flask(__name__)
CORS(app)



temp_file=''
csv_files=[]
ports=[]
exp_name = []
fig_no=1
from second import start
import threading

@app.route('/setup', methods=['POST'])
def setup():
    data = request.json
    constants.reactorVol = data['reactorVol']
    constants.dv1 = data['dv1']
    constants.sta = data['sta']
    constants.nmrInterval = data['nmrInterval']
    return data


@app.route('/inputcsv', methods=['POST'])
def import_csv():
    req = request.json
    timesweep = req['timesweeps']
    filename=req['filename']

    global temp_file
    temp_file = filename
    
    
    data = {
        'start': [i['start'] for i in timesweep],
        'end': [i['end'] for i in timesweep],
        'volume': [constants.reactorVol for i in timesweep],
        'StartFR': [i['startFR'] for i in timesweep],
        'StopFR': [i['endFR'] for i in timesweep],
        'stabilisation time': [constants.sta for i in timesweep],
        'dead volume 1': [constants.dv1 for i in timesweep],
        'Dead Volume 2': [constants.dv2 for i in timesweep],
        'GPC Interval': [constants.gpcInterval for i in timesweep],
        'Dead Volume 3': [constants.dv3 for i in timesweep],
        # 'Dilution FR ml/min': [constants.dilutionFR for i in timesweep],
        'DeadVolume1(min)': [float(constants.dv1)/float(i['endFR']) for i in timesweep],
        'DeadVolume2(min)': [float(constants.dv2)/float(i['endFR']) for i in timesweep],
        'DeadVolume3(min)': [float(constants.dv3)/float(i['endFR']) for i in timesweep],
        'NMR interval': [constants.nmrInterval for i in timesweep],
        'mode': ['GPC and NMR' for i in timesweep],
    }
    df = pd.DataFrame(data)
    df.to_csv(os.getcwd()+'/inputs/'+filename, index=True)

    csv_files.append(filename)
    
    return jsonify(df.to_dict(orient='records'))


@app.route('/outputcsv')
def output_csv():
    dfs=[]
    for file in csv_files:
        df = {
            'scanNumber': [],
            'timesweep' : [],
            'status':[],
            'I0': [],
            'I1': [],
            'conversion': [],
            'tReaction': [],
            'tRes': []
        }


        input_csv = read_csv(os.getcwd()+'/inputs/'+file)
        start_list = input_csv['start']
        end_list = input_csv['end']
        nmr_interval = input_csv['NMR interval']
        sta = input_csv['stabilisation time']
        dv1 = input_csv['dead volume 1']
        fr_end = input_csv['StopFR']
        len_timesweep = [int(i*60/nmr_interval[0])+1 for i in end_list]
        len_no=[int((start_list[0]*sta[0]+dv1[0]/fr_end[0])*60/float(constants.nmrInterval))+1]
        for i in range(1, len(start_list)):
            len_no.append(int((dv1[i]/fr_end[i])*60/float(constants.nmrInterval))+1) 

        for i in range(len(len_timesweep)):
            for j in range(len_no[i]):
                df['status'].append('No')
            for j in range(len_timesweep[i]):
                df['status'].append('Timesweep')   
        for i in range(len(len_timesweep)):
            timesweep_rows = len_timesweep[i]+len_no[i]
            df['timesweep'] += [i+1 for _ in range(timesweep_rows)]
        interval = nmr_interval[0]
        counter = 0
        for i in df['status']:
            if i == 'Timesweep':
                df['tReaction'].append(counter*float(constants.nmrInterval))
                counter+=1
            else:
                counter=0
                df['tReaction'].append('')
        treaction_timesweep = []
        for i in range(len(df['tReaction'])):
            if df['tReaction'][i]!='':
                ts_no = int(df['timesweep'][i])-1

                df['tRes'].append(
                    round(start_list[ts_no] + 
                        (df['tReaction'][i]*(1-(start_list[ts_no]/end_list[ts_no])))/60, 4
                    )
                )

            else:
                df['tRes'].append('')

        threecols(df, file)
        print(len(df))

    print("PORTS ", ports)
    print("NAME ", exp_name)

    files=[]
    for file in csv_files:
        files.append(pd.read_csv(os.getcwd()+'/inputs/'+file))
        pumps=[Pump(ports[i], name=exp_name[i]) for i in range(len(ports))]
        
        # switchValves=SwitchValve('COM3') 
        
        processes=[]
        
        # for i in range(len(pumps)):
        #     processes.append(threading.Thread(target=start, args=(pumps[i], files[0], os.getcwd()+'/outputs/'+temp_file)))
        # for p in processes:
        #     p.start()
        # for p in processes:
        #     p.join()  


        for i in range(len(pumps)):
            pumps[i].start()

    return {'input': os.getcwd()+'/inputs/'+temp_file, 'output': os.getcwd()+'/outputs/'+temp_file}

def threecols(df, file):
    print('EXPERIMENT TYPE: ', constants.experimentType)
    start_time = datetime.now()
    for i in range(len(df['timesweep'])):
        sleep(0.1)
        df['scanNumber'].append(i)
    nmr_data = pd.read_csv('NMR_data.csv')
    for i in range(len(df['timesweep'])):
        df['I0'].append('')
        df['I1'].append('')
        df['conversion'].append('')
        
    df['I0'][0:len(df['timesweep'])] = nmr_data['I0'][0:len(df['timesweep'])]
    df['I1'][0:len(df['timesweep'])] = nmr_data['I1'][0:len(df['timesweep'])]
    for i in range(len(df['I0'])):
        try:
            df['conversion'][i]=1-(float(constants.conversion)*(float(df['I0'][i])/float(df['I1'][i])))
        except:
            pass

    
    exp_columns = readTextFiles()
    mn_list = exp_columns['Mn']
    mw_list = exp_columns['Mw']
    d_list = exp_columns['D']
    gpc_interval = constants.gpcInterval
    nmr_interval = constants.nmrInterval
    row_in_between = int((float(gpc_interval)/float(nmr_interval))*60)+1
    print('row_in_between', row_in_between)
    df_rows = len(df['timesweep'])

    mn_row=[]
    mw_row=[]
    d_row=[]

    counter=0
    num_rows_from_last_write = 0



    for i in range(len(df['timesweep'])):
        if df['status'][i] == 'No':
            mn_row.append('')
            mw_row.append('')
            d_row.append('')
        else:  # status = timesweep
            try:
                if num_rows_from_last_write >= row_in_between:
                    mn_row.append(mn_list[counter])
                    mw_row.append(mw_list[counter])
                    d_row.append(d_list[counter])
                    num_rows_from_last_write=0
                else:
                    mn_row.append('')
                    mw_row.append('')
                    d_row.append('')
            except:
                pass
            
        num_rows_from_last_write+=1
        
    if constants.experimentType=='NMR':
        output=pd.DataFrame(df)
        output.to_csv(os.getcwd()+'/outputs/'+file)
        end_time = datetime.now()

    else:

        no_injection = []
        counter=0
        for row in mn_row[0:len(df['timesweep'])]:
            if row: 
                counter+=1
                no_injection.append(counter)
            else:
                no_injection.append('')
        df['no_injection'] = no_injection
        df['Mn'] = mn_row[0:len(df['timesweep'])]
        df['Mw'] = mw_row[0:len(df['timesweep'])]
        df['D'] = d_row[0:len(df['timesweep'])]
        output=pd.DataFrame(df)
        output.to_csv(os.getcwd()+'/outputs/'+file)
        end_time = datetime.now()



def read_csv(filename):
    df = pd.read_csv(filename)
    return df

def write_column(column_name, filename, data):
    if data:
        df = pd.read_csv(filename)
        new_data = pd.Series(data)
        df[column_name] = new_data
        df.to_csv(filename, mode='a', header=False, index=True)

@app.route('/conversion')
def conversion():
    conversion = request.args.get('c')
    constants.conversion = conversion
    data ={'conversion': conversion}
    return jsonify(data)


@app.route('/dir')
def dir():
    import os

    # set the directory path
    directory = os.getcwd()+'/inputs'
    # print(directory)
    # get all the files in the directory
    files = os.listdir(directory)

    # print the names of all files
    for file in files:
        # print(file)
        pass
    return {'status': 200}



@app.route('/getcsvfiles')
def process():
    global csv_files
    global ports
    global exp_name
    
    return {

        'files' : csv_files,
        'ports': ports,
        'expNames': exp_name

    }


@app.route('/clear')
def clear():
    global csv_files
    global ports
    global exp_name
    
    csv_files=[]
    ports=[]
    exp_name=[]

    return {
        'status': 201
    }


@app.route('/handle-exp', methods=['POST'])
def handleExp():
    global ports
    global exp_name


    data = request.json
    ports.append(data['port']['selectedOption'])
    exp_name.append(data['expName']['text'])
    # print(ports, exp_name)
    return {
        'status': 200
    }

@app.route('/creategraph')
def create_graph():
    global csv_files
    for file in csv_files:
        # print(file)
        show_graph(file)
    return {
        'status': csv_files
    }

def show_graph(filename):
    global fig_no
    # Create a sample DataFrame
    current_datetime = str(datetime.now())
    current_datetime=current_datetime.split(' ')
    date= current_datetime[0]
    time=current_datetime[1]
    parent_dir = os.getcwd()+'\\graph'
    directory = filename+'@'+ date
    path=os.path.join(parent_dir, directory)
    os.makedirs(path, exist_ok=True)

    df = pd.read_csv(os.getcwd()+'/outputs/'+filename)
    
    fig1 = plt.figure(num=fig_no)
    plt.plot(df['scanNumber'], df['conversion'])  # Use the column values as the heights of the bars
    plt.xlabel('scan number')  # Set x-axis label
    plt.ylabel('conversion')  # Set y-axis label
    # plt.show() 
    plt.savefig(path + '/scan-conversion.jpg')
    fig_no+=1

    fig2 = plt.figure(num=fig_no)
    plt.plot(df['tRes'], df['conversion'])  # Use the column values as the heights of the bars
    plt.xlabel('residence time')  # Set x-axis label
    plt.ylabel('conversion')  # Set y-axis label
    # plt.show() 
    plt.savefig(path + '/tres-conversion.jpg')
    fig_no+=1

    fig3 = plt.figure(num=fig_no)
    plt.plot(df['scanNumber'], df['I0'], label='I0')  # Use the column values as the heights of the bars
    plt.plot(df['scanNumber'], df['I1'], label='I1')
    plt.xlabel('scan number')  # Set x-axis label
    plt.ylabel('Integral')  # Set y-axis label
    plt.legend()
    # plt.show() 
    plt.savefig(path + '/scan-integral.jpg')
    fig_no+=1


@app.route('/remove-exp', methods=['POST'])
def removeExp():
    global ports
    global exp_name 
    global csv_files
    data = request.json
    i = data['i']

    # print(ports)
    # print(exp_name)
    # print(csv_files)
    if len(ports)>0 and len(exp_name)>0 :
        ports.pop(i-1)
        exp_name.pop(i-1)
        csv_files.pop(i-1)

    return {
                'data':{
                    'ports':ports,
                    'expNames':exp_name, 
                    'files':csv_files
                }
            }


@app.route('/edit-exp', methods=['POST'])
def editExp():
    global ports
    global exp_name 
    global csv_files
    data = request.json
    newData = data['data']
    
    ports=[]
    exp_name=[]
    csv_files=[]
    # print(data)
    for i in newData:
        # print(i)
        ports.append(i['port'])
        exp_name.append(i['expName'])
        # csv_files.append(i['port'])
    return {
                'data':{
                    'ports':ports,
                    'expNames':exp_name, 
                    'files':csv_files
                }
            }

def findIdx(keyword, arr):
    for i in range(len(arr)):
        if arr[i] == keyword:
            return i 
    return None


from pump_params import calc_flow
@app.route('/get-flowrates')

def getFlowrates():
    start_flowrate= read_csv(os.getcwd()+'/inputs/'+csv_files[0])['StartFR'][0]
    end_flowrate= read_csv(os.getcwd()+'/inputs/'+csv_files[0])['StartFR'][0]
    params=calc_flow(float(start_flowrate))
    ports=params['pump_ports']
    names=params['pump_names']
    flowrates=params['flowrates']
    return {'ports': ports, 'names':names, 'flowrates': flowrates}
    

from pump_params import get_dfs, pump_info
@app.route('/outputCSV-params')
def outputCSVParams():
    
    
    dfs=[]

    df = {
        'scanNumber': [],
        'timesweep' : [],
        'status':[],
        'I0': [],
        'I1': [],
        'conversion': [],
        'tReaction': [],
        'tRes': []
    }

    for input_csv in get_dfs():
    # input_csv = read_csv(os.getcwd()+'/inputs/'+csv_files[0])
        
        start_list = input_csv['start']
        end_list = input_csv['end']
        nmr_interval = input_csv['NMR interval']
        sta = input_csv['stabilisation time']
        dv1 = input_csv['dead volume 1']
        fr_end = input_csv['StopFR']

        len_timesweep = [int(i*60/nmr_interval[0]) for i in end_list]
        len_no=[int((start_list[0]*sta[0]+dv1[0]/fr_end[0])*60/float(constants.nmrInterval))+1]
        # print('len_timesweep', len_timesweep)

        for i in range(1, len(start_list)):
            len_no.append(int((dv1[i]/fr_end[i])*60/float(constants.nmrInterval))+1) 
        for i in range(len(len_timesweep)):
            for j in range(len_no[i]):
                df['status'].append('No')
            for j in range(len_timesweep[i]):
                df['status'].append('Timesweep')   
        for i in range(len(len_timesweep)):
            timesweep_rows = len_timesweep[i]+len_no[i]
            df['timesweep'] += [i+1 for _ in range(timesweep_rows)]
        interval = nmr_interval[0]
        counter = 0
        for i in df['status']:
            if i == 'Timesweep':
                df['tReaction'].append(counter*float(constants.nmrInterval))
                counter+=1
            else:
                counter=0
                df['tReaction'].append('')
        treaction_timesweep = []
        # print('timesweep length', len(df['timesweep']))
        # print('len t reaction ' , len(df['tReaction']))
        for i in range(len(df['tReaction'])):
            if df['tReaction'][i]!='':
                # print('i ', i)
                try:
                    ts_no = int(df['timesweep'][i])-1
                    # print(start_list[ts_no])
                    # print(end_list[ts_no])
                    # print(df['tReaction'][0])
                    df['tRes'].append(
                        round(start_list[ts_no] + 
                            (df['tReaction'][i]*(1-(start_list[ts_no]/end_list[ts_no])))/60, 2
                        )
                    )
                except:
                    pass

            else:
                df['tRes'].append('')

        threecolsParams(df)

    # files=[]
    # for file in csv_files:
    #     files.append(pd.read_csv(os.getcwd()+'/inputs/'+file))

    # pumps=[Pump(ports[i], name=exp_name[i]) for i in range(len(ports))]
    pumps=[Pump(pump_info()['pump_ports'][i], name=pump_info()['pump_names'][i]) for i in range(len(pump_info()['pump_ports']))]
    processes=[]
    files = get_dfs()
    for i in range(len(pumps)):
        processes.append(threading.Thread(target=start, args=(pumps[i], files[0])))
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    return {'input': os.getcwd()+'/inputs/'+temp_file, 'output': os.getcwd()+'/outputs/'+temp_file}




def threecolsParams(df):
    start_time = datetime.now()
    for i in range(len(df['timesweep'])):
        sleep(0.1)
        df['scanNumber'].append(i)
    nmr_data = pd.read_csv('NMR_data.csv')
    for i in range(len(df['timesweep'])):
        df['I0'].append('')
        df['I1'].append('')
        df['conversion'].append('')
        
    df['I0'][0:len(df['timesweep'])] = nmr_data['I0'][0:len(df['timesweep'])]
    df['I1'][0:len(df['timesweep'])] = nmr_data['I1'][0:len(df['timesweep'])]
    for i in range(len(df['I0'])):
        try:
            df['conversion'][i]=float(constants.conversion)*(float(df['I0'][i])/float(df['I1'][i]))
        except:
            pass


    output=pd.DataFrame(df)
    output.to_csv(os.getcwd()+'/outputs/finalTest.csv')
    end_time = datetime.now()



@app.route('/uploadcsv', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(file.filename)
    constants.fileParams = file.filename
    return {'message': file.filename}

@app.route('/setexperiment', methods=['POST'])
def setExperiment():
    data = request.json
    constants.experimentType = data['experimentType']
    return {'experimentType': constants.experimentType}
