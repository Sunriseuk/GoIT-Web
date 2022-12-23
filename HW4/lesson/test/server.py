from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import unquote_plus, parse_qs #импорт декоддера и словаря для хранения данных


template_path = ''

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def send_html_file(self, filename: str, status_code: int = 200):
        self.send_response(status_code,)
        self.send_header('Content-type', 'text/html') #application/json
        self.end_headers()
        with open(os.path.join(template_path, filename), 'rb') as file:
                self.wfile.write(file.read())
        

    def do_GET(self):
        print(f'{self.path=}')
        #match and case вместо if - elif
        if self.path == '/':
            self.send_html_file('index.html')
        elif self.path == '/contact':
            self.send_html_file('contact.html')



    def do_POST(self):
        inputs: bytes = self.rfile.readline(int(self.headers['Content-Length']))
        # print(f'{data.decode()=}')
        query_data: str = unquote_plus(inputs.decode())
        # query_data = query_data + '&username=Nazarii' # добавляет дополнительное имя в словарь юзернейм
        # print(f'{unquote_plus(data.decode())=}')
        # print(f'{parse_qs(query_data)}=') 
        data: dict = parse_qs(query_data)
        errors = self.validate_contact_form(data)
        print(f'{errors=}')
        if errors:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
        else: 
            self.send_response(302) #Ответ серверу, что данные обработаны
            self.send_header('Location', '/') #Делает переадресацию на главную страницу (либо на любую другую "/error")
            #сохраняем данные
            with open('contact.json', 'a') as file:
                json.dump(data, file)
            
            #сделать чтобы джейсон сохранялся как список словарей [{}, {}, {}]

        
        self.end_headers()


    def validate_contact_form(self, data: dict) -> list:
        print(f'{data=}')
        email: str = data['email'][0]
        errors = []
        if '@' not in email:
            errors.append({'email' : 'wrong email'})
        message = data['message']
        forbidden_words = ['abc']
        if message in forbidden_words:
            errors.append('Wrong message')

        return errors


        
def run():
    http = HTTPServer(('', 8000), CustomHTTPRequestHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close

if __name__ == "__main__":
    run()