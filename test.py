from app.cliente_mysql import obtener_conexion
from app.cliente_neo4j import ClienteNeo4j


def probar_mysql():
    print("Probando conexión con MySQL...")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT DATABASE();")
    base_datos = cursor.fetchone()[0]

    cursor.execute("SHOW TABLES;")
    tablas = cursor.fetchall()

    cursor.close()
    conexion.close()

    print(f"Conexión MySQL correcta. Base activa: {base_datos}")
    print(f"Tablas encontradas: {len(tablas)}")


def probar_neo4j():
    print("\nProbando conexión con Neo4j...")

    cliente = ClienteNeo4j()

    resultado = cliente.ejecutar_lectura("""
        RETURN 'Conexión Neo4j correcta' AS mensaje
    """)

    cliente.cerrar()

    print(resultado[0]["mensaje"])


if __name__ == "__main__":
    probar_mysql()
    probar_neo4j()