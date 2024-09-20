from airflow.models import Variable
from airflow.providers.ssh.hooks.ssh import SSHHook
import os


PATH_ORIGEN = Variable.get("path_web_1")
PATH_DESTINO = Variable.get("path_web_2")
PATH_LOCAL = Variable.get("path_local")

def push_message(instance, name, valor):
    instance.xcom_push(key=name, value=valor)

def create_local_path(path):
    print("iniciamos creacion de path {path}")
    exist_dir = os.path.exists(path)
    if not exist_dir:
        try:
            os.makedirs(path, mode=0o755, exist_ok=True)
            print(f"Se creo el directorio: {path}")
        except:
            print(f"Error al crear el path {path}")

def download_files():
    
    ssh_hook = SSHHook(ssh_conn_id="conn_web1")
    sftp_client = ssh_hook.get_conn().open_sftp()

    contador = 0
    ftp_files = []
    file_names = []
    try:
        create_local_path(PATH_LOCAL)
        ftp_files = sftp_client.listdir(PATH_ORIGEN)
        for filename in ftp_files:
            sftp_client.get(PATH_ORIGEN + filename, PATH_LOCAL + filename)
            file_names.append(filename)
            contador += 1

        print(file_names)
    except FileNotFoundError:
        print("Error al descargar archivo")


def upload_files(**kwargs):
    """Uploads a file from the local filesystem to a remote server using SSHHook.

    Args:
        local_file (str): The path to the local file to upload.
        remote_path (str): The path to the remote file to upload to.
    """
    ssh_hook = SSHHook(ssh_conn_id="conn_web2")
    sftp_client = ssh_hook.get_conn().open_sftp()

    try:
        sftp_client.stat(PATH_DESTINO)
    except FileNotFoundError:
        sftp_client.mkdir(PATH_DESTINO)
        sftp_client.chdir(PATH_DESTINO)
        sftp_client.chdir("..")
        sftp_client.chmod(PATH_DESTINO, 0o755)
    except:
        print("Error al crear path remoto")

    list_files = os.listdir(PATH_LOCAL)
    contador = 0
    file_names = []

    for file in list_files:
        local_file = os.path.join(PATH_LOCAL, file)
        remote_file = os.path.join(PATH_DESTINO, file)
        sftp_client.put(local_file, remote_file)
        sftp_client.chmod(remote_file, 0o644)
        contador += 1
        file_names.append(local_file)

    if contador == len(list_files) and contador > 0:
        print("Archivos subidos correctamente")
        push_message(kwargs["ti"], "archivos_subidos", file_names)
    else:
        print("No se subieron archivos")
        push_message(kwargs["ti"], "archivos_subidos", [])

    sftp_client.close()


def delete_files(**kwargs):
    """Deletes a directory and all of its contents.

    Args:
        directory (str): The path to the directory to delete.
    """

    local_files = kwargs["task_instance"].xcom_pull(
        task_ids="subir_archivos",
        key="archivos_subidos",
    )

    if not local_files:
        return
    
    print(local_files)

    try:
        for file in local_files:    
            if os.path.isfile(file):
                print(f"Eliminando el archivo: {file}")
                os.remove(file) 
    except Exception as e:
        print(f"Error al eliminar archivos: {e}")