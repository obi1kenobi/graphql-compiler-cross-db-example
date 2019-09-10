from graphql import parse
from graphql.utils.schema_printer import print_schema
from graphql_compiler.schema_transformation.merge_schemas import (
    CrossSchemaEdgeDescriptor, FieldReference, merge_schemas,
)
from graphql_compiler.schema_transformation.split_query import split_query
from graphql_compiler.schema_transformation.query_plan import (
    execute_query_plan, make_query_plan
)

from demo.server import orientdb_query, postgres_query


def make_merged_schema_descriptor(orientdb_schema, orientdb_type_equivalence_hints,
                                  postgres_schema, postgres_type_equivalence_hints):
    merged_type_equivalence_hints = dict(postgres_type_equivalence_hints, **orientdb_type_equivalence_hints)

    schema_id_to_ast = {
        'orientdb': parse(print_schema(orientdb_schema)),
        'postgres': parse(print_schema(postgres_schema)),
    }

    cross_schema_edges = [
        CrossSchemaEdgeDescriptor(
            edge_name='Airport_BasedIn',
            outbound_field_reference=FieldReference(
                schema_id='postgres',
                type_name='Airport',
                field_name='alpha2_country',
            ),
            inbound_field_reference=FieldReference(
                schema_id='orientdb',
                type_name='Country',
                field_name='alpha2',
            ),
            out_edge_only=False,
        ),
        CrossSchemaEdgeDescriptor(
            edge_name='Airline_RegisteredIn',
            outbound_field_reference=FieldReference(
                schema_id='postgres',
                type_name='Airline',
                field_name='alpha2_country',
            ),
            inbound_field_reference=FieldReference(
                schema_id='orientdb',
                type_name='Country',
                field_name='alpha2',
            ),
            out_edge_only=False,
        )
    ]

    return merge_schemas(schema_id_to_ast, cross_schema_edges,
                         type_equivalence_hints=merged_type_equivalence_hints)


def execute_cross_db_query(orientdb_info, postgres_info, merged_schema_descriptor,
                           cross_db_query, cross_db_args):
    orientdb_schema, orientdb_type_equivalence_hints = orientdb_info
    schema_id_to_execution_func = {
        'orientdb': (
            lambda query, args: orientdb_query.execute_graphql_query(
                orientdb_schema, query, args,
                type_equivalence_hints=orientdb_type_equivalence_hints
            )[1]
        ),
        'postgres': (
            lambda query, args: postgres_query.execute_graphql_query(
                postgres_info, query, args
            )[1]
        ),
    }

    split_result = split_query(parse(cross_db_query), merged_schema_descriptor, strict=False)
    query_plan = make_query_plan(*split_result)

    return query_plan, execute_query_plan(schema_id_to_execution_func, query_plan, cross_db_args)
