import pandas as pd
from syringepump import SyringePump as Pump
import time
from time import sleep
from datetime import datetime
import concurrent.futures
import threading
import os 
import constants
from switchValve import SwitchValve
duration = []
fr = []
times = []
# df = pd.read_csv('input.csv')

def calc_time(df):
    # time=[]
    for index, row in df.iterrows():
        start_min = row['start']
        stop_min = row['end']
        dead_volume1 = row['dead volume 1']
        dead_volume2 = row['Dead Volume 2']
        dead_volume3 = row['Dead Volume 3']
        sta_time = row['stabilisation time']
        res = stop_min-start_min+dead_volume1+dead_volume2+dead_volume3+sta_time
        duration.append(res)
        times.append([start_min, stop_min, dead_volume1,
                     dead_volume2, dead_volume3, sta_time])


def calc_fr(df):
    # fr=[]
    for index, row in df.iterrows():
        start_fr = row['StartFR']
        stop_fr = row['StopFR']
        fr.append([start_fr, stop_fr])
    return fr
def start(pump, input_df, output_df):
    global fr
    # pump = Pump('COM6', name='my_pump')
    calc_time(input_df)
    fr= calc_fr(input_df)
    # print('FR', fr)
    start_time = times[0][0]
    start_time = time.time()
    started = False
    changed_end_flow_rate = False
    i = 0
    pump.changeFlowrate(fr[i][0])
    pump.start()
    changed_fr = False
    spent_time = 0
    reset_position=False


    current_time = time.time()
    live_time = time.time()
    counter =0
    if constants.experimentType!='NMR':
        scanNumbers=readScanNumbers(output_df, fr)
        print(scanNumbers)

    while i < len(times):
        # print(counter)
        if constants.experimentType!='NMR':
            if counter < len(scanNumbers):
                if(time.time() - live_time >= scanNumbers[counter]):
                    print(time.time() - live_time)
                    print('positionA')
                    # sv.toPositionB()
                    sleep(1)
                    # sv.toPositionA()
                    print('positionB')
                    current_time=time.time()
                    counter+=1


        # print(this.name)
        if (time.time()-start_time)/60 >= float(constants.sta)*times[i][0] and i == 0 and not changed_fr:
            pump.changeFlowrate(fr[i][1])
            changed_fr = True
            # spent_time += 
            start_time = time.time()
            print("first if loop")

        if (time.time()-start_time)/60 >=(float(constants.dv1)/float(fr[i][1]))+times[i][1] and changed_fr:
            i += 1
            if i != len(times):
                pump.changeFlowrate(fr[i][1])
                # print(fr[i][1])
            start_time = time.time()
            print("i: ", i)


    pump.stop()








def threecols(df):
    start_time = datetime.now()
    for i in range(len(df['timesweep'])):
        sleep(0.01)
        df['scanNumber'].append(i)
    nmr_data = pd.read_csv('NMR_data.csv')
    for i in range(len(df['timesweep'])):
        df['I0'].append('')
        df['I1'].append('')
        df['conversion'].append('')
        
    df['I0'][0:len(nmr_data['I0'])] = nmr_data['I0']
    df['I1'][0:len(nmr_data['I1'])] = nmr_data['I1']
    for i in range(len(df['I0'])):
        try:
            df['conversion'][i]=1-(float(df['I0'][i])/float(df['I1'][i]))
        except:
            # df['conversion'][i]=''
            pass
    output=pd.DataFrame(df)
    output.to_csv('output.csv')
    end_time = datetime.now()
import math
def readScanNumbers(path, fr):
    if constants.experimentType != 'NMR': 
        scanNumbers = []
        result=[]
        df = pd.read_csv(path)
        for i in range(1, len(df['timesweep'])):

                if df.iloc[i, 3] != 'No' and not math.isnan(df.iloc[i, 10]):
                    # print('10: ', (df.iloc[i, 10]))
                    scanNumbers.append([ int(df.iloc[i, 1]), int(df.iloc[i, 2]) ])

        print(len(scanNumbers))
        for i in range(len(scanNumbers)):
            timesweep = scanNumbers[i][1]

            result.append(
                            
                            (float(scanNumbers[i][0])*float(constants.nmrInterval))
                            +(float(constants.dv2)/float(fr[timesweep-1][1]))
                            +(float(constants.dv3)/(float(constants.dilutionFR)+float(fr[timesweep-1][1])))
                        )


        return result
    return 

# print(readScanNumbers(os.getcwd()+'/outputs/arshia.csv'))


# pump1 = Pump('COM7', name='my_pump')
# pump2 = Pump('COM6', name='my_pump(1)')

# df1 = pd.read_csv(os.getcwd()+'/inputs/'+'aaa.csv')
# df2 = pd.read_csv(os.getcwd()+'/inputs/'+'hi.csv')
# dfs=[df1, df2]

# processes=[]

# for i in range(len(pumps)):
#     processes.append(threading.Thread(target=start, args=(pumps[i], dfs[i])))
# for p in processes:
#     p.start()
# for p in processes:
#     p.join()




# p1 = threading.Thread( target=start, args=(pump1, dfs[0]))
# p2 = threading.Thread(target=start, args=(pump2, dfs[1]))

# p1.start()
# p2.start()

# p1.join()
# p2.join()

