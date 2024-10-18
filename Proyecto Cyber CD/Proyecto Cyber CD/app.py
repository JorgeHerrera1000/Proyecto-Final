from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from flask_bcrypt import Bcrypt

from models.visitas import Visitas
from models.usuario import Usuario

from validators import validate_visita, validate_user

app = Flask(__name__)
app.secret_key = "SecRet0"

bcrypt = Bcrypt(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("disclaimer.html")
@app.route("/home")
def home():
    return render_template("home.html") 

@app.route("/warning")
def warning():
    return render_template("disclaimer.html")  

@app.route("/login/")
def signup():
    return render_template("login.html")

@app.route("/phishing")
def showvuln1():
    return render_template("phishing.html")

@app.route("/formjacking")
def showvuln2():
    return render_template("formjacking.html")

@app.route("/malware")
def showvuln3():
    return render_template("malware.html")

@app.route("/register/", methods=["POST"])
def register():
    form = request.form.to_dict()
    errors = validate_user(form)
        
    if len(errors) > 0:
        return render_template("login.html", register_errors=errors)
    
    form["password"] =  bcrypt.generate_password_hash(form["password"]) 
    newId = Usuario.insert_one(form)
    
    session["id"] = newId
    session["nombre"] = f"{form['nombre']} {form['apellido']}"
    
    return redirect("/home")


@app.route("/consejos")
def consejos():
    return render_template("consejos.html")


@app.route("/spoofing")
def spoofing():
    return render_template("spoofing.html")

@app.route("/hackeado")
def hackeado():
    return render_template("hackeado.html")

# Recive la info del formulario de login   
@app.route("/login/", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    
    errors = []
    
    users = Usuario.get_user_email(email)
    
    if (len(users) == 0):
        errors.append("No existe un usuario con esta combinación de email y password")
    
    user = users[0]
    
    compare = bcrypt.check_password_hash(user.password, password)
    if (not compare):
        errors.append("No existe un usuario con esta combinación de email y password")
        
    if len(errors) > 0:
        return render_template("index.html", login_errors=errors)
    
    session["id"] = user.idusuarios
    session["nombre"] = f"{user.nombre} {user.apellido}"
    
    return redirect("/dashboard/")


@app.route("/logout/", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")



##### CRUD de Entidades

## READ 
@app.route("/dashboard/", methods=["GET"])
def visitas():
    if not session:
        return redirect("/")
    visitas = Visitas.select_all()
    return render_template("welcome.html", visitas=visitas)

@app.route("/ver/<visita_id>", methods=["GET"])
def visitas_view(visita_id):
    if not session:
        return redirect("/")
    visita = Visitas.select_one(visita_id)
    usuarios = Usuario.get_all()
    if len(visita) == 0:
        return "Visita no encontrado", 404
    return render_template("event.html", visita=visita[0])


## CREATE
@app.route("/nuevo/", methods=["GET"])
def new_event_form():
    if not session:
        return redirect("/")
    usuarios = Usuario.get_all()
    return render_template("new_event.html", users=usuarios)

@app.route("/visitas/crear/", methods=["POST"])
def new_event():
    if not session:
        return redirect("/")
    
    form = request.form.to_dict()
    errors = validate_visita(form)
    print(form)
    if (len(errors) > 0):
        return render_template("new_event.html", error_messages=errors)
    
    form["visitante"] = session["id"]
    result = Visitas.insert(form)
    print(form)
    if not result:
        usuarios = Usuario.get_all()
        return render_template("new_event.html", error_messages=["Ha ocurrido un error en el servidor"],users=usuarios)
    
    return redirect("/dashboard/")
    

### EDIT


@app.route("/editar/<visita_id>", methods=["GET"])
def edit_visit_form(visita_id):
    if not session:
        return redirect("/")
    visita = Visitas.select_one(visita_id)
    if len(visita) == 0:
        return "Visita no encontrada", 404
    return render_template("edit_event.html", visita=visita[0])
    
    
@app.route("/editar/visitas/", methods=["POST"])
def edit_visit():
    if not session:
        return redirect("/")
    form = request.form.to_dict()

    visita = Visitas.select_one(form["idvisitas"])
    if len(visita) == 0:
        return "Visita no encontrada", 404
    
    errors = validate_visita(form)
    
    if (len(errors) > 0):
        return render_template("edit_event.html", visita=visita[0], error_messages=errors)
    
    form["visitante"] = session["id"]
    
    Visitas.update(form)
    return redirect("/dashboard")

## DELETE

@app.route("/eliminar/<id_visita>", methods=["GET"])
def eliminar_visita(id_visita):
    Visitas.delete(id_visita)
    return redirect("/dashboard")    

## BOTON ME GUSTA 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)