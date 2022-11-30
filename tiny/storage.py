from os import listdir
from os.path import isfile, join, isdir, basename, split

from google.cloud import storage

INPUT_PREFIX: str = 'input/'

#TODO: look at client lib for tests

def create_bucket(bucket_name: str):
    """
    Create a new bucket in the US region with the coldline storage
    class
    """
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    # Create default directories
    _upload_blob_from_memory(bucket_name, '', 'input/')
    _upload_blob_from_memory(bucket_name, '', 'output/')
    _upload_blob_from_memory(bucket_name, '', 'working/')

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket


def delete_bucket(bucket_name: str):
    """Deletes a bucket. The bucket must be empty."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print(f"Bucket {bucket.name} deleted")


def _upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}"
    )
    return destination_blob_name


def _upload_blob_from_memory(bucket_name: str, contents: str, destination_blob_name: str):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
    )


def upload_files(bucket_name: str, local_files: str):
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
        if base_name and is_dir:
            dir_prefix = INPUT_PREFIX + base_name
            source_path = local_files + '/'
        else:
            dir_prefix = INPUT_PREFIX + base_name
            source_path = local_files

        if is_dir:
            files = [f for f in listdir(local_files) if isfile(join(local_files, f))]
            for file in files:
                local_file = source_path + file
                destination_blob_name = dir_prefix + '/' + file
                _upload_blob(bucket_name, local_file, destination_blob_name)
                file_mapping[local_file] = destination_blob_name
        else:
            destination_blob_name = dir_prefix
            _upload_blob(bucket_name, source_path, destination_blob_name)
            file_mapping[source_path] = destination_blob_name

        return file_mapping
    except Exception as e:
        raise e


# TODO: add list files in bucket
# TODO: add download files from bucket