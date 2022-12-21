from http.server import HTTPServer, BaseHTTPRequestHandler
import os

template_path = 'test/'

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def send_html_file(self, filename: str, status_code: int = 200):
        self.send_response(status_code,)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(os.path.join(template_path, filename), 'rb') as file:
                self.wfile.write(file.read())
        


    def do_Get(self):
        print(f'{self.path=}')
        
        if self.path == '/':
            self.send_html_file('index.html')
        elif self.path == '/contact':
            self.send_html_file('contact.html')
        
        

def run():
    http = HTTPServer(('0.0.0.0', 8000), CustomHTTPRequestHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close

if __name__ == "__main__":
    run()