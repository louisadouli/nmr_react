import pandas as pd
from syringepump import SyringePump as Pump
import time
from time import sleep
from datetime import datetime
import concurrent.futures


duration = []
fr = []
times = []
df = pd.read_csv('input.csv')

def calc_time():
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


def calc_fr():
    # fr=[]
    for index, row in df.iterrows():
        start_fr = row['StartFR']
        stop_fr = row['StopFR']
        fr.append([start_fr, stop_fr])

def start():
    pump = Pump('COM3', name='my_pump')
    calc_time()
    calc_fr()
    start_time = times[0][0]
    print('start_time', start_time)

    start_time = time.time()

    started = False
    changed_end_flow_rate = False

    i = 0
    pump.changeFlowrate(fr[i][0])
    pump.start()
    changed_fr = False
    spent_time = 0
    print(len(times))
    while i < len(times):
        # print(this.name)
        current_time = time.time()
        if (time.time()-start_time)/60 >= 1.3 and i == 0 and not changed_fr:
            pump.changeFlowrate(fr[i][1])
            changed_fr = True
            spent_time += 1.3
            start_time = time.time()
            print("first if loop")

        if (time.time()-start_time)/60 >= times[i][2]+times[i][1] and changed_fr:
            i += 1
            if i != len(times):
                pump.changeFlowrate(fr[i][1])
                print(fr[i][1])
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

