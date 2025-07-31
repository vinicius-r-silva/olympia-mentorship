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

### `connect`

Authenticate / connect with the traces database

> To be defined how the authentication / connections will be defined, also the necessecity of such authentication


---

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
$ python trace_share.py upload --workload path/to/workload.out --trace path/to/trace.zstf
Uploaded trace with ID: company_test_1_workload
```

> Requires a metadata file located at `<trace>.metadata.yaml`.

> For every upload, will be genreated a unique id

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

Examples:

```bash
$ python trace_share.py list --traces
example_company_1_dhrystone

Workload: dhrystone
Author: Jane Doe
Trace Timestamp: 2025-07-20T21:05:32.840053+00:00
Revision: 2

---------------------------------

example_company_2_dhrystone_partial_trace_0_0_100

Workload: dhrystone
Author: Jane Doe
Trace Timestamp: 2025-07-20T21:05:32.840053+00:00
Revision: 0
Trace Interval:
  Instruction PC: 0
  PC Count: 0
  Interval Length: 100

---------------------------------
```

```bash
$ python trace_share.py list --companies
example_company_1
example_company_2
```
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


## Trace ID

When a trace file is uploaded to the trace archive, a `trace_id` is automatically created and filled into the metadata. The `trace_id` follows the structure:

```text
<workload_filename>_<workload_version>_<trace_part>_<revision>
```

Where:
- **`workload_filename`**: Taken directly from the `workload.filename` field.
- **`workload_version`**: If multiple workloads with the same filename exist (but different SHA256), the first is versioned as `v0`, and subsequent versions increment (e.g., `dhrystone_v0`, `dhrystone_v1`, ...).
- **`trace_part`**:

  - If the workload is **fully traced**, this field is `fully-traced`.
  - If partially traced, this field is `part<N>`, where `<N>` increments with each distinct interval (e.g., `part0`, `part1`, ...).

- **`revision`**: If the same trace (same workload SHA256 and trace interval) is uploaded again, a new revision is created using `rev<N>` (e.g., `rev0`, `rev1`, ...).

---

### Example Trace IDs

| Upload # | Description                                               | Trace ID                              |
| -------- | --------------------------------------------------------- | ------------------------------------- |
| 1st      | `dhrystone` compiled with `-O3`, fully traced             | `dhrystone_v0_fully-traced_rev0`      |
| 2nd      | `dhrystone` `-O3`, traced from instruction 0 to 1,000,000 | `dhrystone_v0_part0_rev0`             |
| 3rd      | `dhrystone` `-O3`, traced from 2,000,000 to 3,000,000     | `dhrystone_v0_part1_rev0`             |
| 4th      | `dhrystone` `-O3`, traced from 1,000,000 to 2,000,000     | `dhrystone_v0_part2_rev0`             |
| 5th      | Same trace as 2nd (re-uploaded)                           | `dhrystone_v0_part0_rev1`             |
| 6th      | `dhrystone` compiled with `-O2`, fully traced             | `dhrystone_v1_fully-traced_rev0`      |
| 7th      | `dhrystone-test` compiled with `-O3`, fully traced        | `dhrystone-test_v0_fully-traced_rev0` |

---
