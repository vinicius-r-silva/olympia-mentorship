from .base import CommandHandler
from utils.database_explorer import DatabaseExplorer
from utils.ui import print_medatata_details

class ListHandler(CommandHandler):
    def __init__(self):
        self.explorer = DatabaseExplorer()

    def run(self, args):
        match vars(args):
            case {'companies': True}:
                self._list_companies()
            case _:
                self._list_traces()

    def _list_traces(self):
        trace_ids = self.explorer.get_all_ids()
        if not trace_ids:
            print("No traces found.")
            return
        
        for trace_id in sorted(trace_ids):
            metadata = self.explorer.get_metadata(trace_id)
            last_revision = self.explorer.get_last_revision(trace_id)
            print_medatata_details(trace_id, metadata, last_revision)
            print("")

    def _list_companies(self):
        trace_ids = self.explorer.get_all_ids()
        if not trace_ids:
            print("No traces found.")
            return
        
        companies = set()
        for trace_id in trace_ids:
            metadata = self.explorer.get_metadata(trace_id)
            company_name = metadata['author']['company']
            companies.add(company_name)
        
        for company in sorted(companies):
            print(company)

