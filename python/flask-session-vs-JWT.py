
session_cookie = 'eyJ1c2VyIjp7ImlzX2FkbWluIjpmYWxzZSwiaXNfYXV0aGVudGljYXRlZCI6dHJ1ZX19.ZzmKeg.m8uS4-E7E8xGvqm5SQPGzyypp-8'

# decode jwt token

import jwt

decoded = jwt.decode(session_cookie, "secret", algorithms=["HS256"])
print(decoded)
