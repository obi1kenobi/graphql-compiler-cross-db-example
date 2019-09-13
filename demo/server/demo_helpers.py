from collections import OrderedDict

from graphql.language.printer import print_ast
from IPython.display import HTML, display
from tabulate import tabulate

from graphql_compiler.macros import create_macro_registry

from demo.server import orientdb_query, postgres_query
from demo.server.cross_db_query import execute_cross_db_query, make_merged_schema_descriptor
from demo.server.orientdb_query import get_orientdb_graphql_schema_and_equivalence_hints
from demo.server.postgres_query import get_postgres_schema_info


def pretty_print_data(data):
    sorted_column_order = [
        OrderedDict(sorted(row.items(), key=lambda x: x[0]))
        for row in data
    ]

    display(HTML(tabulate(
        sorted_column_order, headers='keys', tablefmt='html', showindex="always")))


orientdb_info = get_orientdb_graphql_schema_and_equivalence_hints()
orientdb_schema, orientdb_type_equivalence_hints = orientdb_info
postgres_info = get_postgres_schema_info()
postgres_schema = postgres_info.schema
postgres_type_equivalence_hints = postgres_info.type_equivalence_hints

merged_type_equivalence_hints = dict(
    postgres_type_equivalence_hints, **orientdb_type_equivalence_hints)

merged_schema_descriptor = make_merged_schema_descriptor(
    orientdb_schema, orientdb_type_equivalence_hints,
    postgres_schema, postgres_type_equivalence_hints)


def get_schema():
    return print_ast(merged_schema_descriptor.schema_ast)


def get_empty_macro_registry():
    return create_macro_registry(
        merged_schema_descriptor.schema,
        type_equivalence_hints=merged_type_equivalence_hints)


def execute_query(query, args):
    query_plan, results = execute_cross_db_query(
        orientdb_info, postgres_info, merged_schema_descriptor, query, args)
    return query_plan, results


def set_verbose_mode(value):
    orientdb_query.verbose = value
    postgres_query.verbose = value
