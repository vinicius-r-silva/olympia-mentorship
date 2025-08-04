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
<workload id>.<trace attempt>.<trace.part>_<workload filename>
```

Where:
- **`workload id`**: A **sequential integer**, uniquely identifying a workload **based on its SHA256**. Assigned in upload order (e.g., `0`, `1`, `2`, ...).
- **`trace attempt`**: A **sequential number** representing a distinct tracing process for the same workload — whether it’s a full trace or a colletion of trace parts.
- **`trace_part`**: A **sequential index** of the specific part within a trace attempt.

  * For a **fully traced workload**, this will always be `0`.
  * For a **partial trace**, each part is numbered in upload order (e.g., `0`, `1`, `2`, ...).
- **`workload filename`**: Taken directly from the `workload.filename` field.
---

### Example Trace IDs

| Upload # | Description                                               | Trace ID                              |
| -------- | --------------------------------------------------------- | ------------------------------------- |
| 1st      | `dhrystone` compiled with `-O3`, fully traced             | `0.0.0_dhrystone`                     |
| 2nd      | `dhrystone` `-O3`, traced from instruction 0 to 1,000,000 | `0.1.0_dhrystone`                     |
| 3rd      | `dhrystone` `-O3`, traced from 1,000,000 to 2,000,000     | `0.1.1_dhrystone`                     |
| 4th      | `dhrystone` `-O3`, traced from 2,000,000 to 3,000,000     | `0.1.2_dhrystone`                     |
| 5th      | Same trace as 1st (re-uploaded)                           | `0.2.0_dhrystone`                     |
| 6th      | `dhrystone` compiled with `-O2`, fully traced             | `1.0.0_dhrystone`                     |
| 7th      | `embench` compiled with `-O3`, fully traced               | `2.0.0_embench`                       |

---

### Possible Improvements

#### 1. **Add `revision` support**

Allow trace re-uploads (e.g., bug fixes or corrections) without incrementing `trace_attempt`. Extend format to:

```text
<workload_id>.<trace_attempt>.<trace_part>.rev<revision>_<workload_filename>
```

**Example**:

* First partial upload of dhrystone: `0.1.0.rev0_dhrystone`
* Re-upload of the same part: `0.1.0.rev1_dhrystone`

#### 2. **id names**

Instead of only using numbers, use more descriptive ids, like:

```text
<workload_name>_v<workload_id>_attempt<attempt>_part<part>[_rev<revision>]
```

**Example**:

* `dhrystone_v0_attempt1_part0`
* `dhrystone_v0_attempt1_part1`
* `dhrystone_v0_attempt1_part1_rev1`


### Storage Folder Structure

For the trace archive, the following folder structure is proposed:

- **Workloads folder**: Contains all uploaded workloads.
  - Each workload is stored in its own folder using the structure:  
    `<workload_id>_<workload_sha256>`

- **Traces folder**: Contains trace files organized by workload and trace attempt.
  - Each workload has a folder named with its `workload_id`.
    - Each trace attempt is stored in a numbered subfolder with its `trace_attempt_id`.


The structure below illustrates a setup of the [Trace Id Example](#example-trace-ids):

```text
workloads/
├── 0_5c35ccfe1d5b81b2e37366b011107eec40e39aa2b930447edc1f83ceaf877066/
│   └── dhrystone
├── 1_065778c4b6cfaad7b8495cabad748179ce1ce2eb02453cc6fd10ded1fcb8125a/
│   └── dhrystone
└── 2_9be975d7e18f9ea98f95ef2a0d07be278109d111c269e4fb4c73429701adbf51/
    └── embench.zip

traces/
├── 0/
│   ├── 0/
│   │   ├── 0.0.0_dhrystone.zstf
│   │   └── 0.0.0_dhrystone.zstf.metadata.yaml
│   └── 1/
│       ├── 0.1.0_dhrystone.zstf
│       ├── 0.1.0_dhrystone.zstf.metadata.yaml
│       ├── 0.1.1_dhrystone.zstf
│       ├── 0.1.1_dhrystone.zstf.metadata.yaml
│       ├── 0.1.2_dhrystone.zstf
│       └── 0.1.2_dhrystone.zstf.metadata.yaml
├── 1/
│   └── 0/
│       ├── 1.0.0_dhrystone.zstf
│       └── 1.0.0_dhrystone.zstf.metadata.yaml
└── 2/
    └── 0/
        ├── 2.0.0_embench.zstf
        └── 2.0.0_embench.zstf.metadata.yaml
```



