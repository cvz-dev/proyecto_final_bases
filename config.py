import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_MYSQL = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE", "university"),
}

CONFIG_NEO4J = {
    "uri": os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687"),
    "usuario": os.getenv("NEO4J_USER", "neo4j"),
    "contrasena": os.getenv("NEO4J_PASSWORD"),
    "database": os.getenv("NEO4J_DATABASE", "neo4j"),
}
