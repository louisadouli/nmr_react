import pandas as pd
from syringepump import SyringePump as Pump
import constants
df = pd.read_csv('pump_params.csv')
n = len(df)
C_N = float(df['desired_concentration'][0])
C = df['concentration_stock_solution']
EQ = df['equivalent']
PUMP_PORTS = list(df['pump_port'])
PUMP_NAMES = list(df['pump_name'])

def pump_info():
   return {'pump_ports': PUMP_PORTS, 'pump_names': PUMP_NAMES, 'EQ': EQ, 'C':C, 'C_N':C_N}


def calc_flow(flowrate):
    flowrates=[]
    for i in range(len(df)-1):
      flowrates.append((flowrate*C_N)/(C[i]*(EQ[0]/EQ[i])))
    flowrates.append(flowrate - sum(flowrates))
    # return {'flowrates':flowrates}
    return flowrates

def get_dfs():
  input_df = pd.read_csv('aaaa.csv')
  dfs=[input_df.copy() for i in range(n)]
  for index, row in input_df.iterrows():
      start_flow = calc_flow(float(row['StartFR']))
      stop_flow = calc_flow(float(row['StopFR']))
      for i in range(len(dfs)):
        dfs[i]['StartFR'].iloc[index] = start_flow[i] 
        dfs[i]['StopFR'].iloc[index] = stop_flow[i]
  return dfs

# print(dfs)
dfs = get_dfs()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
  for i in range(len(dfs)):
    print(dfs[i])
    

    


# # print(calc_flow(2.3, 3.6))
# inputcsv = pd.read_csv('aaaa.csv')
# print(len(inputcsv))
# # data = calc_flow(2.3, 3.6)
# # len_fr = len(data)

# inputcsv.at[0, 'volume']='1.0'
# print(inputcsv['volumeb '])


