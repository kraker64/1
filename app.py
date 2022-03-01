from flask import Flask, redirect, render_template, request, redirect, url_for, flash
from config import config
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from requests import get
from models.ModelUser import ModelUser
from flask_login import login_required,LoginManager,login_user,logout_user
from models.entities.User import User


headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhYjQ5NDEyNmEzOTQ0ZjgwYmRhMTc2YzZmMWI0YjYwYyIsImlhdCI6MTY0NTA1MTY1NiwiZXhwIjoxOTYwNDExNjU2fQ.VRKr35Sb6vlx97SKTws1U6r-wGXhnLZzSU1SBCI_Q9I",
    "content-type": "application/json",
}

app = Flask(__name__)

csrf= CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method=='POST':
        user = User(0,request.form['username'],request.form['password'])
        logged_user = ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid password... ")
                return render_template('auth/login.html')
        else:
            flash("User not found... ")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/home')
def home():
    return render_template('home.html')

#inici Energia casa

@app.route("/ecasa/A")
@login_required
def CA():
    url = "http://homeassistant.local:8123/api/states/sensor.wifi_smart_meter_phase_a_current"
    response = get(url, headers=headers)
    return response.text[67]+response.text[68]+response.text[69]+response.text[70]
@app.route("/ecasa/W")
@login_required
def CW():
    url = "http://homeassistant.local:8123/api/states/sensor.wifi_smart_meter_phase_a_power"
    response = get(url, headers=headers)
    return response.text[65]+response.text[66]+response.text[67]+response.text[68]+response.text[69]
@app.route("/ecasa/V")
@login_required
def CV():
    url = "http://homeassistant.local:8123/api/states/sensor.wifi_smart_meter_phase_a_voltage"
    response = get(url, headers=headers)
    return response.text[67]+response.text[68]+response.text[69]+response.text[70]+response.text[71]
@app.route("/ecasa/Total")
@login_required
def CT():
    url = "http://homeassistant.local:8123/api/states/sensor.wifi_smart_meter_total_energy"
    response = get(url, headers=headers)
    return response.text[64]+response.text[65]+response.text[66]+response.text[67]+response.text[68]+response.text[69]+response.text[70]

#final Energia casa


#inici Energia plaques

@app.route("/eplaques/A")
@login_required
def PA():
    url = "http://192.168.31.141:8888/"
    response = get(url, headers=headers)
    return response.text

@app.route("/eplaques/W")
@login_required
def PW():
    url = "http://192.168.31.141:8888/"
    response = get(url, headers=headers)
    
    return str("{:.2f}".format(int(CV()[0]+CV()[1]+CV()[2]) * float(response.text[0]+response.text[1]+response.text[2]+response.text[3])))



#final Energia plaques
if __name__ == '__main__':
    from waitress import serve
  
    csrf.init_app(app)
    app.config.from_object(config['production'])
    serve(app, host="0.0.0.0", port=10000)

