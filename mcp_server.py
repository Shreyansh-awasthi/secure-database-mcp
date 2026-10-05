import os
import re
import sys
import sqlite3
from mcp.server.fastmcp import FastMCP

server = FastMCP("Universal-Safe-Database-Toolbox")

def get_db_path() -> str:
    if len(sys.argv) > 1:
        return sys.argv[-1]
    return os.environ.get("DB_PATH", "data.db")

@server.tool()
def list_directory_databases(directory_path: str = ".") -> str:
    if not os.path.exists(directory_path):
        return f"Error: Directory not found at '{directory_path}'"
    try:
        files = os.listdir(directory_path)
        db_files = [f for f in files if f.endswith(('.db', '.sqlite', '.sqlite3'))]
        if not db_files:
            return "No SQLite database files found in this directory."
        return "Found databases:\n" + "\n".join(f"- {f}" for f in db_files)
    except Exception as e:
        return f"Error scanning directory: {str(e)}"

@server.tool()
def inspect_dataset_schema() -> str:
    db_path = get_db_path()
    if not os.path.exists(db_path):
        return f"Error: No database file found at '{db_path}'. Please check your path."
        
    try:
        conn = sqlite3.connect(db_path, timeout=3.0)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            return "The database is empty (contains no tables)."
            
        schema_info = "Dataset Schema Discovered:\n"
        for table in tables:
            table_name = table[0]
            schema_info += f"\nTable: {table_name}\n   Columns:\n"
            
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                col_name, col_type = col[1], col[2]
                schema_info += f"     - {col_name} ({col_type})\n"
                
        conn.close()
        return schema_info
    except Exception as e:
        return f"Database error: {str(e)}"

@server.tool()
def fetch_data_safely(sql_query: str, page: int = 1, rows_per_page: int = 50) -> str:
    forbidden_words = ["insert", "update", "delete", "drop", "alter", "create", "replace", "truncate"]
    clean_query = sql_query.strip().lower()
    
    if not clean_query.startswith("select"):
        return "Security Violation: Only 'SELECT' queries are allowed to protect the dataset."
        
    for word in forbidden_words:
        if re.search(r'\b' + word + r'\b', clean_query):
            return f"Security Violation: The command '{word.upper()}' is forbidden."
            
    if rows_per_page > 100:
        rows_per_page = 100
        
    if "limit" in clean_query:
        sql_query = re.sub(r'\blimit\b.*', '', sql_query, flags=re.IGNORECASE)
        
    offset = (page - 1) * rows_per_page
    final_query = f"{sql_query.rstrip(';').rstrip()} LIMIT {rows_per_page} OFFSET {offset};"
    
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path, timeout=3.0)
        cursor = conn.cursor()
        
        cursor.execute(final_query)
        rows = cursor.fetchall()
        
        column_names = [description[0] for description in cursor.description]
        
        conn.close()
        
        if not rows:
            return f"No results found on page {page}."
            
        headers = " | ".join(column_names)
        divider = " | ".join(["---"] * len(column_names))
        data_rows = "\n".join(f"| {' | '.join(str(item) for item in row)} |" for row in rows)
        
        page_info = f"\nShowing rows {offset + 1} to {offset + len(rows)} (Page {page})"
        return f"| {headers} |\n| {divider} |\n{data_rows}\n{page_info}"
        
    except Exception as e:
        return f"SQL Error: {str(e)}"

@server.tool()
def read_file_safely(file_path: str) -> str:
    if not os.path.exists(file_path):
        return f"Error: File not found at '{file_path}'"
        
    if os.path.isdir(file_path):
        return f"Error: '{file_path}' is a directory, not a file."
        
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

if __name__ == "__main__":
    server.run(transport="stdio")
