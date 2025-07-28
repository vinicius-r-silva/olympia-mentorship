def print_medatata_details(trace_id, metadata, last_revision):
    print(trace_id)
    print("")
    if "description" in metadata and metadata['description']:
        print(metadata['description'])

    print(f"Workload: {metadata['workload']['filename']}")
    print(f"Author: {metadata['author']['name']}")
    print(f"Trace Timestamp: {metadata['stf']['timestamp']}")
    print(f"Revision: {last_revision}")
    
    if "trace_interval" in metadata['stf'] and metadata['stf']['trace_interval']:
        print(f"Trace Interval:")
        print(f"  Instruction PC: {metadata['stf']['trace_interval']['instruction_pc']}")
        print(f"  PC Count: {metadata['stf']['trace_interval']['pc_count']}")
        print(f"  Interval Length: {metadata['stf']['trace_interval']['interval_lenght']}")

    print("\n---------------------------------")