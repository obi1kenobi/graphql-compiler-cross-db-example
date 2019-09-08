import pandas as pd


airports_url = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
airlines_url = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat'
flight_routes_url = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat'
countries_url = (
    'https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv'
)


# All of these values exist as placeholders for unknown or missing data.
data_replacements = {
    '\\N': None,
    '': None,
    ' ': None,
    '-': None,
    float('nan'): None,
}


def get_airports_data():
    airports_df = pd.read_csv(
        airports_url, header=None,
        names=('id', 'name', 'city', 'country', 'iata_code', 'icao_code',
               'latitude', 'longitude', 'altitude',
               'utc_offset_hours', 'daylight_savings', 'timezone_name',
               'airport_type', 'source'))
    airports_df.replace(to_replace=data_replacements, inplace=True)
    return airports_df


def get_airlines_data():
    airlines_df = pd.read_csv(
        airlines_url, header=None,
        names=('id', 'name', 'alias', 'iata_code', 'icao_code', 'callsign', 'country', 'active'))
    airlines_df.replace(to_replace=data_replacements, inplace=True)
    return airlines_df


def get_flight_routes_data():
    flight_routes_df = pd.read_csv(
        flight_routes_url, header=None,
        names=('airline', 'airline_id', 'source_airport', 'source_airport_id',
               'destination_airport', 'destination_airport_id', 'codeshare', 'stops', 'equipment'))
    flight_routes_df.replace(to_replace=data_replacements, inplace=True)
    return flight_routes_df


def get_countries_data():
    raw_countries_df = pd.read_csv(countries_url)
    raw_countries_df.replace(to_replace=data_replacements, inplace=True)

    countries_columns = [
        'ISO3166-1-Alpha-3',
        'ISO3166-1-Alpha-2',
        'Sub-region Name',
        'Intermediate Region Name',
        'official_name_en',
        'Region Name',
    ]
    raw_countries_df = raw_countries_df[countries_columns]
    countries_with_no_name = pd.isnull(raw_countries_df['official_name_en'])
    countries_df = raw_countries_df.drop(raw_countries_df[countries_with_no_name].index)
    return countries_df
