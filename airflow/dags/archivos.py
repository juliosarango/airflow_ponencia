from airflow.models import Variable
from airflow.providers.ssh.hooks.ssh import SSHHook
import os


PATH_ORIGEN = Variable.get("path_web_1")
PATH_DESTINO = Variable.get("path_web_2")
PATH_LOCAL = Variable.get("path_local")

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
    result = "error"
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


def upload_file():
    """Uploads a file from the local filesystem to a remote server using SSHHook.

    Args:
        local_file (str): The path to the local file to upload.
        remote_path (str): The path to the remote file to upload to.
    """
    ssh_hook = SSHHook(ssh_conn_id="conn_web2")
    sftp_client = ssh_hook.get_conn().open_sftp()

    # if sftp_client.stat(remote_path) is false:
    #     sftp_client.mkdir(remote_path)

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
    result = "error"
    for file in list_files:
        local_file = os.path.join(PATH_LOCAL, file)
        remote_file = os.path.join(PATH_DESTINO, file)
        sftp_client.put(local_file, remote_file)
        sftp_client.chmod(remote_file, 0o644)
        contador += 1
        file_names.append(file)

    if contador == len(list_files) and contador > 0:
        result = "ok"
    else:
        result = "sin_archivos_destino"    

    sftp_client.close()
    return result, file_names
