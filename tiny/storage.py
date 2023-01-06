import json
from os import listdir
from os.path import isfile, join, isdir, split

import httpx

from .settings import PROD_BASE_URL

INPUT_PREFIX: str = 'input/'


def download_file(bucket_name: str, remote_file: str) -> json:
    """
    Downloads a file from a bucket
    :param bucket_name: name of bucket
    :param remote_file: full path of remote file
    :return:
    """
    query_params = {'file_path': remote_file}
    url = f"{PROD_BASE_URL}/workbench/{bucket_name}/download"
    r = httpx.get(url, params=query_params)
    if r.status_code != 200:
        raise Exception(f"Error downloading file {remote_file} from bucket {bucket_name}")

    return r.json()


def list_files_in_bucket(bucket_name: str) -> json:
    """
    Lists files in a bucket
    :param bucket_name: name of bucket
    :return:
    """
    url = f"{PROD_BASE_URL}/workbench/{bucket_name}"
    r = httpx.get(url, timeout=None)
    if r.status_code != 200:
        raise Exception(f"Error listing files in bucket {bucket_name}")

    return r.json()


def _upload_blob(bucket_name: str, source_file_name: str) -> json:
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"

    # from requests_toolbelt import MultipartEncoder
    url = f"{PROD_BASE_URL}/workbench/{bucket_name}/upload"
    # m = MultipartEncoder(fields={'file': (source_file_name, open(source_file_name, 'rb'))})
    # r = requests.post(url, data=m, headers={'Content-Type': m.content_type})
    files = {'file': open(source_file_name, 'rb')}
    print(f'Uploading {source_file_name} to {bucket_name}')
    r = httpx.post(url, files=files, timeout=None)
    if r.status_code != 200:
        print(r.text)
        raise Exception(f"Error uploading file {source_file_name} to bucket {bucket_name}")

    return r.json()


def upload_files(bucket_name: str, local_files: str) -> dict:
    """
    Uploads a list or single files to a bucket
    :param bucket_name: name of bucket
    :param local_files: full path of local file or directory
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
                _upload_blob(bucket_name, local_file)
                destination_blob_name = dir_prefix + '/' + file
                file_mapping[local_file] = destination_blob_name
        else:
            _upload_blob(bucket_name, source_path)
            destination_blob_name = dir_prefix
            file_mapping[source_path] = destination_blob_name

        return file_mapping
    except Exception as e:
        raise e
