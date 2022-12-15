from datetime import datetime

from .storage import upload_files, download_file, list_files_in_bucket
from .workflow import execute_workflow, get_workflow


class Job:
    # TODO: handle multiple inputs
    def __init__(self, tool: str, input_file: str, output_file: str, bucket_name: str, command: str,
                 flags: list = None):
        if flags is None:
            self.flags = list()
        else:
            self.flags = flags

        self.tool = tool
        self.input_file = input_file
        self.output_file = output_file
        self.command = command
        self.bucket_name = bucket_name
        self.input_uploaded = False
        self.remote_input_file_path = None
        self.execution_id = None

    def __repr__(self):
        input_file = self.remote_input_file_path if self.input_uploaded else self.input_file
        return f'{self.tool} {self.command} {" ".join(self.flags)} -o {self.output_file} {input_file}'

    def upload(self, file) -> dict:
        uploaded_files = upload_files(self.bucket_name, file)
        if uploaded_files.get(self.input_file):
            self.remote_input_file_path = uploaded_files.get(self.input_file)
        return uploaded_files

    def download(self, file) -> dict:
        return download_file(self.bucket_name, file)

    #TODO: rename to show workbench?
    def list_files(self):
        return list_files_in_bucket(self.bucket_name)

    def file_exists_in_bucket(self, file):
        input_file_path = f'input/{file}'
        return input_file_path in list_files_in_bucket(self.bucket_name), input_file_path

    def run(self):
        file_exists, path = self.file_exists_in_bucket(self.input_file)
        if file_exists:
            self.remote_input_file_path = path
        if not self.remote_input_file_path:
            self.upload(self.input_file)
        arguments = {
            'input': self.remote_input_file_path,
            'output': self.output_file,
            'bucket_name': self.bucket_name,
            'command': self.command,
            'flags': self.flags
        }
        execution = execute_workflow(self.tool, arguments)
        self.execution_id = execution.get('id')
        return execution

    def status(self):
        if not self.execution_id:
            raise Exception('Job not started')
        return get_workflow(self.tool, self.execution_id)
