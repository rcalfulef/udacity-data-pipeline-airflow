# pylint: disable=pointless-statement
""" Udacity final project dag file. """
from datetime import datetime, timedelta
import os
from airflow.decorators import dag

from airflow.operators.dummy_operator import DummyOperator
from operators.data_quality import DataQualityOperator

from operators.load_dimension import LoadDimensionOperator
from operators.load_fact import LoadFactOperator
from operators.stage_redshift import StageToRedshiftOperator
from airflow.operators.postgres_operator import PostgresOperator

from helpers.sql_create_tables import create_table_queries, drop_table_queries
from helpers.sql_queries import SqlQueries


default_args = {
    "owner": "Andrés Calfulef",
    "depends_on_past": False,
    "start_date": datetime.now(),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
    "email_on_retry": False,
}


@dag(
    default_args=default_args,
    description="Load and transform data in Redshift with Airflow",
    schedule_interval="@hourly",
)
def final_project():
    """Final project dag"""
    start_operator = DummyOperator(task_id="Begin_execution")

    drop_tables = PostgresOperator(
        task_id="Drop_tables",
        postgres_conn_id="redshift",
        sql=list(drop_table_queries),
    )
    create_tables = PostgresOperator(
        task_id="Create_tables",
        postgres_conn_id="redshift",
        sql=list(create_table_queries),
    )

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id="Stage_events",
        table="staging_events",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="airflow-s3-andres-udacity",
        s3_key="log-data",
        json_path="s3://airflow-s3-andres-udacity/log_json_path.json",
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id="Stage_songs",
        table="staging_songs",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="airflow-s3-andres-udacity",
        s3_key="song-data",
        json_path="auto",
    )

    load_songplays_table = LoadFactOperator(
        task_id="Load_songplays_fact_table",
        redshift_conn_id="redshift",
        table="songplays",
        sql=SqlQueries.songplay_table_insert,
        append_data=False,
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id="Load_user_dim_table",
        redshift_conn_id="redshift",
        table="users",
        sql=SqlQueries.user_table_insert,
        append_data=False,
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id="Load_song_dim_table",
        redshift_conn_id="redshift",
        table="songs",
        sql=SqlQueries.song_table_insert,
        append_data=False,
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id="Load_artist_dim_table",
        redshift_conn_id="redshift",
        table="artists",
        sql=SqlQueries.artist_table_insert,
        append_data=False,
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id="Load_time_dim_table",
        redshift_conn_id="redshift",
        table="time",
        sql=SqlQueries.time_table_insert,
        append_data=False,
    )

    run_quality_checks = DataQualityOperator(
        task_id="Run_data_quality_checks",
        redshift_conn_id="redshift",
        tables=["songplays", "songs", "artists", "time", "users"],
    )

    end_operator = DummyOperator(task_id="End_execution")

    start_operator >> drop_tables

    # Drop tables
    drop_tables >> create_tables

    # Create tables
    create_tables >> stage_events_to_redshift
    create_tables >> stage_songs_to_redshift

    stage_events_to_redshift >> load_songplays_table
    stage_songs_to_redshift >> load_songplays_table

    load_songplays_table >> load_user_dimension_table
    load_songplays_table >> load_song_dimension_table
    load_songplays_table >> load_artist_dimension_table
    load_songplays_table >> load_time_dimension_table

    load_user_dimension_table >> run_quality_checks
    load_song_dimension_table >> run_quality_checks
    load_artist_dimension_table >> run_quality_checks
    load_time_dimension_table >> run_quality_checks

    run_quality_checks >> end_operator


final_project_dag = final_project()
