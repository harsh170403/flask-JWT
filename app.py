import json
import base64
import hmac
import hashlib

def access_token(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


header = {
    "alg": "HS256",
    "typ": "JWT"
}
header_encoded = access_token(json.dumps(header).encode('utf-8'))


payload = {
    "sub": "1234567890",
    "name": "harsh",
    "iat": 15123462346323
}
payload_encoded = access_token(json.dumps(payload).encode('utf-8'))


secret = 'your-256-bit-secret'
signature_input = f"{header_encoded}.{payload_encoded}".encode('utf-8')
signature = hmac.new(secret.encode('utf-8'), signature_input, hashlib.sha256).digest()
signature_encoded = access_token(signature)


jwt = f"{header_encoded}.{payload_encoded}.{signature_encoded}"
print(jwt)
