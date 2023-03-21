from datetime import datetime
from typing import List, Tuple

import httpx
from tabulate import tabulate
from anytree import Node, RenderTree

from .storage import upload_files, download_file, list_files_in_bucket, upload_file_path, create_bucket
from .workflow import execute_workflow, get_job, get_job_logs, JobStatus
from .settings import PROD_BASE_URL


def print_table(headers, table_data):
    """
    Print table using specified headers, table data, format, and column width.
    """
    print(tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, None, 60, 60, 80]))


class Auth:
    def __init__(self, access_token: str = None):
        self.access_token = access_token

        if not self.access_token:
            self.authenticate()

    def __repr__(self):
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
        self._jobs = {}

        if not auth:
            self.auth = Auth()
            self.auth.authenticate()
        else:
            self.auth = auth

    def __repr__(self):
        return f'Workbench({self.bucket_name})'

    def _add_job(self, job: 'Job'):
        self._jobs[job.job_id] = job

    def remove_job(self, job_id):
        if job_id in self._jobs:
            del self._jobs[job_id]

    def run(self, tool: str, full_command: str):
        arguments = {
            'full_command': full_command,
            'tool': tool,
        }
        execution = execute_workflow(self.bucket_name, arguments, auth_token=self.auth.get_access_token())
        job = Job(
            job_id=execution.get('id'),
            tool=execution.get('tool'),
            full_command=execution.get('full_command'),
            workbench=self
        )
        self._add_job(job)
        get_logs = f"workbench.jobs['{job.job_id}'].logs()"
        table = [[job.job_id, job.tool, 'Queued', get_logs, job.full_command]]
        headers = ['Job ID', 'Tool', 'Status', 'Get Logs', 'Full Command']

        # format the table using tabulate
        print_table(headers, table)

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
        files = list_files_in_bucket(self.bucket_name, auth_token=self.auth.get_access_token())
        root = Node(self.bucket_name)
        for file in files:
            file_name = file.get('name')
            file_size = file.get('size')

            path = file_name.split("/")
            node = root
            for i in range(len(path)):
                name = path[i]
                if name not in [child.name for child in node.children]:
                    node = Node(name, parent=node)
                else:
                    node = [child for child in node.children if child.name == name][0]
            if file.get('size') is not None:
                Node(f"{file_name} ({file_size})", parent=node)
            else:
                Node(file_name, parent=node)

        output = ""
        for pre, _, node in RenderTree(root):
            output += f"{pre}{node.name}\n"

        print(output)

    def upload_job(self, files: List[Tuple[str, str]], method: str = 'curl'):
        upload_jobs = upload_file_path(self.bucket_name, files=files, method=method,
                                       auth_token=self.auth.get_access_token())
        table = []
        for job in upload_jobs:
            job = Job(job_id=job.get('id'), tool=method, full_command=f'{method} {job.get("input")}', workbench=self)
            row = [job.job_id, job.tool, job.status, f"workbench.jobs['{job.job_id}'].logs()", job.full_command]
            self._add_job(job)
            table.append(row)
        headers = ['Job ID', 'Tool', 'Status', 'Get Logs', 'Full Command']
        print_table(headers, table)

    def jobs(self):
        table = []
        for job in self._jobs.values():
            job.status = job.get_status()
            row = [job.job_id, job.tool, job.status, f"workbench.jobs['{job.job_id}'].logs()", job.full_command]
            table.append(row)

        headers = ['Job ID', 'Tool', 'Status', 'Get Logs', 'Full Command']

        # format the table using tabulate
        print_table(headers, table)


def create_workbench(bucket_name: str, auth: Auth = None):
    bucket = create_bucket(bucket_name, auth_token=auth.get_access_token())

    workbench_name = bucket.get('workbench_name')
    print(f"""
        The {workbench_name} workbench is now available. 

        The command workbench.list_files() will return the list of files in your workbench. Note, by default, we've included files for running through an RNA-Seq, ATAC-Seq, and variant calling experiments which are outline here: {urls}.

        The command workbench.run(tool=TOOL_NAME, full_command=COMMAND) will create a super computer (16 cores, 256GB RAM) with the specified tool installed and run the command specified in full_command. 

        To check the status of your commands for a workbench please run. workbench.logs(). 

        To upload a file directly from your machine run workbench.upload('file_path_on_your_machine'). Please note, if you're uploading from a colab notebook, you will need to first upload the file to the colab instance and then upload it from that instance. 

        To upload from a remote machine run workbench.upload_job(method="curl/wget", files=[("public_file_url","download_path")]). 

        To download a file run the following workbench.download('file_path_on_the_workbench'). This will generate a download URL.
    """)

    return Workbench(workbench_name, auth)


class Job:
    def __init__(
            self,
            job_id: str,
            tool: str,
            full_command: str,
            workbench: Workbench,
            status: str = JobStatus.QUEUED,
    ):
        self.job_id = job_id
        self.tool = tool
        self.full_command = full_command
        self.workbench = workbench
        self.status = status

    def get_status(self):
        if self.status in [JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.DELETION_IN_PROGRESS]:
            return self.status
        status = get_job(self.job_id, auth_token=self.workbench.auth.get_access_token())
        self.status = status
        return status.__str__()

    def logs(self):
        return get_job_logs(self.job_id, auth_token=self.workbench.auth.get_access_token())
