import math
import pandas as pd

event_log_entry_key = 'event log entry'
state_log_entry_key = 'state log entry'
duration_key = 'duration'

def discover_atomic_devs_of_manufacturing_system(
    event_log: pd.DataFrame, 
    state_log: pd.DataFrame,
    timestamp_key: str = 'timestamp',
    state_key: str = 'state',
    resource_key: str = 'resource',
    activity_key: str = 'event'
) -> tuple:
    """
    Discovers an atomic DEVS model of a manufacturing system.

    :param event_log: Event log with headers; timestamp, order_id, resource, and event.
    :param state_log: State log with headers; timestamp, resource, and state.
    :param timestamp_key: Attribute to be used for timestamp.
    :param state_key: Attribute to be used for state.
    :param resource_key: Attribute to be used for resource.
    :param activity_key: Attribute to be used for activity.
    :return: A tuple representation of an atomic DEVS model. 
    
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
    """
    log = _join_logs_on_timestamp(event_log, state_log, timestamp_key)

    # Estimate durations
    for i in range(len(log) - 1):
        log.at[i, duration_key] = log.at[i + 1, timestamp_key] - log.at[i, timestamp_key] 
    passive_state = log.at[len(log) - 1, state_log_entry_key][state_key]
    for i in range(len(log)):
        if log.at[i, state_log_entry_key][state_key] == passive_state:
            log.at[i, duration_key] = math.inf
    
    # Extract inputs, outputs and states
    inputs = set()
    outputs = set()
    states = set()
    resources = set()
    for i in range(len(state_log)):
        states.add(log.at[i, state_log_entry_key][state_key])
        resources.add(state_log.at[i, resource_key])
    for i in range(1, len(log)):     
        event = log.at[i, event_log_entry_key]
        current_state = log.at[i, state_log_entry_key][state_key]
        prev_state = log.at[i - 1, state_log_entry_key][state_key]
        if event[resource_key] not in resources and current_state != prev_state:
            inputs.add(event[activity_key])
        if event[resource_key] in resources:
            outputs.add(event[activity_key])
    
    # Extract external transition, internal transition, output and time advance functions
    ext_trans = set()
    int_trans = set()
    output_func = set()
    ta = set()
    for i in range(1, len(log)):
        event_activity = log.at[i, event_log_entry_key][activity_key]
        current_state = log.at[i, state_log_entry_key][state_key]
        prev_state = log.at[i - 1, state_log_entry_key][state_key]
        if event_activity in inputs:
            ext_trans.add(((prev_state, event_activity), current_state,))
        if event_activity not in inputs and current_state != prev_state:
            int_trans.add((prev_state, current_state,))
        if event_activity in outputs:
            output_func.add((prev_state, event_activity,))
        ta.add((current_state, float(log.at[i, duration_key]),))
        
    return inputs, outputs, states, ta, ext_trans, int_trans, output_func

def _join_logs_on_timestamp(event_log, state_log, timestamp_key):
    joined_log = pd.DataFrame(columns=[timestamp_key, event_log_entry_key, state_log_entry_key, duration_key])

    joined_log_i = 0
    event_log_i = 0
    state_log_i = 0

    # Add initial state to log
    joined_log.loc[joined_log_i] = [0, event_log.loc[event_log_i], state_log.loc[state_log_i], None]
    joined_log_i += 1
    state_log_i += 1
    
    while event_log_i < len(event_log) or state_log_i < len(state_log):
        # Case: joined all log entries from event_log
        if event_log_i >= len(event_log):
            joined_log.loc[joined_log_i] = [state_log[state_log_i][timestamp_key], None, state_log.loc[state_log_i], None]
            state_log_i += 1
        # Case: joined all log entries from state_log
        elif state_log_i >= len(state_log):
            joined_log.loc[joined_log_i] = [event_log[event_log_i][timestamp_key], event_log.loc[event_log_i], None, None]
            event_log_i += 1
        # Case: timestamps match
        elif event_log.loc[event_log_i][timestamp_key] == state_log.loc[state_log_i][timestamp_key]:
            joined_log.loc[joined_log_i] = [event_log.loc[event_log_i][timestamp_key], event_log.loc[event_log_i], 
                                            state_log.loc[state_log_i], None]
            event_log_i += 1
            state_log_i += 1
        # Case: event_log timestamp is less than state_log timestamp
        elif event_log.loc[event_log_i][timestamp_key] < state_log.loc[state_log_i][timestamp_key]:
            joined_log.loc[joined_log_i] = [event_log.loc[event_log_i][timestamp_key], event_log.loc[event_log_i], None, None]
            event_log_i += 1
        # Case: event_log timestamp is greater than state_log timestamp
        else:
            joined_log.loc[joined_log_i] = [state_log.loc[state_log_i][timestamp_key], None, state_log.loc[state_log_i], None]
            state_log_i += 1
        joined_log_i += 1

    return joined_log
