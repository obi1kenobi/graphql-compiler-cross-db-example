from graphql import GraphQLID
from graphql_compiler import graphql_to_match
from graphql_compiler.schema_generation.orientdb.schema_graph_builder import (
    get_orientdb_schema_graph
)
from graphql_compiler.schema_generation.orientdb.utils import (
    ORIENTDB_INDEX_RECORDS_QUERY, ORIENTDB_SCHEMA_RECORDS_QUERY
)
from graphql_compiler.schema_generation.graphql_schema import get_graphql_schema_from_schema_graph

from demo.server.config import get_pyorient_client


def get_orientdb_graphql_schema_and_equivalence_hints():
    """Return a tuple (GraphQLSchema, type_equivalence_hints) for use with the GraphQL compiler."""
    graph_client = get_pyorient_client()
    try:
        schema_records = graph_client.client.command(ORIENTDB_SCHEMA_RECORDS_QUERY)
        schema_data = [record.oRecordData for record in schema_records]

        index_records = graph_client.client.command(ORIENTDB_INDEX_RECORDS_QUERY)
        index_query_data = [record.oRecordData for record in index_records]

        schema_graph = get_orientdb_schema_graph(schema_data, index_query_data)

        overrides = {
            'GeographicArea': {
                'uuid': GraphQLID,
            }
        }
        hidden_classes = frozenset({
            # Don't include OrientDB's built-in base vertex class in the schema.
            'V',
        })

        return get_graphql_schema_from_schema_graph(
            schema_graph, class_to_field_type_overrides=overrides, hidden_classes=hidden_classes)
    finally:
        graph_client.client.close()


def execute_graphql_query(schema, graphql_query, graphql_args,
                          type_equivalence_hints=None, limit=1000):
    """Execute the provided GraphQL query and return the compilation result and resulting data."""
    graph_client = get_pyorient_client()
    try:
        compilation_result = graphql_to_match(
            schema, graphql_query, graphql_args,
            type_equivalence_hints=type_equivalence_hints)

        outputs = [
            x.oRecordData
            for x in graph_client.client.command(compilation_result.query, limit)
        ]

        return compilation_result, outputs
    finally:
        graph_client.client.close()
