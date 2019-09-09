from graphql_compiler import get_sqlalchemy_schema_info_from_specified_metadata, graphql_to_sql
from graphql_compiler.schema_generation.sqlalchemy.edge_descriptors import DirectEdgeDescriptor
from sqlalchemy import MetaData, dialects

from demo.server.config import sqlalchemy_engine


def get_postgres_schema_info():
    """Return a SQLAlchemySchemaInfo object for use with the GraphQL compiler."""
    metadata = MetaData(bind=sqlalchemy_engine)
    metadata.reflect()

    vertex_name_to_table = metadata.tables

    direct_edges = {
        'FlightRoute_FromAirport': DirectEdgeDescriptor(
            from_vertex='FlightRoute',
            from_column='source_airport_id',
            to_vertex='Airport',
            to_column='id',
        ),
        'FlightRoute_ToAirport': DirectEdgeDescriptor(
            from_vertex='FlightRoute',
            from_column='destination_airport_id',
            to_vertex='Airport',
            to_column='id',
        ),
        'FlightRoute_OperatingAirline': DirectEdgeDescriptor(
            from_vertex='FlightRoute',
            from_column='airline_id',
            to_vertex='Airline',
            to_column='id',
        ),
    }

    sql_schema_info = get_sqlalchemy_schema_info_from_specified_metadata(
        vertex_name_to_table, direct_edges, dialects.postgresql.dialect())
    return sql_schema_info


def execute_graphql_query(sql_schema_info, graphql_query, graphql_args, limit=1000):
    compilation_result = graphql_to_sql(sql_schema_info, graphql_query, graphql_args)

    result_proxy = sqlalchemy_engine.execute(compilation_result.query)
    try:
        if limit is None:
            fetched_results = result_proxy.fetchall()
        else:
            fetched_results = result_proxy.fetchmany(size=limit)

        outputs = [
            dict(row)
            for row in fetched_results
        ]

        return compilation_result, outputs
    finally:
        result_proxy.close()
