from datetime import datetime
from typing import List, Tuple

import httpx
from tabulate import tabulate

from .storage import upload_files, download_file, list_files_in_bucket, upload_file_path
from .workflow import execute_workflow, get_job, get_job_logs
from .settings import PROD_BASE_URL


class Workbench:
    def __init__(self, bucket_name: str, auth_token: str = None):
        if not auth_token:
            login_url = f'{PROD_BASE_URL}/auth/google/authorize'
            response = httpx.get(login_url)
            if response.status_code == 200:
                auth_url = response.json().get('authorization_url')
                raise Exception(f'Please provide an auth token to get an auth token login via {auth_url}')

        self.bucket_name = bucket_name
        self.jobs = []
        self.auth_token = auth_token

    def run(self, tool: str, full_command: str):
        arguments = {
            'full_command': full_command,
            'tool': tool,
        }
        execution = execute_workflow(self.bucket_name, arguments, auth_token=self.auth_token)
        job = Job(job_id=execution.get('id'), tool=execution.get('tool'), full_command=execution.get('full_command'), workbench=self)
        self.jobs.append(job)
        # create a table with the relevant job information
        table = [[job.job_id, job.tool, job.full_command, f"wb.('{job.job_id}').status()"] for job in self.jobs]
        headers = ['Job ID', 'Tool', 'Full Command', 'status']

        # format the table using tabulate
        print(tabulate(table, headers=headers))
        # return job

    def upload_file(self, file) -> dict:
        uploaded_files = upload_files(self.bucket_name, file, auth_token=self.auth_token)
        return uploaded_files

    def download(self, file) -> dict:
        return download_file(self.bucket_name, file, auth_token=self.auth_token)

    def file_exists_in_bucket(self, file):
        input_file_path = f'input/{file}'
        return input_file_path in list_files_in_bucket(self.bucket_name, auth_token=self.auth_token), input_file_path

    def list_files(self):
        return list_files_in_bucket(self.bucket_name, auth_token=self.auth_token)

    def upload_job(self, files: List[Tuple[str, str]], method: str = 'curl'):
        upload_jobs = upload_file_path(self.bucket_name, files=files, method=method, auth_token=self.auth_token)
        for job in upload_jobs:
            self.jobs.append(Job(job_id=job.get('id'), tool=method, full_command=f'{method} {job.get("input")}', workbench=self))
        return upload_jobs


class Job:
    def __init__(
            self,
            job_id: str,
            tool: str,
            full_command: str,
            workbench: Workbench,
    ):
        self.job_id = job_id
        self.tool = tool
        self.full_command = full_command
        self.workbench = workbench

    def __repr__(self):
        return f'{self.job_id} running {self.full_command}'

    def status(self):
        return get_job(self.job_id, auth_token=self.workbench.auth_token)

    def logs(self):
        return get_job_logs(self.job_id, auth_token=self.workbench.auth_token)
