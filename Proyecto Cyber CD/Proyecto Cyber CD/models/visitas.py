from config.db import connectToMySQL
from models.usuario import Usuario

class Visitas:
    def __init__(self, data):
        self.idvisitas = data["idvisitas"] 
        self.parque = data["parque"]  
        self.fecha = data["fecha"]  
        self.raiting = data["raiting"]  
        self.detalles = data["detalles"] 
        self.visitante = data["visitante"]  

        self.visitante_obj = None

    @classmethod
    def select_all(cls):
        query = "SELECT * FROM visitas LEFT JOIN usuarios ON visitas.visitante = usuarios.idusuarios ORDER BY visitas.raiting DESC;"
        results = connectToMySQL("parqueaventura").query_db(query)
        visitas = []
        for result in results:
            visita = cls(result)
            visitante = Usuario(result)
            visita.visitante_obj = visitante
            visitas.append(visita)
        return visitas


    @classmethod
    def select_one(cls, id):
        query = "SELECT * FROM visitas LEFT JOIN usuarios ON visitas.visitante = usuarios.idusuarios WHERE idvisitas=%(id)s;"
        results = connectToMySQL("parqueaventura").query_db(query,{"id":id})
        visitas = []

        for result in results:
            visita = cls(result)
            visitante = Usuario(result)
            visita.visitante_obj = visitante
            visitas.append(visita)
        return visitas

    @classmethod 
    def insert(cls, data):
        query = """
        INSERT INTO `parqueaventura`.`visitas`
    (`parque`, `fecha`, `raiting`, `detalles`,`visitante`)
    VALUES (%(parque)s, %(fecha)s, %(raiting)s, %(detalles)s,%(visitante)s);
"""
    
        print(data)
        result = connectToMySQL("parqueaventura").query_db(query, data)
        return result
    
    @classmethod 
    def delete(cls,id):
        query = "DELETE FROM `visitas` WHERE idvisitas=%(id)s;"
        result =  connectToMySQL("parqueaventura").query_db(query,{"id":id})
        return result
    
    @classmethod
    def update(cls, data):
        query = """UPDATE `parqueaventura`.`visitas`
            SET
            `idvisitas` = %(idvisitas)s,
            `parque` = %(parque)s,
            `fecha` = %(fecha)s ,
            `raiting` = %(raiting)s ,
            `detalles` = %(detalles)s 
            WHERE `idvisitas` = %(idvisitas)s;
        """
        
        result =  connectToMySQL("parqueaventura").query_db(query, data)
        return result