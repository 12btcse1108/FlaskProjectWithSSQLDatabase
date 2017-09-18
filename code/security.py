from werkzeug.security import safe_str_cmp
from user import User



def authenticate(username,password):
    print("username===="+username+"password===="+password)
    user = User.findByUsername(username)
    if user and safe_str_cmp(user.password , password):
        return user

def identity(payload):
    userid = payload["identity"]
    print([userid,]+"========")
    return User.findByUserid(userid)
