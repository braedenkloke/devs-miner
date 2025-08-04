import csv

from devsminer import discover_atomic_devs_of_ms

if __name__ == '__main__':
    event_log = []
    state_log = []
    
    with open('tests/input_data/manufacturing_sys_event_log.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            event_log.append(row)

    with open('tests/input_data/manufacturing_sys_state_log.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            state_log.append(row)

    X, Y, S, ta, ext_trans, int_trans, output = discover_atomic_devs_of_ms.execute(event_log, state_log)

    print('X: ' + str(X))
    print('Y: ' + str(Y))
    print('S: ' + str(S))
    print('ta: ' + str(ta))
    print('ext_trans: ' + str(ext_trans))
    print('int_trans: ' + str(int_trans))
    print('output: ' + str(output))
