from airflow import DAG
from airflow.models import Variable
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_sftp import S3ToSFTPOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.S3_hook import S3Hook
from pendulum import duration
import os

from datetime import datetime

email_notificacion = Variable.get("email_notificacion")

def download_file_s3():
    aws_hook = S3Hook("aws_default")
    file_s3 =aws_hook.download_file(
        key="prueba_1.pdf",
        bucket_name="s3-sensor-js",
    )

    return file_s3

def rename_file_s3(ti, new_name: str):
    list_of_args = ti.xcom_pull(task_ids=['download_file_s3'])
    downloaded_file_name = list_of_args[0]
    downloaded_file_path = '/'.join(downloaded_file_name.split('/')[:-1])
    new_name_for_file = f'{downloaded_file_path}/{new_name}'
    os.rename(src=downloaded_file_name, dst=new_name_for_file)

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
        bucket_key="reporte.csv",
        bucket_name="s3-sensor-js",
        task_id="sensor_one_key",
        aws_conn_id="aws_default",
    )

    descargar_from_s3 = S3ToSFTPOperator(
        task_id='descargar_from_s3',
        s3_bucket='s3-sensor-js',
        s3_key='reporte.csv',
        sftp_path='/tmp/reporte.csv',
        sftp_conn_id='conn_user_postgres',
        aws_conn_id='aws_default'
    )

    cargar_datos_postgres = PostgresOperator(
        task_id = 'cargar_datos_postgres',
        sql = "select fn_cargar_datos()",
        postgres_conn_id = 'conn_bd_postgres',
        autocommit = True        
    )

    
    sensor_aws_s3 >> descargar_from_s3 >> cargar_datos_postgres

    