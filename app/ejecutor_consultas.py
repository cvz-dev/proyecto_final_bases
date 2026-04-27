from app.cliente_mysql import obtener_conexion
from app.cliente_neo4j import ClienteNeo4j


CONSULTAS = {
    "1": {
        "titulo": "Profesores con salario mayor al promedio de su departamento",
        "descripcion": "Muestra los profesores cuyo salario supera el salario promedio de su mismo departamento.",
        "sql": """
SELECT i.name AS profesor,
       i.salary AS salario,
       i.dept_name AS departamento,
       ROUND(AVG(i2.salary), 2) AS promedio_depto
FROM instructor i
JOIN department d  ON i.dept_name  = d.dept_name
JOIN instructor i2 ON i2.dept_name = i.dept_name
GROUP BY i.ID, i.name, i.salary, i.dept_name
HAVING i.salary > AVG(i2.salary)
ORDER BY i.dept_name, i.salary DESC;
        """,
        "cypher": """
MATCH (i:Instructor)-[:PERTENECE_A]->(d:Department)
WITH d, avg(toFloat(i.salary)) AS promedio_depto
MATCH (i:Instructor)-[:PERTENECE_A]->(d)
WHERE toFloat(i.salary) > promedio_depto
RETURN i.name AS profesor,
       i.salary AS salario,
       d.dept_name AS departamento,
       round(promedio_depto, 2) AS promedio_depto
ORDER BY departamento, salario DESC;
        """,
    },

    "2": {
        "titulo": "Departamentos con profesores, salario promedio y presupuesto por profesor",
        "descripcion": "Calcula métricas por departamento.",
        "sql": """
SELECT d.dept_name AS departamento,
       d.budget AS presupuesto,
       COUNT(i.ID) AS num_profesores,
       ROUND(AVG(i.salary), 2) AS promedio_salario,
       ROUND(d.budget / COUNT(i.ID), 2) AS presupuesto_por_profesor
FROM department d
JOIN instructor i ON d.dept_name = i.dept_name
GROUP BY d.dept_name, d.budget
ORDER BY presupuesto_por_profesor DESC;
        """,
        "cypher": """
MATCH (d:Department)<-[:PERTENECE_A]-(i:Instructor)
WITH d,
     count(i) AS num_profesores,
     avg(toFloat(i.salary)) AS promedio_salario
RETURN d.dept_name AS departamento,
       d.budget AS presupuesto,
       num_profesores,
       round(promedio_salario, 2) AS promedio_salario,
       round(toFloat(d.budget) / num_profesores, 2) AS presupuesto_por_profesor
ORDER BY presupuesto_por_profesor DESC;
        """,
    },

    "3": {
        "titulo": "Profesores con más de una sección en un semestre",
        "descripcion": "Identifica profesores con múltiples secciones en el mismo periodo.",
        "sql": """
SELECT i.name AS profesor,
       t.semester AS semestre,
       t.year AS anio,
       COUNT(*) AS secciones
FROM teaches t
JOIN instructor i ON t.ID = i.ID
GROUP BY i.ID, i.name, t.semester, t.year
HAVING COUNT(*) > 1;
        """,
        "cypher": """
MATCH (i:Instructor)-[:TEACHES]->(sec:Section)
WITH i, sec.semester AS semestre, sec.year AS anio, count(sec) AS secciones
WHERE secciones > 1
RETURN i.name AS profesor, semestre, anio, secciones;
        """,
    },

    "4": {
        "titulo": "Cursos con prerrequisitos",
        "descripcion": "Cursos que requieren otros cursos.",
        "sql": """
SELECT c.course_id, c.title, p.title AS prereq
FROM course c
JOIN prereq pr ON c.course_id = pr.course_id
JOIN course p ON pr.prereq_id = p.course_id;
        """,
        "cypher": """
MATCH (c:Course)-[:REQUIERE]->(p:Course)
RETURN c.title AS curso, p.title AS prerequisito;
        """,
    },

    "5": {
        "titulo": "Departamentos sin profesores",
        "descripcion": "Departamentos sin instructores asociados.",
        "sql": """
SELECT d.dept_name
FROM department d
LEFT JOIN instructor i ON d.dept_name = i.dept_name
WHERE i.ID IS NULL;
        """,
        "cypher": """
MATCH (d:Department)
WHERE NOT (:Instructor)-[:PERTENECE_A]->(d)
RETURN d.dept_name;
        """,
    },

    "6": {
        "titulo": "Estudiantes y su asesor",
        "descripcion": "Muestra estudiantes con su asesor.",
        "sql": """
SELECT s.name, i.name AS asesor
FROM advisor a
JOIN student s ON a.s_ID = s.ID
JOIN instructor i ON a.i_ID = i.ID;
        """,
        "cypher": """
MATCH (i:Instructor)-[:ADVISES]->(s:Student)
RETURN s.name, i.name AS asesor;
        """,
    },

    "7": {
        "titulo": "Secciones 2009 con aula",
        "descripcion": "Secciones impartidas en 2009 con su aula.",
        "sql": """
SELECT sec.sec_id, c.title, cl.building
FROM section sec
JOIN course c ON sec.course_id = c.course_id
JOIN classroom cl ON sec.building = cl.building
WHERE sec.year = 2009;
        """,
        "cypher": """
MATCH (sec:Section)-[:ES_DE]->(c:Course),
      (sec)-[:SE_IMPARTE_EN]->(cl:Classroom)
WHERE sec.year = 2009
RETURN sec.sec_id, c.title, cl.building;
        """,
    },

    "8": {
        "titulo": "Cursos aprobados por estudiante",
        "descripcion": "Cursos donde la calificación no es F.",
        "sql": """
SELECT s.name, c.title
FROM takes t
JOIN student s ON t.ID = s.ID
JOIN course c ON t.course_id = c.course_id
WHERE t.grade <> 'F';
        """,
        "cypher": """
MATCH (s:Student)-[t:TAKES]->(sec:Section)-[:ES_DE]->(c:Course)
WHERE t.grade <> 'F'
RETURN s.name, c.title;
        """,
    },

    "9": {
        "titulo": "Profesores y estudiantes",
        "descripcion": "Relación profesor-estudiante.",
        "sql": """
SELECT i.name, s.name
FROM instructor i
JOIN teaches t ON i.ID = t.ID
JOIN takes tk ON t.course_id = tk.course_id
JOIN student s ON tk.ID = s.ID;
        """,
        "cypher": """
MATCH (i:Instructor)-[:TEACHES]->(sec:Section)<-[:TAKES]-(s:Student)
RETURN i.name, s.name;
        """,
    },

    "10": {
        "titulo": "Cursos nunca tomados",
        "descripcion": "Cursos sin estudiantes.",
        "sql": """
SELECT c.title
FROM course c
LEFT JOIN takes t ON c.course_id = t.course_id
WHERE t.ID IS NULL;
        """,
        "cypher": """
MATCH (c:Course)
WHERE NOT EXISTS {
    MATCH (c)<-[:ES_DE]-(sec:Section)<-[:TAKES]-(:Student)
}
RETURN c.title;
        """,
    },
}


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

    print("\nDescripción:")
    print(consulta["descripcion"])

    print("\nSQL:")
    print(consulta["sql"])
    filas_sql = ejecutar_sql(consulta["sql"])
    print("\nResultado SQL:")
    mostrar_filas(filas_sql)
    print(f"Total SQL: {len(filas_sql)}")

    print("\nCypher:")
    print(consulta["cypher"])
    filas_cypher = ejecutar_cypher(cliente, consulta["cypher"])
    print("\nResultado Cypher:")
    mostrar_filas(filas_cypher)
    print(f"Total Cypher: {len(filas_cypher)}")

    if len(filas_sql) == len(filas_cypher):
        print("\n✔ Resultados consistentes")
    else:
        print("\n⚠ Diferencia en resultados")

    cliente.cerrar()


def mostrar_menu_consultas():
    while True:
        print("\n=== MENÚ ===")
        for k, v in CONSULTAS.items():
            print(f"{k}. {v['titulo']}")
        print("0. Salir")

        opcion = input("Opción: ")

        if opcion == "0":
            break
        if opcion not in CONSULTAS:
            print("Opción inválida")
            continue

        ejecutar_consulta(opcion)
        input("\nEnter para continuar...")