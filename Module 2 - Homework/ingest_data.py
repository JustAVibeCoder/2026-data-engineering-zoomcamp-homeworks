import pandas as pd
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='postgres', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
@click.option('--zones-table-name', default='taxi_zones', help='Table name in PostgreSQL')
@click.option('--data-table-name', default='yellow_taxi_data', help='Table name in PostgreSQL')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')



def run(pg_user, pg_pass, pg_host, pg_port, pg_db, zones_table_name, data_table_name, chunksize):
    
    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    ds = pd.read_csv("https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv")

    # ds = pd.read_parquet("green_tripdata_2025-11.parquet")

    ds.to_sql(
        name=zones_table_name,
        con=engine,
        schema="public",      # default schema in Postgres
        if_exists="replace",  # "append" in real pipelines
        index=False,
        method="multi",       # faster inserts
        chunksize=chunksize
    )

    ds = pd.read_parquet("https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet")

    # ds = pd.read_parquet("green_tripdata_2025-11.parquet")

    ds.to_sql(
        name=data_table_name,
        con=engine,
        schema="public",      # default schema in Postgres
        if_exists="replace",  # "append" in real pipelines
        index=False,
        method="multi",       # faster inserts
        chunksize=1000
    )


if __name__ == '__main__':
    run()
    