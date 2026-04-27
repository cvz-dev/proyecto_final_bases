from config import MYSQL_CONFIG, NEO4J_CONFIG
import mysql.connector
from neo4j import GraphDatabase


def test_mysql():
    print("Probando conexión a MySQL...")

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE();")
    db = cursor.fetchone()

    print(f"Conexión MySQL correcta. Base activa: {db[0]}")

    cursor.close()
    conn.close()


def test_neo4j():
    print("Probando conexión a Neo4j...")

    driver = GraphDatabase.driver(
        NEO4J_CONFIG["uri"],
        auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"])
    )

    driver.verify_connectivity()

    with driver.session() as session:
        result = session.run("RETURN 'Conexión Neo4j correcta' AS mensaje")
        print(result.single()["mensaje"])

    driver.close()


if __name__ == "__main__":
    test_mysql()
    test_neo4j()
