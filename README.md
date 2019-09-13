# GraphQL compiler cross-database querying demo

A demo of the GraphQL compiler's cross-database querying capabilities.

The demo uses a dataset of countries, geographical regions, airports, airlines, and flights.
The data originates from the following open datasets:
- [OpenFlights](https://github.com/jpatokal/openflights)
- [Core Data's country codes dataset](https://github.com/datasets/country-codes)

To get started, you'll need `docker-compose`, Python 3.6+, and `pipenv` installed.

Get started by running the following from the root directory of the repository:
```bash
# Start the Postgres and OrientDB containers.
docker-compose up -d

# Set up all required Python libraries.
pipenv install --python="$(which python3)"
pipenv shell
```

Then, after Pipenv has created your new shell with the required Python dependencies,
run the following inside it:
```bash
# Load the demo datasets into the databases.
# If this step fails, then tear down the database containers
# with "docker-compose down" and start from the top.
python -m demo.bootstrap

# Start the Jupyter lab environment and open any of the notebooks to play around.
# 01_intro_demo and 02_macro_edges have pre-written queries for you to try running.
jupyter lab
```



