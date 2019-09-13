from demo.data_loading.apply_orientdb_schema import apply_orientdb_schema
from demo.data_loading.apply_postgres_schema import apply_postgres_schema
from demo.data_loading.orientdb_loading import orientdb_load_all
from demo.data_loading.postgres_loading import postgres_load_all


def run_all():
    print('Applying Postgres schema...')
    apply_postgres_schema()
    print('Downloading data and writing it into Postgres, this will take a few minutes.')
    print('  Please make sure you remain connected to the internet.')
    postgres_load_all()

    print('\nApplying OrientDB schema...')
    apply_orientdb_schema()
    print('Downloading data and writing it into OrientDB, this will take a few minutes.')
    print('  Please make sure you remain connected to the internet.')
    orientdb_load_all()

    print('\nAll done!')


if __name__ == '__main__':
    run_all()
