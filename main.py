"""
main.py — punto de entrada del proyecto MySQL a Neo4j

Uso:
  python main.py migrar --limpiar   # limpia Neo4j y migra datos
  python main.py consultas          # abre menú interactivo de consultas
  python main.py todo --limpiar     # migra y luego abre el menú
"""

import sys


def main():
    comando = sys.argv[1] if len(sys.argv) > 1 else "consultas"

    if comando in ["migrar", "migrate"]:
        from app.migraciones import ejecutar_migracion
        ejecutar_migracion(limpiar="--limpiar" in sys.argv or "--clear" in sys.argv)

    elif comando in ["consultas", "comparar", "compare", "menu"]:
        from app.ejecutor_consultas import mostrar_menu_consultas
        mostrar_menu_consultas()

    elif comando in ["todo", "all"]:
        from app.migraciones import ejecutar_migracion
        from app.ejecutor_consultas import mostrar_menu_consultas
        ejecutar_migracion(limpiar="--limpiar" in sys.argv or "--clear" in sys.argv)
        mostrar_menu_consultas()

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
