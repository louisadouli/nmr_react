import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
from syringepump import SyringePump as Pump
# from pump_params import calc_flow
from switchValve import SwitchValve


# data = calc_flow(99)
# df = pd.read_csv('aaaa.csv')
# print(data)
for i in range(32):
    try:
        SwitchValve(port='COM3')
    except:
        pass