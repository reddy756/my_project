from flask import Flask,render_template
from key import secret_key
from auth import auth_bp
from admin import admin_bp
from incharge import incharge_bp
from faculty import faculty_bp
from database import execute_query
import os
os.chdir(os.path.abspath(os.path.dirname(__file__)))
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SESSION_TYPE'] = 'FILESYSTEM'

@app.route('/')
def index():
    return render_template('index.html')

# Registering blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(incharge_bp)
app.register_blueprint(faculty_bp)

if __name__ == "__main__":
    app.run(debug=True)