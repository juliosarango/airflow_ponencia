from airflow import DAG
from airflow.models import Variable
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_sftp import S3ToSFTPOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.operators.email import EmailOperator
from pendulum import duration
import os

from datetime import datetime

email_notificacion = Variable.get("email_notificacion")

BUCKET_KEY = "reporte.csv"
BUCKET_NAME = "s3-sensor-js"

default_args = {
    "start_date": datetime(2024, 9, 12),
    "retries": 3,
    "retry_delay": duration(seconds=2),
    "email": [email_notificacion],
    "email_on_failure": True,
}

with DAG(
    dag_id="sensor_archivos",
    schedule_interval="*/5 * * * *",
    default_args=default_args,
    catchup=False,
) as dag:

    sensor_aws_s3 = S3KeySensor(
        bucket_key=f"{BUCKET_KEY}",
        bucket_name=f"{BUCKET_NAME}",
        task_id="sensor_one_key",
        aws_conn_id="aws_default",
    )

    descargar_from_s3 = S3ToSFTPOperator(
        task_id="descargar_from_s3",
        s3_bucket=f"{BUCKET_NAME}",
        s3_key=f"{BUCKET_KEY}",
        sftp_path=f"/tmp/{BUCKET_KEY}",
        sftp_conn_id="conn_user_postgres",
        aws_conn_id="aws_default",
    )

    cargar_datos_postgres = PostgresOperator(
        task_id="cargar_datos_postgres",
        sql="""                       
            create or replace function fn_cargar_datos()
            returns void
            language plpgsql
            as
            $$
            declare
            film_count integer;
            begin
            create table if not exists reporte(
                    id serial not null,
                    nombre varchar(100) not null,
                    apellido varchar(100) not null,
                    departamento varchar(50) not null,
                    valor_ventas float not null,
                    fecha_venta date,
                    fecha_registro timestamp without time zone default now(),
                    constraint pk_reporte primary key (id)
                );

                COPY reporte(nombre, apellido, departamento, valor_ventas, fecha_venta)
                FROM '/tmp/reporte.csv'
                DELIMITER ','
                CSV HEADER;
                
            end;
            $$;
            select fn_cargar_datos();
        """,
        postgres_conn_id="conn_bd_postgres",
        autocommit=True,
    )

    notificacion_email = EmailOperator(
        task_id="notificacion_email",
        to="jsarangoq@gmail.com",
        subject="Reporte cargado correctamente!!",
        html_content="<p>El reporte ha sido cargado correctamente en la BD</p>",
    )

    sensor_aws_s3 >> descargar_from_s3 >> cargar_datos_postgres >> notificacion_email
