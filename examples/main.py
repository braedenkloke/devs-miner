from devsminer import read_file, discover_atomic_devs_of_ms

if __name__ == "__main__":
    event_log = read_file.read_csv("tests/input_data/event_log_1.csv")
    state_log = read_file.read_csv("tests/input_data/state_log_1.csv")
    m = discover_atomic_devs_of_ms.execute(event_log, state_log)
    print(m)
