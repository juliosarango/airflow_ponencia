# Apache Airflow

![logo airflow](images/apache_airflow.png)

# Automatizando tareas con Apache Airflow

Ponencia para el Freedom Software Day Quito - 2024

# Stack utilizado
- Docker
- Docker Compose

## Primer Caso
Copia de archivos desde un servidor hacia otro mediante mediante tarea programada.

### Arquitectura

![Caso 1](images/caso_1.png)

- Servidor 1: Servidor web con apache php y servicio ssh
- Servidor 2: Servidor web con apache php y servicio ssh
- Apache airflow

## Segundo Caso

### Arquitectura

![Caso 2](images/caso_2.png)

- Bucket de S3
- Apache airflow
- Servidor de Bd Postgres