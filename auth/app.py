""" Get Auhorization Token from the  Client """
import json
from functools import wraps
from flask import Flask, request, abort
from jose import jwt
from urllib.request import urlopen


# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'irzelindo.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

APP = Flask(__name__)

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code



def check_permissions(permission, payload):
    if "permissions" not in payload:
        abort(400)

    if permission not in payload["permissions"]:
        abort(403)

    return True



def requires_auth(permission=""):
    def requires_auth_decorator(f):
        """ Decorator function """
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            # is_valid = verify_decode_jwt(jwt)
            try:
                payload = verify_decode_jwt(jwt)
            except:
                abort(401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def get_token_auth_header():
    """ Extracts the Token from the Bearer  Auth Header """
    if "Authorization" not in request.headers:
        abort(401)

    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(" ")

    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != "bearer":
        abort(401)

    return header_parts[1].strip()

@APP.route("/images")
@requires_auth('get:images')
def images(jwt):
    """ Retrieves the headers auth keys """
    print(jwt)

    return "Not implemented"
