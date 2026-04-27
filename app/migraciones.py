"""
migraciones.py
Migra los datos de MySQL a Neo4j respetando únicamente las relaciones definidas por FK en el DDL.
"""

import sys

from app.cliente_mysql import (
    obtener_departamentos,
    obtener_salones,
    obtener_horarios,
    obtener_cursos,
    obtener_profesores,
    obtener_estudiantes,
    obtener_secciones,
    obtener_imparticiones,
    obtener_inscripciones,
    obtener_asesorias,
    obtener_prerrequisitos,
)
from app.cliente_neo4j import ClienteNeo4j


def migrar_nodos(cliente: ClienteNeo4j):
    print("► Migrando nodos...")

    for fila in obtener_departamentos():
        cliente.ejecutar_escritura(
            "MERGE (d:Department {dept_name: $dept_name}) "
            "SET d.building = $building, d.budget = $budget",
            fila,
        )

    for fila in obtener_salones():
        cliente.ejecutar_escritura(
            "MERGE (s:Classroom {building: $building, room_number: $room_number}) "
            "SET s.capacity = $capacity",
            fila,
        )

    horarios = {}
    for fila in obtener_horarios():
        id_horario = fila["time_slot_id"]
        horarios.setdefault(id_horario, []).append({
            "day": fila["day"],
            "start_hr": fila["start_hr"],
            "start_min": fila["start_min"],
            "end_hr": fila["end_hr"],
            "end_min": fila["end_min"],
        })

    for id_horario, bloques in horarios.items():
        cliente.ejecutar_escritura(
            "MERGE (h:TimeSlot {time_slot_id: $id_horario}) "
            "SET h.bloques = $bloques",
            {"id_horario": id_horario, "bloques": str(bloques)},
        )

    for fila in obtener_cursos():
        cliente.ejecutar_escritura(
            "MERGE (c:Course {course_id: $course_id}) "
            "SET c.title = $title, c.credits = $credits, c.dept_name = $dept_name",
            fila,
        )

    for fila in obtener_profesores():
        cliente.ejecutar_escritura(
            "MERGE (p:Instructor {ID: $ID}) "
            "SET p.name = $name, p.salary = $salary, p.dept_name = $dept_name",
            fila,
        )

    for fila in obtener_estudiantes():
        cliente.ejecutar_escritura(
            "MERGE (e:Student {ID: $ID}) "
            "SET e.name = $name, e.tot_cred = $tot_cred, e.dept_name = $dept_name",
            fila,
        )

    for fila in obtener_secciones():
        cliente.ejecutar_escritura(
            "MERGE (sec:Section {course_id: $course_id, sec_id: $sec_id, semester: $semester, year: $year}) "
            "SET sec.building = $building, sec.room_number = $room_number, sec.time_slot_id = $time_slot_id",
            fila,
        )

    print("  ok nodos creados")


def migrar_relaciones(cliente: ClienteNeo4j):
    print("► Migrando relaciones...")

    for fila in obtener_cursos():
        if fila.get("dept_name"):
            cliente.ejecutar_escritura(
                "MATCH (c:Course {course_id: $course_id}), (d:Department {dept_name: $dept_name}) "
                "MERGE (c)-[:PERTENECE_A]->(d)",
                fila,
            )

    for fila in obtener_profesores():
        if fila.get("dept_name"):
            cliente.ejecutar_escritura(
                "MATCH (p:Instructor {ID: $ID}), (d:Department {dept_name: $dept_name}) "
                "MERGE (p)-[:PERTENECE_A]->(d)",
                fila,
            )

    for fila in obtener_secciones():
        cliente.ejecutar_escritura(
            "MATCH (sec:Section {course_id: $course_id, sec_id: $sec_id, semester: $semester, year: $year}), "
            "      (c:Course {course_id: $course_id}) "
            "MERGE (sec)-[:ES_DE]->(c)",
            fila,
        )

    for fila in obtener_secciones():
        if fila.get("building") and fila.get("room_number"):
            cliente.ejecutar_escritura(
                "MATCH (sec:Section {course_id: $course_id, sec_id: $sec_id, semester: $semester, year: $year}), "
                "      (s:Classroom {building: $building, room_number: $room_number}) "
                "MERGE (sec)-[:SE_IMPARTE_EN]->(s)",
                fila,
            )

    for fila in obtener_imparticiones():
        cliente.ejecutar_escritura(
            "MATCH (p:Instructor {ID: $ID}), "
            "      (sec:Section {course_id: $course_id, sec_id: $sec_id, semester: $semester, year: $year}) "
            "MERGE (p)-[:TEACHES]->(sec)",
            fila,
        )

    for fila in obtener_inscripciones():
        cliente.ejecutar_escritura(
            "MATCH (e:Student {ID: $ID}), "
            "      (sec:Section {course_id: $course_id, sec_id: $sec_id, semester: $semester, year: $year}) "
            "MERGE (e)-[r:TAKES]->(sec) "
            "SET r.grade = $grade",
            fila,
        )

    for fila in obtener_asesorias():
        cliente.ejecutar_escritura(
            "MATCH (p:Instructor {ID: $i_ID}), (e:Student {ID: $s_ID}) "
            "MERGE (p)-[:ADVISES]->(e)",
            fila,
        )

    for fila in obtener_prerrequisitos():
        cliente.ejecutar_escritura(
            "MATCH (c:Course {course_id: $course_id}), (pre:Course {course_id: $prereq_id}) "
            "MERGE (c)-[:REQUIERE]->(pre)",
            fila,
        )

    print("  ok relaciones creadas")


def ejecutar_migracion(limpiar: bool = False):
    cliente = ClienteNeo4j()
    try:
        if limpiar:
            print("► Limpiando base de datos Neo4j...")
            cliente.limpiar_base()
        cliente.crear_restricciones()
        migrar_nodos(cliente)
        migrar_relaciones(cliente)
        print("Migración completa")
    finally:
        cliente.cerrar()


if __name__ == "__main__":
    ejecutar_migracion(limpiar="--clear" in sys.argv or "--limpiar" in sys.argv)
