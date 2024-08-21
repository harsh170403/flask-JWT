import pytest
import json
import base64
import hmac
import hashlib

from app import access_token, header_encoded, payload_encoded, signature_encoded, jwt

def test_access_token():
    data = b'test'
    expected = 'dGVzdA'
    assert access_token(data) == expected

def test_header_encoding():
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    expected_header = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).rstrip(b'=').decode('utf-8')
    assert header_encoded == expected_header

def test_payload_encoding():
    payload = {
        "sub": "1234567890",
        "name": "harsh",
        "iat": 15123462346323
    }
    expected_payload = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).rstrip(b'=').decode('utf-8')
    assert payload_encoded == expected_payload

def test_signature():
    secret = 'your-256-bit-secret'
    signature_input = f"{header_encoded}.{payload_encoded}".encode('utf-8')
    expected_signature = hmac.new(secret.encode('utf-8'), signature_input, hashlib.sha256).digest()
    expected_signature_encoded = base64.urlsafe_b64encode(expected_signature).rstrip(b'=').decode('utf-8')
    assert signature_encoded == expected_signature_encoded

def test_jwt_structure():
   
    assert jwt == f"{header_encoded}.{payload_encoded}.{signature_encoded}"
