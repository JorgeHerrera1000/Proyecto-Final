from config.db import connectToMySQL

class Usuario:
    def __init__(self, data):
        self.idusuarios = data["idusuarios"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]

        self.visitante_obj = None
        
    @classmethod
    def get_user_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email=%(email)s;"
        results = connectToMySQL("parqueaventura").query_db(query, {"email": email})
        usuarios = []
        for usuario in results:
            usuarios.append(cls(usuario))
        return usuarios
    
    
    @classmethod
    def insert_one(cls, data):
        query = """
        INSERT INTO usuarios (
            `nombre`,
            `apellido`,
            `email`,
            `password`)
            VALUES
            (
                %(nombre)s,
                %(apellido)s,
                %(email)s,
                %(password)s
            );"""
        result = connectToMySQL("parqueaventura").query_db(query, data)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL("parqueaventura").query_db(query)
        usuarios = []
        for usuario in results:
                usuarios.append(cls(usuario))
        return usuarios
        