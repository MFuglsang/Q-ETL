import http.server
import socketserver
from pathlib import Path
import json
import os
import urllib

def get_config():
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    settings_file = parent_dir / 'settings.json'

    with open(settings_file, 'r') as f:
        settings = json.load(f)
    
    return settings
    
settings = get_config()
log_dir = settings['logdir']

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def list_txt_files(self, directory):
        try:
            file_list = os.listdir(directory)
            # txt_files = [f for f in file_list if f.endswith('.txt') and os.path.isfile(os.path.join(directory, f))]
            txt_files = [
                (f, os.path.getctime(os.path.join(directory, f)))
                for f in file_list if f.endswith('.txt') and os.path.isfile(os.path.join(directory, f))
            ]
            txt_files.sort(key=lambda x: x[1], reverse=True)
            return [f[0] for f in txt_files]
        except OSError:
            return []

    def do_GET(self):
        filepath = self.translate_path(self.path)
        if os.path.isdir(filepath):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            file_list = self.list_txt_files(filepath)
            response = "<html><body><h2>Log filer</h2><ul>"

            for file in file_list:
                file_url = urllib.parse.quote(file)
                response += f'<li><a href="{file_url}">{file}</a></li>'

            response += '</ul></body></html>'

            self.wfile.write(response.encode('utf-8'))

        elif os.path.isfile(filepath) and filepath.endswith('.txt'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found or access denied')

os.chdir(log_dir)

PORT = 3000

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f'Serving log files at http://localhost:{PORT}')
    httpd.serve_forever()