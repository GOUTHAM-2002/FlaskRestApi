from flask import Flask,url_for,request,json,Response,jsonify
from functools import wraps
app=Flask(__name__)

def check_auth(username,password):
    return username=="admin" and password=="pass"

def authenticate():
    message = {'message':"Authenticte."}
    resp = jsonify(message)
    resp.status_code=401
    resp.headers["WWW-Authenticate"] = "basic realm=Example"

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        elif not check_auth(auth.username,auth.password):
            return authenticate()
        return f(*args,**kwargs)

    return decorated

@app.route('/secrets')
@requires_auth
def api_hello():
    return "Shhh this is top secret spy stuff!"


@app.route("/messages",methods=["POST"])
def api_message():
    if request.headers["Content-Type"] == "text/plain":
        return "Text Message" + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"


@app.route("/")
def api_root():
    return "Welcome"

@app.route('/hello')
def api_hello():
    data = {
        'hello': 'world',
        'number': 3
    }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://luisrei.com'

    return resp



@app.route("/echo",methods=["GET","POST","PATCH","PUT","DELETE"])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

if __name__ == "__main__":
    app.run(debug=True)