import os
import yaml
from .base import CommandHandler
from utils.metadata_parser import MetadataParser
from utils.database_explorer import DatabaseExplorer

class UploadHandler(CommandHandler):
    def __init__(self):
        self.explorer = DatabaseExplorer()

    def run(self, args):
        workload_path = args.workload
        trace_path = args.trace if args.trace else f"{workload_path}.zstf"
        metadata_path = f"{trace_path}.metadata.yaml" 

        metadata = MetadataParser.read_metadata(metadata_path)
        trace_id = self.get_trace_id(metadata)

        if self.explorer.exists(trace_id):
            print(f"Trace ID {trace_id} already exist in the database. Do you to create a new revision? (yes/no)")
            response = input().strip().lower()
            if response != 'yes' and response != 'y':
                print("Upload cancelled.")
                return
            
        self.explorer.upload(workload_path, trace_path, metadata_path, trace_id)
        print(f"Uploaded trace with ID: {trace_id}")
    
    def get_trace_id(self, metadata):
        company_name = metadata.get('author').get('company')
        workload_name = metadata.get('workload').get('filename')
        trace_id = f"{company_name}_{workload_name}"
        
        trace_interval = metadata.get('stf').get('trace_interval')
        if(trace_interval):
            trace_id += f"_partial_trace_{trace_interval['instruction_pc']}_{trace_interval['pc_count']}_{trace_interval['interval_lenght']}"

        return trace_id
    
    

