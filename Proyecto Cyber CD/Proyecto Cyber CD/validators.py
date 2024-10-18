from models.usuario import Usuario
from models.visitas import Visitas
from utils import check_email
from datetime import datetime

def validate_visita(form):
    errors = []
    fecha_ingresada = form.get('fecha')  
    
    if not fecha_ingresada:
        errors.append("El campo de fecha es obligatorio.")
    else:
        try:
            fecha_formateada = datetime.strptime(fecha_ingresada, '%Y-%m-%d').date()
            if fecha_formateada > datetime.now().date():
                errors.append("La fecha de la visita no puede ser una fecha futura.")
        except ValueError:
            errors.append("El formato correcto es YYYY-MM-DD.")
    return errors



def validate_user(form):
    errors = []
    
    if (len(form["nombre"]) < 2):
        errors.append("El largo del nombre debe ser mayor a 2 caracteres")
    
    if (len(form["apellido"]) < 2):
        errors.append("El largo del apellido debe ser mayor a 2 caracteres")
        
    if not check_email(form["email"]):
        errors.append("El email no es un email valido")
        
    if form["password"] != form["password2"]:
        errors.append("Las contraseñas deben calzar")
        
    users = Usuario.get_user_email(form["email"])
    if len(users) > 0:
        errors.append("Usuario con email ya creado")
        
    return errors