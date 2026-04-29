import re
import os
from app.cliente_mysql import obtener_conexion
from app.cliente_neo4j import ClienteNeo4j


Datos_consultas= {
    "1":  {
        "titulo":      "Profesores con salario mayor al promedio de su departamento",
        "descripcion": "Muestra los profesores cuyo salario supera el promedio de su mismo departamento.",
    },
    "2":  {
        "titulo":      "Departamentos con profesores, salario promedio y presupuesto por profesor",
        "descripcion": "Calcula métricas agregadas por departamento.",
    },
    "3":  {
        "titulo":      "Profesores con más de una sección en un semestre",
        "descripcion": "Identifica profesores con múltiples secciones en el mismo periodo.",
    },
    "4":  {
        "titulo":      "Cursos con prerrequisitos",
        "descripcion": "Cursos que requieren haber cursado otro antes.",
    },
    "5":  {
        "titulo":      "Departamentos sin profesores",
        "descripcion": "Departamentos que no tienen instructores asociados.",
    },
    "6":  {
        "titulo":      "Estudiantes con su asesor y departamento del asesor",
        "descripcion": "Muestra la relación asesor-estudiante incluyendo el departamento.",
    },
    "7":  {
        "titulo":      "Secciones 2009 con nombre del curso y aula",
        "descripcion": "Secciones impartidas en 2009 junto con su curso y salón.",
    },
    "8":  {
        "titulo":      "Cursos aprobados por estudiante",
        "descripcion": "Cursos donde la calificación no es F.",
    },
    "9":  {
        "titulo":      "Profesores y estudiantes que tuvieron en sus secciones",
        "descripcion": "Relación profesor-estudiante a través de secciones compartidas.",
    },
    "10": {
        "titulo":      "Cursos que nunca ha tomado nadie",
        "descripcion": "Cursos sin ningún estudiante inscrito.",
    },
}


raiz = os.path.dirname(os.path.dirname(__file__))


def _parsear_archivo(ruta, prefijo):
    with open(ruta, encoding="utf-8") as f:
        contenido = f.read()

    resultado = {}
    for bloque in contenido.split("\n\n"):
        bloque = bloque.strip()
        if not bloque:
            continue
        match = re.search(r"Q(\d+)", bloque)
        if not match:
            continue
        numero = str(int(match.group(1)))
        lineas_query = []
        for l in bloque.splitlines():
            if not l.strip().startswith(prefijo):
                lineas_query.append(l)
        resultado[numero] = "\n".join(lineas_query).strip()

    return resultado


def _cargar_consultas():
    ruta_sql    = os.path.join(raiz, "consultas", "consultas_sql.sql")
    ruta_cypher = os.path.join(raiz, "consultas", "consultas_cypher.cypher")

    sqls    = _parsear_archivo(ruta_sql,    prefijo="--")
    cyphers = _parsear_archivo(ruta_cypher, prefijo="//")

    consultas = {}
    for num, info_pregunta in Datos_consultas.items():
        consultas[num] = {
            **info_pregunta,
            "sql":    sqls.get(num,    "-- query no encontrada"),
            "cypher": cyphers.get(num, "// query no encontrada"),
        }
    return consultas


CONSULTAS = _cargar_consultas()


def ejecutar_sql(consulta_sql):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(consulta_sql)
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas


def ejecutar_cypher(cliente, consulta):
    return cliente.ejecutar(consulta)


def mostrar_filas(filas, limite=10):
    if not filas:
        print("Sin resultados")
        return
    for fila in filas[:limite]:
        print(fila)


def ejecutar_consulta(opcion):
    consulta = CONSULTAS[opcion]
    cliente = ClienteNeo4j()

    print("\n" + "=" * 60)
    print(consulta["titulo"])
    print("=" * 60)
    print(f"\n{consulta['descripcion']}\n")

    print("── SQL " + "─" * 54)
    filas_sql = ejecutar_sql(consulta["sql"])
    mostrar_filas(filas_sql)
    print(f"Total: {len(filas_sql)} filas")

    print("\n── Cypher " + "─" * 50)
    filas_cypher = ejecutar_cypher(cliente, consulta["cypher"])
    mostrar_filas(filas_cypher)
    print(f"Total: {len(filas_cypher)} filas")

    cliente.cerrar()


def mostrar_menu_consultas():
    while True:
        print("\n=== MENÚ ===")
        for k, v in CONSULTAS.items():
            print(f"  {k}. {v['titulo']}")
        print("  0. Salir")

        opcion = input("\nOpción: ").strip()

        if opcion == "0":
            break
        if opcion not in CONSULTAS:
            print("Opción inválida")
            continue

        ejecutar_consulta(opcion)
