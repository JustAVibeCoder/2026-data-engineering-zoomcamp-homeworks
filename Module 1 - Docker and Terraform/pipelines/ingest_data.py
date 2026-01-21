import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import click


year = 2021
month = 1


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
link = f'{prefix}yellow_tripdata_{year}-{month:02d}.csv.gz'


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}


parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
@click.option('--table-name', default='yellow_taxi_data', help='Table name in PostgreSQL')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')

def ingest(pg_user, pg_pass, pg_host, pg_port, pg_db, table_name, chunksize):
    """Ingest NYC taxi data into PostgreSQL database."""
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_iter = pd.read_csv(
        prefix + 'yellow_tripdata_2021-01.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize 
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.to_sql(name=table_name, con=engine, if_exists='replace')
            print(len(df_chunk))
        else:
            df_chunk.to_sql(name=table_name, con=engine, if_exists='append')
            print(len(df_chunk))
        first = False


if __name__ == '__main__':
    ingest()
    
