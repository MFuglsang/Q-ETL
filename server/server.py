import http.server
import socketserver
from pathlib import Path
import json
import os

def get_config():
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    settings_file = parent_dir / 'settings.json'

    with open(settings_file, 'r') as f:
        settings = json.load(f)
    
    return settings
    
settings = get_config()
log_dir = settings['logdir']

os.chdir(log_dir)

PORT = 3000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f'Serving log files at http://localhost:{PORT}')
    httpd.serve_forever()