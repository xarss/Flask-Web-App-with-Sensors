from flask import Flask, render_template, session, g
from controllers.auth_controller import auth
from controllers.iot_controller import iot

app = Flask(__name__, template_folder="./views/", static_folder="./static/")

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(iot, url_prefix='/iot')

@app.route('/')
def index():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)