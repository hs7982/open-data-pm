import os

def load_sql_query(filename: str) -> str:
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, 'sql', filename)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read() 