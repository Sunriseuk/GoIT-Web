from jose import jwt

# данные для заполнения токена
payload = {"sub": "1234567890", "name": "John Doe"}

# создание токена с симметричным ключом
encoded = jwt.encode(payload, "secret_key", algorithm='HS256')
print(encoded)

# проверка токена
decoded = jwt.decode(encoded, "secret_key", algorithms=['HS256'])
print(decoded)