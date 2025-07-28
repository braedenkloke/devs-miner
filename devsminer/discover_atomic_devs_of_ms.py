
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
        ext_trans   external transition function represented as a set of ordered pairs.
                    mapping ext_trans(s,e,x) -> s
        int_trans   internal transition function represented as a set of ordered pairs.
                    mapping int_trans(s) -> s
        output      output function represented as a set of ordered pairs mapping
                    output(s) -> y

    >>> execute(event_log, state_log)
    X: {'enter'}
    Y: {'end'}
    S: {'idle', 'busy'}
    ta: {('busy', 5.0), ('idle', inf)}
    ext_trans: {(('idle', 'enter'), 'busy')}
    int_trans: {('busy', 'idle')}
    output: {('busy', 'end')}
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

    # Identify system resources
    resources = set()
    for e in log:
        resources.add(e[L_state_i][SL_resource_i])

    # Extract inputs
    inputs = set()
    for i in range(1, len(log)):     
        event = log[i][L_event_i]
        current_state = log[i][L_state_i][SL_state_i]
        prev_state = log[i - 1][L_state_i][SL_state_i]
        if event[EL_resource_i] not in resources and current_state != prev_state:
            inputs.add(event[EL_activity_i])

    # Extract outputs
    outputs = set()
    for e in log:     
        event = e[L_event_i]
        if event != None and event[EL_resource_i] in resources:
            outputs.add(event[EL_activity_i])

    # Extract states
    states = set()
    for e in log:
        states.add(e[L_state_i][SL_state_i])

    # Extract external transition function
    ext_trans = set()
    for i in range(1, len(log)):
        event_activity = log[i][L_event_i][EL_activity_i]
        current_state = log[i][L_state_i][SL_state_i]
        prev_state = log[i - 1][L_state_i][SL_state_i]
        if event_activity in inputs:
            ext_trans.add( ((prev_state, event_activity), current_state,) )

    # Extract internal transition function
    int_trans = set()
    for i in range(1, len(log)):
        event = log[i][L_event_i]
        current_state = log[i][L_state_i][SL_state_i]
        prev_state = log[i - 1][L_state_i][SL_state_i]
        if current_state != prev_state:
            if event == None or event[EL_activity_i] not in inputs:
                int_trans.add( (prev_state, current_state,) )

    # Extract output function
    output_func = set()
    for i in range(len(log)):
        event = log[i][L_event_i]
        prev_state = log[i - 1][L_state_i][SL_state_i]
        if event != None and event[EL_activity_i] in outputs:
            output_func.add( (prev_state, event[EL_activity_i],) )

    # Extract time advance function
    ta = set()
    for e in log:
        state = e[L_state_i][SL_state_i]
        duration = e[L_duration_i]
        ta.add( (state, duration,) )
        
    return inputs, outputs, states, ta, ext_trans, int_trans, output_func

def _join_logs_on_timestamp(event_log, state_log, event_log_timestamp_i=0, state_log_timestamp_i=0):
    # Assumptions:
    # * logs are not empty
    # * logs are sorted by timestamp in ascending order
    # * no concurrency, i.e., events that happen at the same time happen in the given order
    joined_log = []
    event_log_i = 0
    state_log_i = 0
    
    # Add initial state to log
    joined_log.append( [ state_log[state_log_i][state_log_timestamp_i], None, state_log[state_log_i] ] )
    state_log_i += 1

    while event_log_i < len(event_log) or state_log_i < len(state_log):
        # Case: joined all log entries from event_log
        if event_log_i >= len(event_log):
            joined_log.append( [ state_log[state_log_i][state_log_timestamp_i], None, state_log[state_log_i] ] )
            state_log_i += 1
        # Case: joined all log entries from state_log
        elif state_log_i >= len(state_log):
            joined_log.append( [ event_log[event_log_i][event_log_timestamp_i], event_log[event_log_i], None ] )
            event_log_i += 1
        # Case: timestamps match
        elif event_log[event_log_i][event_log_timestamp_i] == state_log[state_log_i][state_log_timestamp_i]:
            joined_log.append( [ event_log[event_log_i][event_log_timestamp_i], event_log[event_log_i], state_log[state_log_i] ] )
            event_log_i += 1
            state_log_i += 1
        # Case: event_log timestamp is less than state_log timestamp
        elif event_log[event_log_i][event_log_timestamp_i] < state_log[state_log_i][state_log_timestamp_i]:
            joined_log.append( [ event_log[event_log_i][event_log_timestamp_i], event_log[event_log_i], None ] )
            event_log_i += 1
        # Case: event_log timestamp is greater than state_log timestamp
        else:
            joined_log.append( [ state_log[state_log_i][state_log_timestamp_i], None, state_log[state_log_i] ] )
            state_log_i += 1

    return joined_log
