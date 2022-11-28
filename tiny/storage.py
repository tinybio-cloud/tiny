from os import listdir
from os.path import isfile, join, isdir, basename, split

from google.cloud import storage

INPUT_PREFIX = 'input/'

def create_bucket(bucket_name):
    """
    Create a new bucket in the US region with the coldline storage
    class
    """
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket


def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print(f"Bucket {bucket.name} deleted")


def _upload_blob(bucket_name, source_file_name, destination_blob_name):
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
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def upload_files(bucket_name, local_files):
    try:
        is_dir = isdir(local_files)

        file_path, base_name = split(local_files)
        if base_name:
            dir_prefix = INPUT_PREFIX + base_name
            source_path = local_files + '/'
        else:
            dir_prefix = INPUT_PREFIX + basename(file_path)
            source_path = local_files

        if is_dir:
            files = [f for f in listdir(local_files) if isfile(join(local_files, f))]
            for file in files:
                local_file = source_path + file
                destination_blob_name = dir_prefix + '/' + file
                _upload_blob(bucket_name, local_file, destination_blob_name)
        else:
            destination_blob_name = dir_prefix
            _upload_blob(bucket_name, source_path, destination_blob_name)
    except Exception as e:
        raise e