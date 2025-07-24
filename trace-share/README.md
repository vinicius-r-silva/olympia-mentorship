# Trace Share Tool

A Python command-line interface (CLI) tool to manage shared trace files,such as uploding, searching and downloading traces.

## Requirements

> TODO: Add dependencies, e.g., Python version and required packages.


## Usage

Run the script using:

```bash
python trace_share.py <command> [options]
```

To view all available commands and options:

```bash
$ python trace_share.py --help
Usage: python trace_share.py COMMAND [OPTIONS]

CLI tool for Olympia traces exploration

Commands:
  connect    Connect to the system or database.
  upload     Upload workload and trace.
  search     Search traces by specified expression.
  list       List items by category.
  get        Download a specified trace file.

Run 'trace_share COMMAND --help' for more information on a command.

For more help on how to use trace_share, head to GITHUB_README_LINK
```

---

## Available Commands

### `upload`

Uploads a trace file along with its associated workload and metadata.
```bash
$ python trace_share.py upload --help
Usage:  python trace_share.py upload [OPTIONS]

Upload a workload, trace and metadata to the database

Options:
      --workload  Path to the workload file.
      --trace     Path to the trace file (optional).
      
If `--trace` is omitted, it defaults to `<workload>.zstf`.
```

Examples:
```bash
python trace_share.py upload --workload path/to/workload.out --trace path/to/trace.zstf
python trace_share.py upload --workload path/to/workload.out
```

> Requires a metadata file located at `<trace>.metadata.yaml`.

---

### `search`

Search can be used to search for the given regex term in the list of available traces and metadata matches

```bash
$ python trace_share.py search --help
Usage:  python trace_share.py search [OPTIONS] [REGEX]

Search for traces and metadata using a regular expression.

Arguments:
      REGEX             Regex expression to search with.

Options:
      --names-only      Search only by trace name (ignore metadata).
```
> TODO example

---

### `list`
```bash
$ python trace_share.py list --help
Usage:  python trace_share.py list [OPTIONS]

List database traces or related entities.

Options:
      --traces        Lists available traces (default)
      --companies     Lists associated companies
      
If no option is passed, all traces are listed by default.
```
> TODO example

<!-- ```bash
$ python trace_share.py list --traces
```
```bash
$ python trace_share.py list --companies
``` -->
---

### `get`

Downloads a specified trace file.

```bash
$ python trace_share.py get --help
Usage:  python trace_share.py get [OPTIONS] TRACE 

Download a specified trace file.

Arguments:
      TRACE             Name of the trace to download.

Options:
      --revision        Revision number. If not specified, the latest revision is used.
      --company         Filter by associated company.
      --author          Filter by author.
      -o, --output      Output file path.
```
> TODO example
