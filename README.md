# Universal Safe Database MCP Toolbox

A secure, universal, and privacy-first Model Context Protocol (MCP) server that empowers AI models to securely analyze SQLite datasets and view local text documents without risking data leaks, unauthorized alterations, or prompt injection exploits.

## Core Features

- **Read-Only Enforcement:** Strict internal whitelist filters block dangerous SQL statements (`DROP`, `DELETE`, `UPDATE`, `INSERT`) instantly, shielding datasets from destructive mutations.
- **Dynamic Schema Discovery:** Automatic multi-step scanning discovers table architecture dynamically, eliminating model hallucinations.
- **Automated Row Pagination:** Enforces a rigid ceiling of 50 rows per page to prevent high token expenses and memory overhead on large production tables.
- **Local Privacy Isolation:** Operates 100% locally via standard input/output (`stdio`). Your raw database files never travel to cloud networks or outside environments.
- **Query Timeout Bounds:** Integrated 3-second runtime safety abort thresholds shield host CPU memory assets against recursive recursive table join locking loops.

## Repository Layout

```text
📁 secure-database-mcp/
  └── 📁 Universal_safe_db/
        ├── mcp_server.py      # Core Python server logic
        ├── requirements.txt   # Application dependencies
        └── README.md          # Project documentation
```

## Setup & Testing

### 1. Installation
Install project requirements via your local prompt environment:
```bash
pip install -r requirements.txt
```

### 2. Launch Local Debug Inspector
You can test and run your tool visually inside a free local web pane in your browser using the official MCP Inspector. Run the following command, passing your target database file at the end:
```bash
npx @modelcontextprotocol/inspector@latest python mcp_server.py /path/to/your/dataset.db
```

### 3. Registering with Cursor IDE
To leverage this toolbox for free inside Cursor, navigate to **Settings -> Features -> MCP**, click **Add New MCP Server**, and configure:
- **Name:** universal-database-toolbox
- **Type:** stdio
- **Command:** python
- **Args:** "/absolute/path/to/Universal_safe_db/mcp_server.py" "/absolute/path/to/your/dataset.db"

## Available Tools

- `list_directory_databases`: Scans local paths to auto-discover active SQLite extensions.
- `inspect_dataset_schema`: Discovers available tables and structured definitions dynamically.
- `fetch_data_safely`: Executes read-only paginated data queries securely.
- `read_file_safely`: Reads local text logs or configuration document files cleanly.

## License
MIT License. Open-source contribution framework.
