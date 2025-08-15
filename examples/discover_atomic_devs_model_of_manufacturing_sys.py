import csv
import pm4py
import pandas as pd

import devsminer.discover as dm

def extract_petri_net(event_log):
    event_log['timestamp'] = pd.to_datetime(event_log['timestamp'], unit='s')
    net, im, fm = pm4py.discover_petri_net_alpha(event_log, activity_key='event',
                                                 case_id_key='order_id', timestamp_key='timestamp')
    pm4py.view_petri_net(net, im, fm)
    print(net)

def main():
    event_log = pd.read_csv('tests/input_data/manufacturing_sys_event_log.csv', sep=',', converters={"order_id":str}) 
    state_log = pd.read_csv('tests/input_data/manufacturing_sys_state_log.csv', sep=',') 

    #extract_petri_net(event_log)
    
    X, Y, S, ta, ext_trans, int_trans, output = dm.discover_atomic_devs_of_manufacturing_system(event_log, state_log)

    print('X: ' + str(X))
    print('Y: ' + str(Y))
    print('S: ' + str(S))
    print('ta: ' + str(ta))
    print('ext_trans: ' + str(ext_trans))
    print('int_trans: ' + str(int_trans))
    print('output: ' + str(output))
    
if __name__ == '__main__':
    main() 
