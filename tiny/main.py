from datetime import datetime

from .storage import upload_files, download_file, list_files_in_bucket
from .workflow import execute_workflow, get_job, get_job_logs


class Workbench:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.jobs = []

    def run(self, tool: str, full_command: str):

        arguments = {
            'full_command': full_command,
            'tool': tool,
        }
        execution = execute_workflow(self.bucket_name, arguments)
        job = Job(job_id=execution.get('id'), tool=execution.get('tool'), full_command=execution.get('full_command'))
        self.jobs.append(job)
        return job

    def upload(self, file) -> dict:
        uploaded_files = upload_files(self.bucket_name, file)
        return uploaded_files

    def download(self, file) -> dict:
        return download_file(self.bucket_name, file)

    def file_exists_in_bucket(self, file):
        input_file_path = f'input/{file}'
        return input_file_path in list_files_in_bucket(self.bucket_name), input_file_path

    def list_files(self):
        return list_files_in_bucket(self.bucket_name)


class Job:
    def __init__(
            self,
            job_id: str,
            tool: str,
            full_command: str,
    ):
        self.job_id = job_id
        self.tool = tool
        self.full_command = full_command

    def __repr__(self):
        return f'{self.job_id} running {self.full_command}'

    def status(self):
        return get_job(self.job_id)

    def logs(self):
        return get_job_logs(self.job_id)