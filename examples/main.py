from devsminer import io, discover_atomic_devs_of_ms

if __name__ == "__main__":
    event_log = io.read_csv("tests/input_data/event_log_1.csv")
    state_log = io.read_csv("tests/input_data/state_log_1.csv")
    X, Y, S, ta, ext_trans, int_trans, output = discover_atomic_devs_of_ms.execute(event_log, state_log)
    print("X: " + str(X))
    print("Y: " + str(Y))
    print("S: " + str(S))
    print("ta: " + str(ta))
    print("ext_trans: " + str(ext_trans))
    print("int_trans: " + str(int_trans))
    print("output: " + str(output))
