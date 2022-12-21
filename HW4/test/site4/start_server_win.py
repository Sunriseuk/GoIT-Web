from http.server import HTTPServer, CGIHTTPRequestHandler

server_adress = ('', 8000)

httpd = HTTPServer(server_adress, CGIHTTPRequestHandler) #запускает сервер по указанному адресу и дополнительно CGI скрипті

httpd.serve_forever() #запускает сервер до тех пор, пока открыто окно выполнения