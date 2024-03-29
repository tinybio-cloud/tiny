import json
from os import listdir
from os.path import isfile, join, isdir, split
from typing import List, Tuple, Any

import httpx

from .settings import PROD_BASE_URL

INPUT_PREFIX: str = 'input/'


def download_file(workbench_name: str, remote_file: str, auth_token: str) -> json:
    """
    Downloads a file from a workbench
    :param workbench_name: name of workbench
    :param remote_file: full path of remote file
    :param auth_token: auth token provided by logging in
    :return:
    """
    query_params = {'file_path': remote_file}
    url = f"{PROD_BASE_URL}/workbench/{workbench_name}/download"
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.get(url, timeout=None, params=query_params, headers=headers)
    if r.status_code != 200:
        raise Exception(f"Error downloading file {remote_file} from workbench {workbench_name}")

    return r.json()


def list_files_in_workbench(workbench_name: str, auth_token: str, path: str = None) -> json:
    """
    Lists files in a workbench
    :param workbench_name: name of workbench
    :param path: path to list files in
    :param auth_token: auth token provided by logging in
    :return:
    """
    url = f"{PROD_BASE_URL}/workbench/{workbench_name}"
    if path:
        url += f"?path={path}"

    #TODO: abstract this out into a client?
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.get(url, timeout=None, headers=headers)
    if r.status_code != 200:
        raise Exception(r.content)

    return r.json()


def _upload_blob(workbench_name: str, source_file_name: str, auth_token: str) -> json:
    """Uploads a file to the workbench."""
    # The ID of your GCS workbench
    # name = "your-workbench-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"

    # from requests_toolbelt import MultipartEncoder
    url = f"{PROD_BASE_URL}/workbench/{workbench_name}/upload"
    # m = MultipartEncoder(fields={'file': (source_file_name, open(source_file_name, 'rb'))})
    # r = requests.post(url, data=m, headers={'Content-Type': m.content_type})
    files = {'file': open(source_file_name, 'rb')}
    print(f'Uploading {source_file_name} to {workbench_name}')
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.post(url, files=files, timeout=None, headers=headers)
    if r.status_code != 200:
        print(r.text)
        raise Exception(f"Error uploading file {source_file_name} to workbench {workbench_name}")

    return r.json()


def upload_files(workbench_name: str, local_files: str, auth_token: str) -> dict:
    """
    Uploads a list or single files to a workbench
    :param workbench_name: name of workbench
    :param local_files: full path of local file or directory
    :param auth_token: auth token provided by logging in
    :return:
    """
    file_mapping = {}
    try:
        is_dir = isdir(local_files)

        file_path, base_name = split(local_files)
        dir_prefix = INPUT_PREFIX + base_name
        if base_name and is_dir:
            source_path = local_files + '/'
        else:
            source_path = local_files

        if is_dir:
            files = [f for f in listdir(local_files) if isfile(join(local_files, f))]
            for file in files:
                local_file = source_path + file
                _upload_blob(workbench_name, local_file, auth_token)
                destination_blob_name = dir_prefix + '/' + file
                file_mapping[local_file] = destination_blob_name
        else:
            _upload_blob(workbench_name, source_path, auth_token)
            destination_blob_name = dir_prefix
            file_mapping[source_path] = destination_blob_name

        return file_mapping
    except Exception as e:
        raise e


def upload_file_path(workbench_name: str, files: List[Tuple[str, str]], auth_token: str, method: str = 'curl') -> list[Any]:
    """
    creates a job that will download a list or single files to a workbench
    :param workbench_name: name of workbench
    :param files: list of tuples (url, output path)
    :param auth_token: auth token provided by logging in
    :param method: method to use to download file
    :return:
    """
    response = []
    for file in files:
        input_url = file[0]
        output_path = file[1]
        url = f"{PROD_BASE_URL}/workbench/{workbench_name}/upload/file-url"
        headers = {'Authorization': f'Bearer {auth_token}'}
        data = {
            'input_url': input_url,
            'output_path': output_path,
            'method': method
        }
        r = httpx.post(url, timeout=None, headers=headers, json=data)
        if r.status_code != 200:
            raise Exception(r.content)

        response.append(r.json())
    return response


def create_bucket(workbench_name: str, auth_token: str) -> json:
    """
    Creates a workbench
    :param workbench_name: name of workbench
    :param auth_token: auth token provided by logging in
    :return:
    """
    url = f"{PROD_BASE_URL}/workbench/{workbench_name}"
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.post(url, timeout=None, headers=headers)
    if r.status_code != 200:
        raise Exception(r.content)

    return r.json()


def move_file(workbench_name: str, source_file: str, destination_file: str, auth_token: str) -> json:
    """
    Moves a file in a workbench
    :param workbench_name: name of workbench
    :param source_file: full path of source file
    :param destination_file: full path of destination file
    :param auth_token: auth token provided by logging in
    :return:
    Cannot rename folders currently only files
    """

    url = f"{PROD_BASE_URL}/workbench/{workbench_name}/move-file"
    headers = {'Authorization': f'Bearer {auth_token}'}
    data = {
        'source_file_name': source_file,
        'destination_file_name': destination_file
    }
    r = httpx.post(url, timeout=None, headers=headers, json=data)
    if r.status_code != 200:
        return {'message': json.loads(r.content).get('detail')}

    return r.json()


def create_directory(workbench_name: str, directory: str, auth_token: str) -> json:
    """
    Creates a directory in a workbench
    :param workbench_name: name of workbench
    :param directory: full path of directory
    :param auth_token: auth token provided by logging in
    :return:
    """
    url = f"{PROD_BASE_URL}/workbench/{workbench_name}/create-directory"
    headers = {'Authorization': f'Bearer {auth_token}'}
    query_params = {
        'path': directory
    }
    r = httpx.post(url, timeout=None, headers=headers,  params=query_params)
    if r.status_code != 200:
        raise Exception(r.content)

    return r.json()


def delete_path(workbench_name: str, path: str, auth_token: str) -> json:
    """
    Deletes a file or directory in a workbench
    :param workbench_name: name of workbench
    :param path: full path of file or directory
    :param auth_token: auth token provided by logging in
    :return:
    """
    url = f"{PROD_BASE_URL}/workbench/{workbench_name}/delete-path"
    headers = {'Authorization': f'Bearer {auth_token}'}
    query_params = {
        'path': path
    }
    r = httpx.delete(url, timeout=None, headers=headers,  params=query_params)
    if r.status_code != 200:
        raise Exception(r.content)

    return r.json()


def get_workbenches(auth_token: str) -> json:
    """
    Gets a list of workbenches
    :return:
    """
    url = f"{PROD_BASE_URL}/workbench/me"
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.get(url, headers=headers, timeout=None)
    if r.status_code != 200:
        raise Exception(r.content)

    return r.json()