from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, Władysław Pniewski"


@app.route('/name/<name>')
def nname(name=None):
    return f"Hello, {name}"