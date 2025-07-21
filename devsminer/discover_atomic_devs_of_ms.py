"""Process mining discovery algorithm for an atomic DEVS model of a manufacturing system."""

from math import inf

def execute(event_log, state_log):
    """Returns an atomic DEVS model from a given event log and state log for a manufacturing system.

    Event log:

        [ [ timestamp, order identifier, resource, activity ], ... ]

    State log:

        [ [ timestamp, resource, state ], ... ]

    Return:
    
        ( X, Y, S, ta, ext_trans, int_trans, output )

        X           set of inputs
        Y           set of outputs
        S           set of states
        ta          time advance function represented as a set of pairs mapping 
                    ta(s) -> real number
        ext_trans   external transition function represented as a set of pairs
                    mapping ext_trans(s,e,x) -> s
        int_trans   internal transition function represented as a set of pairs
                    mapping int_trans(s) -> s
        output      output function represented as a set of tuples mapping
                    output(s) -> y

    """
    # Log indices
    EL_timestamp_i = 0
    EL_order_id_i = 1
    EL_resource_i = 2
    EL_activity_i = 3
    SL_timestamp_i = 0
    SL_resource_i = 1
    SL_state_i = 2
    L_timestamp_i = 0
    L_event_i = 1
    L_state_i = 2
    L_duration_i = 3

    # Clean data
    for e in event_log:
        e[EL_timestamp_i] = float(e[EL_timestamp_i])
    for e in state_log:
        e[SL_timestamp_i] = float(e[SL_timestamp_i])

    # Check assumption that logs are sorted by timestamp in ascending order
    prev_timestamp = 0
    for e in event_log:
        assert e[EL_timestamp_i] >= prev_timestamp, "Event log should be sorted by timestamp in ascending order."
        prev_timestamp = e[EL_timestamp_i]

    prev_timestamp = 0
    for e in state_log:
        assert e[SL_timestamp_i] >= prev_timestamp, "State log should be sorted by timestamp in ascending order."
        prev_timestamp = e[SL_timestamp_i]

    log = _join_logs_on_timestamp(event_log, state_log)

    # Estimate durations
    n = len(log)
    for i in range(n - 1):
        log[i].append(log[i + 1][L_timestamp_i] - log[i][L_timestamp_i])
    log[n - 1].append(inf)

    # Estimate passive states
    passive_state = log[len(log)-1][L_state_i][SL_state_i]
    for i in range(len(log)):
        if log[i][L_state_i][SL_state_i] == passive_state:
            log[i][L_duration_i] = inf

    return log

def _join_logs_on_timestamp(log1, log2, log1_t_index=0, log2_t_index=0):
    # Assumptions:
    # * logs are not empty
    # * logs are sorted by timestamp in ascending order
    # * timestamps within a log are unique, i.e., no concurrent events in a given log
    joined_log = []
    log1_i = 0
    log2_i = 0

    while log1_i < len(log1) or log2_i < len(log2):
        # Case: joined all log entries from log1
        if log1_i >= len(log1):
            joined_log.append( [ log2[log2_i][log2_t_index], None, log2[log2_i] ] )
            log2_i += 1
        # Case: joined all log entries from log2
        elif log2_i >= len(log2):
            joined_log.append( [ log1[log1_i][log1_t_index], log1[log1_i], None ] )
            log1_i += 1
        # Case: timestamps match
        elif log1[log1_i][log1_t_index] == log2[log2_i][log2_t_index]:
            joined_log.append( [ log1[log1_i][log1_t_index], log1[log1_i], log2[log2_i] ] )
            log1_i += 1
            log2_i += 1
        # Case: log1 timestamp is less than log2 timestamp
        elif log1[log1_i][log1_t_index] < log2[log2_i][log2_t_index]:
            joined_log.append( [ log1[log1_i][log1_t_index], log1[log1_i], None ] )
            log1_i += 1
        # Case: log1 timestamp is greater than log2 timestamp
        else:
            joined_log.append( [ log2[log2_i][log2_t_index], None, log2[log2_i] ] )
            log2_i += 1

    return joined_log
