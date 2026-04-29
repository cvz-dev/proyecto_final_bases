from neo4j import GraphDatabase
from config import CONFIG_NEO4J


class ClienteNeo4j:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            CONFIG_NEO4J["uri"],
            auth=(CONFIG_NEO4J["usuario"], CONFIG_NEO4J["contrasena"]),
        )

    def cerrar(self):
        self._driver.close()

    def ejecutar_lectura(self, consulta, parametros):
        with self._driver.session(database=CONFIG_NEO4J["database"]) as sesion:
            resultado = sesion.run(consulta, parametros or {})
            return resultado.data()
            
    def ejecutar(self, consulta, parametros):
        return self.ejecutar_lectura(consulta, parametros)

    def ejecutar_escritura(self, consulta, parametros):
        with self._driver.session(database=CONFIG_NEO4J["database"]) as sesion:
            sesion.execute_write(lambda tx: tx.run(consulta, parametros or {}))

    def limpiar_base(self):
        """Elimina todos los nodos y relaciones. Útil para repetir la migración."""
        self.ejecutar_lectura("MATCH (n) DETACH DELETE n")

    def crear_restricciones(self):
        """Crea restricciones de unicidad para evitar nodos duplicados."""
        restricciones = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Department) REQUIRE d.dept_name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Course) REQUIRE c.course_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Instructor) REQUIRE i.ID IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Student) REQUIRE s.ID IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (r:Classroom) REQUIRE (r.building, r.room_number) IS NODE KEY",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (sec:Section) REQUIRE (sec.course_id, sec.sec_id, sec.semester, sec.year) IS NODE KEY",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (h:TimeSlot) REQUIRE h.time_slot_id IS UNIQUE",
        ]
        for restriccion in restricciones:
            self.ejecutar_lectura(restriccion)
