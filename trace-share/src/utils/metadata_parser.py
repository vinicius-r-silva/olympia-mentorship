import os
import yaml
from .fields_validator import FieldsValidator

class MetadataParser:
    @staticmethod
    def read_metadata(metadata_path):
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        with open(metadata_path, 'r') as file:
          data = yaml.safe_load(file)
          
        MetadataParser.validate_metadata(data)
        return data
    
    @staticmethod
    def validate_metadata(metadata):
        if not metadata:
            raise ValueError("Metadata is empty or invalid.")
        
        required_keys = {'author': ["name", "company", "email"], 
                         'workload': ['filename', 'SHA256', 'execution_command', 'elf_sections'],
                         'stf': ['timestamp', 'stf_trace_info']}
        dependent_keys = {
            'stf': {'trace_interval': ['instruction_pc', 'pc_count', 'interval_lenght']}
        }
        
        FieldsValidator.validate(metadata, required_keys, dependent_keys)