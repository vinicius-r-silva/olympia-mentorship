from utils.cli_parser import parseArgs
from handlers.upload import UploadHandler
from handlers.list import ListHandler
from handlers.connect import ConnectHandler
from handlers.search import SearchHandler
from handlers.get import GetHandler

def main():
    args = parseArgs()
    command_map = {
        'connect': ConnectHandler(),
        'upload': UploadHandler(),
        'search': SearchHandler(),
        'list': ListHandler(),
        'get': GetHandler(),
    }

    handler = command_map.get(args.command)
    if handler:
        handler.run(args)
    else:
        print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()