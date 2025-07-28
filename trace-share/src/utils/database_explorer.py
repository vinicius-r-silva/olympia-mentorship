
import os
import shutil
from utils.metadata_parser import MetadataParser

class DatabaseExplorer:
    def __init__(self):
        self.storage_path = "./storage"

    def get_last_revision(self, trace_id):
        trace_path = f"{self.storage_path}/{trace_id}"
        if not os.path.exists(trace_path):
            raise FileNotFoundError(f"Trace path does not exist: {trace_path}")

        files = os.listdir(trace_path)
        metadata_files = [f for f in files if f.startswith(trace_id) and f.endswith('.metadata.yaml')]

        if not metadata_files:
            raise FileNotFoundError(f"No trace files found for trace ID: {trace_id}")

        revisions = [int(filename.split('_rev')[-1].split('.')[0]) for filename in metadata_files]
        latest_revision = max(revisions)
        return latest_revision

    
    def exists(self, trace_id):
        trace_path = f"{self.storage_path}/{trace_id}"
        return os.path.exists(trace_path)


    def upload(self, workload_path, trace_path, metadata_path, trace_id):
        trace_dir = f"{self.storage_path}/{trace_id}"
        
        last_revision = None
        if not self.exists(trace_id):
            os.makedirs(trace_dir)
        else:
            last_revision = self.get_last_revision(trace_id)
            
        next_revision = (last_revision + 1) if last_revision != None else 0
        revision_str = f"_rev{next_revision}"

        trace_extension = os.path.splitext(trace_path)[1]
        if not trace_extension:
            trace_extension = ".zstf"

        workload_dst_path = os.path.join(trace_dir, f"{trace_id}{revision_str}")
        trace_dst_path = f"{workload_dst_path}{trace_extension}"
        metadata_dst_path = f"{trace_dst_path}.metadata.yaml"

        shutil.copy(workload_path, workload_dst_path)
        shutil.copy(trace_path, trace_dst_path)
        shutil.copy(metadata_path, metadata_dst_path)

        print(f"Uploaded to: {trace_dir}")

    def get_all_ids(self):
        if not os.path.exists(self.storage_path):
            return []

        trace_ids = []
        for item in os.listdir(self.storage_path):
            item_path = os.path.join(self.storage_path, item)
            if os.path.isdir(item_path):
                trace_ids.append(item)

        return trace_ids

    def get_metadata(self, trace_id, revision=None):
        trace_path = f"{self.storage_path}/{trace_id}"
        if not os.path.exists(trace_path):
            raise FileNotFoundError(f"Trace path does not exist: {trace_path}")

        selected_metadata_path = ""
        metadata_files = [f for f in os.listdir(trace_path) if f.startswith(trace_id) and f.endswith('.metadata.yaml')]
        if revision is None:
            if not metadata_files:
                raise FileNotFoundError(f"No metadata files found for trace ID: {trace_id}")
            
            metadata_files = sorted(metadata_files)
            latest_metadata_file = metadata_files[-1]
            selected_metadata_path = os.path.join(trace_path, latest_metadata_file)
        else:
            for metadata_file in metadata_files:
                if f"_rev{revision}." in metadata_file:
                    selected_metadata_path = os.path.join(trace_path, metadata_file)
                    break

        metadata = MetadataParser.read_metadata(selected_metadata_path)
        return metadata



