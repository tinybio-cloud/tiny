from datetime import datetime
from typing import List, Tuple

import httpx

from .storage import upload_files, download_file, list_files_in_bucket, upload_file_path
from .workflow import execute_workflow, get_job, get_job_logs
from .settings import PROD_BASE_URL


class Auth:
    def __init__(self, access_token: str = None):
        self.access_token = access_token

        if not self.access_token:
            self.authenticate()

    def __str__(self):
        return self.access_token

    def authenticate(self):
        login_url = f'{PROD_BASE_URL}/auth/google/authorize'
        response = httpx.get(login_url)

        if response.status_code == 200:
            auth_url = response.json().get('authorization_url')
            raise Exception(f'''
                To create a token click here: {auth_url}

                To gain access to your bucket, run:
                >>> auth = tiny.Auth('YOUR_TOKEN_HERE')
                >>> workbench = tiny.Workbench('your_bucket_name', auth=auth)
            ''')

        self.access_token = response.json().get('access_token')

    def get_access_token(self):
        return self.access_token


class Workbench:
    def __init__(self, bucket_name: str, auth: Auth = None):
        self.bucket_name = bucket_name
        self.jobs = {}

        if not auth:
            self.auth = Auth()
            self.auth.authenticate()
        else:
            self.auth = auth

    def _add_job(self, job: 'Job'):
        self.jobs[job.job_id] = job

    def remove_job(self, job_id):
        if job_id in self.jobs:
            del self.jobs[job_id]

    def run(self, tool: str, full_command: str):
        arguments = {
            'full_command': full_command,
            'tool': tool,
        }
        execution = execute_workflow(self.bucket_name, arguments, auth_token=self.auth.get_access_token())
        job = Job(job_id=execution.get('id'), tool=execution.get('tool'), full_command=execution.get('full_command'),
                  workbench=self)
        self._add_job(job)
        return job

    def upload_file(self, file) -> dict:
        uploaded_files = upload_files(self.bucket_name, file, auth_token=self.auth.get_access_token())
        return uploaded_files

    def download(self, file) -> dict:
        return download_file(self.bucket_name, file, auth_token=self.auth.get_access_token())

    def file_exists_in_bucket(self, file):
        input_file_path = f'input/{file}'
        return input_file_path in list_files_in_bucket(self.bucket_name,
                                                       auth_token=self.auth.get_access_token()), input_file_path

    def list_files(self):
        return list_files_in_bucket(self.bucket_name, auth_token=self.auth.get_access_token())

    def upload_job(self, files: List[Tuple[str, str]], method: str = 'curl'):
        upload_jobs = upload_file_path(self.bucket_name, files=files, method=method,
                                       auth_token=self.auth.get_access_token())
        for job in upload_jobs:
            job = Job(job_id=job.get('id'), tool=method, full_command=f'{method} {job.get("input")}', workbench=self)
            self._add_job(job)
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
        return get_job(self.job_id, auth_token=self.workbench.auth.get_access_token())

    def logs(self):
        return get_job_logs(self.job_id, auth_token=self.workbench.auth.get_access_token())
