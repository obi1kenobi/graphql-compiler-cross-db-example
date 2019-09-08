from glob import glob
from os import path

from demo.server.config import get_graph_client


def apply_orientdb_schema():
    graph = get_graph_client()

    comment_char = '#'
    demo_root = path.dirname(path.dirname(path.abspath(__file__)))
    sql_files = glob(path.join(demo_root, "orientdb_schema/*.sql"))

    for schema_file in sorted(sql_files):
        with open(schema_file, "r") as update_file:
            for line in update_file:
                command = line.strip()
                if not command or command.startswith(comment_char):
                    continue

                graph.client.command(command)


if __name__ == '__main__':
    apply_orientdb_schema()
