from jose import jwt, JWTError

#in ubuntu console write "openssl rand -hex 32"
secret = '692ef2fcce8526152d643bd16e64003f7d52899f760019fd2aa9dc823103bbc6'

payload = {'sub': 'example@api.com', 'username': 'kolobok', 'role': 'moderator'}

token = jwt.encode(payload, secret, algorithm='HS256')

print(token)

try:
    r = jwt.decode(token, secret, algorithms=['HS256'])
    print(r)
except JWTError as e:
    print(e)