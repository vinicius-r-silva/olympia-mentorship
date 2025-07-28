import argparse
import sys

def parseArgs():
    # TODO add readme link
    parser = argparse.ArgumentParser(
        prog='trace_share',
        usage='python trace_share.py COMMAND [OPTIONS]',
        description='CLI tool for Olympia traces exploration',
        epilog="For more help on how to use trace_share, head to GITHUB_README_LINK",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )

    parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')

    subparsers = parser.add_subparsers(title='Commands', dest='command')

    connect_parser = subparsers.add_parser(
        'connect',
        help='Connect to the system or database.',
        description='Authenticate / connect with the traces database'
    )

    upload_parser = subparsers.add_parser(
        'upload',
        help='Upload workload and trace.',
        description='Upload a workload, trace and metadata to the database',
        formatter_class=argparse.RawTextHelpFormatter
    )
    upload_parser.add_argument('--workload', required=True, help='Path to the workload file.')
    upload_parser.add_argument('--trace', help='(optional) Path to the trace file. If omitted, defaults to <workload>.zstf')

    search_parser = subparsers.add_parser(
        'search',
        help='Search traces by specified expression.',
        description='Search for traces and metadata using a regular expression.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    search_parser.add_argument('regex', nargs='?', help='Regex expression to search with.')
    search_parser.add_argument('--names-only', action='store_true', help='Search only by trace name (ignore metadata).')

    list_parser = subparsers.add_parser(
        'list',
        help='List items by category.',
        description='List database traces or related entities.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    group = list_parser.add_mutually_exclusive_group()
    group.add_argument('--traces', action='store_true', help='Lists available traces (default)')
    group.add_argument('--companies', action='store_true', help='Lists associated companies')

    get_parser = subparsers.add_parser(
        'get',
        help='Download a specified trace file.',
        description='Download a specified trace file.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    get_parser.add_argument('trace', help='Name of the trace to download.')
    get_parser.add_argument('--revision', help='Revision number. If not specified, the latest revision is used.')
    get_parser.add_argument('--company', help='Filter by associated company.')
    get_parser.add_argument('--author', help='Filter by author.')
    get_parser.add_argument('-o', '--output', help='Output file path.')

    # If no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nRun 'trace_share COMMAND --help' for more information on a command.")
        print("\nFor more help on how to use trace_share, head to GITHUB_README_LINK")
        sys.exit(0)

    args = parser.parse_args()
    return args