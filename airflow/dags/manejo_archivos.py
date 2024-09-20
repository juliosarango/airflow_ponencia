from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable

from pendulum import duration

from archivos import download_files, upload_files, delete_files

from datetime import datetime

email_notificacion = Variable.get("email_notificacion")

default_args = {
    "start_date": datetime(2024, 9, 12),
    "retries": 3,
    "retry_delay": duration(seconds=2),
    "email": [email_notificacion],
    "email_on_failure": True,
}

with DAG(
    dag_id="manejo_arhivos",
    schedule_interval="*/5 * * * *",
    default_args=default_args,
    catchup=False,

) as dag:
    
    download_files_operator = PythonOperator(
        task_id="descargar_archivos",
        python_callable = download_files,
        provide_context=True
    )

    upload_files_operator = PythonOperator(
        task_id="subir_archivos",
        python_callable = upload_files,
        provide_context=True
    )

    delete_files = PythonOperator(
        task_id="eliminar_archivos",
        python_callable=delete_files
    )



    download_files_operator >> upload_files_operator >> delete_files