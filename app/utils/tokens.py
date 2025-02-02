import jwt
import datetime

from app import app

# Secret key for token signing (keep this secret)
SECRET_KEY = app.secret_key

# Function to generate a token with an expiration time
def generate_token(expiration_hours=24, **payload):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)  # Token expires in 24 hours
    payload = {
        'exp': expiration_time,
        **payload
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Function to verify and decode a token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        expiration_time = payload['exp']
        current_time = datetime.datetime.utcnow().timestamp()
        if current_time <= expiration_time:
            return payload
        else:
            return None  # Token has expired
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return False # Token is invalid