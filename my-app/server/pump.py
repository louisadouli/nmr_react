import threading
import pandas as pd
from syringepump import SyringePump
import time
from time import sleep
from datetime import datetime
import concurrent.futures
import os
import constants

class Pump:
    def __init__(self, id, name, filename):
        self.duration = []
        self.fr = []
        self.times = []
        self.df = pd.read_csv(filename)
        self.id = id
        self.name = name
        self.filename=filename
    def calc_time(self):
        # time=[]
        for index, row in self.df.iterrows():
            start_min = row['start']
            stop_min = row['end']
            dead_volume1 = row['dead volume 1']
            dead_volume2 = row['Dead Volume 2']
            dead_volume3 = row['Dead Volume 3']
            sta_time = row['stabilisation time']
            res = stop_min-start_min+dead_volume1+dead_volume2+dead_volume3+sta_time
            self.duration.append(res)
            self.times.append([start_min, stop_min, dead_volume1,
                        dead_volume2, dead_volume3, sta_time])


    def calc_fr(self):
        # fr=[]
        for index, row in self.df.iterrows():
            start_fr = row['StartFR']
            stop_fr = row['StopFR']
            self.fr.append([start_fr, stop_fr])

    def start(self):
        pump = SyringePump(self.id, name=self.name)
        self.calc_time()
        self.calc_fr()
        start_time = self.times[0][0]
        print('start_time', start_time)
        
        start_time = time.time()

        started = False
        changed_end_flow_rate = False

        i = 0
        pump.changeFlowrate(self.fr[i][0])
        pump.start()
        changed_fr = False
        spent_time = 0
        print(len(self.times))
        while i < len(self.times):
            print(float(self.times[i][0]))
            # print(self.name)
            current_time = time.time()
            if (time.time()-start_time)/60 >= float(constants.sta)*float(self.times[i][0]) and i == 0 and not changed_fr:
                pump.changeFlowrate(self.fr[i][1])
                changed_fr = True
                spent_time += float(constants.sta)
                start_time = time.time()
                print("first if loop")

            if (time.time()-start_time)/60 >= float(self.times[i][2])+float(self.times[i][1]) and changed_fr:
                i += 1
                if i != len(self.times):
                    pump.changeFlowrate(self.fr[i][1])
                    print(self.fr[i][1])
                start_time = time.time()
                print("i: ", i)

        pump.stop()






        

    # def threecols(self, df):
    #     start_time = datetime.now()
    #     for i in range(len(df['timesweep'])):
    #         sleep(0.01)
    #         df['scanNumber'].append(i)
    #     nmr_data = pd.read_csv('NMR_data.csv')
    #     for i in range(len(df['timesweep'])):
    #         df['I0'].append('')
    #         df['I1'].append('')
    #         df['conversion'].append('')
            
    #     df['I0'][0:len(nmr_data['I0'])] = nmr_data['I0']
    #     df['I1'][0:len(nmr_data['I1'])] = nmr_data['I1']
    #     for i in range(len(df['I0'])):
    #         try:
    #             df['conversion'][i]=1-(float(df['I0'][i])/float(df['I1'][i]))
    #         except:
    #             # df['conversion'][i]=''
    #             pass
    #     output=pd.DataFrame(df)
    #     output.to_csv(os.getcwd()+'/outputs/'+self.)
        
    #     end_time = datetime.now()








# pump1 = Pump('COM6', 'p1', '../server/inputs/input1.csv')
# pump2 = Pump('COM7', 'p2', '../server/inputs/input2.csv')

# import concurrent.futures
# import time
# # stop_event = threading.Event()
# # a = pump1.start
# # b = pump2.start
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     future1 = executor.submit(pump1.start)
#     future2 = executor.submit(pump2.start)
# try:
#     while True:
#         time.sleep(0.1)

# except KeyboardInterrupt:
#     # Cancel the tasks
#     pump1.stop()
#     pump2.stop()
#     # Shutdown the executor
#     executor.shutdown(wait=False)