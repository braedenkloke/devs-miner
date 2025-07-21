from devsminer import read_file, discover_devs

if __name__ == "__main__":
    event_log = read_file.read_csv("tests/input_data/event_log_1.csv")
    print(event_log)
