from demo.pg_models import Airline, Airport, FlightRoute
from demo.data_loading.fixes import (
    fix_alpha2_value, fix_iata_or_icao_code, hardcoded_alpha2_values
)
from demo.data_loading.data_fetching import (
    get_airlines_data, get_airports_data, get_countries_data, get_flight_routes_data
)
from demo.server.config import sqlalchemy_session


def _get_alpha2_for_country_name(countries_df, country_name):
    alpha2 = hardcoded_alpha2_values.get(country_name, None)
    if alpha2 is None:
        matches = countries_df[
            countries_df['official_name_en'] == country_name]
        if len(matches) == 1:
            matching_row = next(matches.iterrows())[1]
            alpha2 = matching_row['ISO3166-1-Alpha-2']

    return fix_alpha2_value(alpha2)


def load_airlines(airlines_df, countries_df):
    for _, airline_item in airlines_df.iterrows():
        with sqlalchemy_session() as session:
            alpha2 = _get_alpha2_for_country_name(countries_df, airline_item['country'])
            airline = Airline(
                id=airline_item['id'],
                name=airline_item['name'],
                iata_code=fix_iata_or_icao_code(airline_item['iata_code']),
                icao_code=fix_iata_or_icao_code(airline_item['icao_code']),
                callsign=airline_item['callsign'],
                alpha2_country=alpha2,
            )
            session.add(airline)


def load_airports(airports_df, countries_df):
    for _, airport_item in airports_df.iterrows():
        with sqlalchemy_session() as session:
            alpha2 = _get_alpha2_for_country_name(countries_df, airport_item['country'])
            airport = Airport(
                id=airport_item['id'],
                name=airport_item['name'],
                city_served=airport_item['city'],
                alpha2_country=alpha2,
                iata_code=fix_iata_or_icao_code(airport_item['iata_code']),
                icao_code=fix_iata_or_icao_code(airport_item['icao_code']),
                elevation_ft=airport_item['altitude'],
            )
            session.add(airport)


def load_flight_routes(flight_routes_df, airlines_df, airports_df):
    airline_ids = {
        airline_item['id']
        for _, airline_item in airlines_df.iterrows()
    }
    airport_ids = {
        airport_item['id']
        for _, airport_item in airports_df.iterrows()
    }

    for index, flight_route_item in flight_routes_df.iterrows():
        if any((
            flight_route_item['airline_id'] not in airline_ids,
            flight_route_item['source_airport_id'] not in airport_ids,
            flight_route_item['destination_airport_id'] not in airport_ids,
        )):
            # Bad data, we don't have the matching airline or airports.
            continue

        with sqlalchemy_session() as session:
            flight_route = FlightRoute(
                id=index,
                airline_id=flight_route_item['airline_id'],
                source_airport_id=flight_route_item['source_airport_id'],
                destination_airport_id=flight_route_item['destination_airport_id'],
                stops=flight_route_item['stops'],
            )
            session.add(flight_route)


if __name__ == '__main__':
    airlines_df = get_airlines_data()
    airports_df = get_airports_data()
    flight_routes_df = get_flight_routes_data()
    countries_df = get_countries_data()

    load_airlines(airlines_df, countries_df)
    load_airports(airports_df, countries_df)
    load_flight_routes(flight_routes_df, airlines_df, airports_df)
