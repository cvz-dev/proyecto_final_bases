import mysql.connector
from decimal import Decimal
from config import CONFIG_MYSQL


def obtener_conexion():
    return mysql.connector.connect(**CONFIG_MYSQL)


def convertir_decimal(valor):
    """Convierte valores Decimal de MySQL a tipos aceptados por Neo4j."""
    if isinstance(valor, Decimal):
        if valor % 1 == 0:
            return int(valor)
        return float(valor)
    return valor


def limpiar_fila(fila: dict) -> dict:
    return {
        llave: convertir_decimal(valor)
        for llave, valor in fila.items()
    }


def consultar_todo(consulta: str, parametros=None) -> list[dict]:
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(consulta, parametros or ())
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [limpiar_fila(fila) for fila in filas]


# Lecturas por tabla

def obtener_departamentos():
    return consultar_todo("SELECT * FROM department")


def obtener_salones():
    return consultar_todo("SELECT * FROM classroom")


def obtener_cursos():
    return consultar_todo("SELECT * FROM course")


def obtener_profesores():
    return consultar_todo("SELECT * FROM instructor")


def obtener_estudiantes():
    return consultar_todo("SELECT * FROM student")


def obtener_secciones():
    return consultar_todo("SELECT * FROM section")


def obtener_horarios():
    return consultar_todo("SELECT * FROM time_slot")


def obtener_imparticiones():
    return consultar_todo("SELECT * FROM teaches")


def obtener_inscripciones():
    return consultar_todo("SELECT * FROM takes")


def obtener_asesorias():
    return consultar_todo("SELECT * FROM advisor")


def obtener_prerrequisitos():
    return consultar_todo("SELECT * FROM prereq")
