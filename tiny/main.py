import json
import os
from datetime import datetime
from typing import List, Tuple

import httpx
from tabulate import tabulate
from anytree import Node, RenderTree

from .storage import upload_files, download_file, list_files_in_bucket, upload_file_path, create_bucket, move_file
from .workflow import execute_workflow, get_job, get_job_logs, JobStatus, stream_job_logs
from .settings import PROD_BASE_URL


def print_table(headers, table_data, maxcolwidths=[None, None, 60, 60, 80]):
    """
    Print table using specified headers, table data, format, and column width.
    """
    print(tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=maxcolwidths))


class Auth:
    def __init__(self, access_token: str = None):
        self.access_token = access_token

    def get_access_token(self):
        return self.access_token


class Workbench:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self._jobs = {}
        auth_token = os.environ.get('TINYBIO_AUTH_TOKEN')
        if auth_token:
            self.auth = Auth(auth_token)
        else:
            print("""
TINYBIO_AUTH_TOKEN NOT FOUND IN ENVIRONMENT VARIABLES

To create a token click here: https://api.tinybio.cloud/readme-docs/login

SET YOUR TOKEN AS AN ENVIRONMENT VARIABLE:
import os
os.environ['TINYBIO_AUTH_TOKEN']='YOUR_TOKEN_HERE'

To gain access to your bucket, run:
workbench = tiny.Workbench(bucket_name="WORKBENCH_NAME")

Check out these comprehensive tutorials on RNA-Seq, ATAC-Seq, and Variant calling on our docs here: http://docs.tinybio.cloud
            """)

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
        status = JobStatus.QUEUED.__str__()
        try:
            execution = execute_workflow(self.bucket_name, arguments, auth_token=self.auth.get_access_token())
            job = Job(
                job_id=execution.get('id'),
                tool=execution.get('tool'),
                version=execution.get('version'),
                full_command=execution.get('full_command'),
                workbench=self
            )
            self._add_job(job)
            get_logs = f"workbench.jobs('{job.job_id}').logs()"
        except Exception as e:
            status = e.__str__()
            get_logs = 'N/A'
            job = Job(
                job_id='N/A',
                tool=tool,
                version='N/A',
                full_command=full_command,
                workbench=self
            )

        table = [[job.job_id, job.tool, job.version, status, get_logs, job.full_command]]
        headers = ['Job ID', 'Tool', 'Version', 'Status', 'Get Logs', 'Full Command']

        # format the table using tabulate
        print_table(headers, table)

    def upload_file(self, file) -> dict:
        try:
            uploaded_files = upload_files(self.bucket_name, file, auth_token=self.auth.get_access_token())
            return uploaded_files
        except Exception as e:
            print(e)

    def download(self, file) -> dict:
        try:
            return download_file(self.bucket_name, file, auth_token=self.auth.get_access_token())
        except Exception as e:
            print(e)

    def file_exists_in_bucket(self, file):
        input_file_path = f'input/{file}'
        return input_file_path in list_files_in_bucket(self.bucket_name,
                                                       auth_token=self.auth.get_access_token()), input_file_path

    def ls(self, path: str = None):
        return self.list_files(path)

    def list_files(self, path: str = None):
        files = list_files_in_bucket(
            self.bucket_name,
            auth_token=self.auth.get_access_token(),
            path=path
        )
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
            if file_size is not None:
                Node(f"{file_name} ({file_size})", parent=node)

        output = ""
        for pre, _, node in RenderTree(root):
            output += f"{pre}{node.name}\n"

        print(output)

    def upload_job(self, files: List[Tuple[str, str]], method: str = 'curl'):
        upload_jobs = upload_file_path(self.bucket_name, files=files, method=method,
                                       auth_token=self.auth.get_access_token())
        table = []
        for job in upload_jobs:
            job = Job(job_id=job.get('id'), tool=method, version='latest', full_command=f'{method} {job.get("input")}', workbench=self)
            row = [job.job_id, job.tool, job.version, job.status.__str__(), f"workbench.jobs('{job.job_id}').logs()", job.full_command]
            self._add_job(job)
            table.append(row)
        headers = ['Job ID', 'Tool', 'Version', 'Status', 'Get Logs', 'Full Command']
        print_table(headers, table)

    def jobs(self, job_id: str = None, exclude: List[str] = None):
        if job_id:
            return self._jobs.get(job_id)

        table = []
        for job in self._jobs.values():
            job.status = job.get_status()
            if exclude and job.status.__str__() in exclude:
                continue
            row = [job.job_id, job.tool, job.version, job.status.__str__(), f"workbench.jobs('{job.job_id}').logs()", job.full_command]
            table.append(row)

        headers = ['Job ID', 'Tool', 'Version', 'Status', 'Get Logs', 'Full Command']

        if not table:
            print('No jobs have been run yet. Run workbench.run(tool, full_command) to run a job.')
            return
        # format the table using tabulate
        print_table(headers, table)

    def move_file(self, source, destination):
        response = move_file(self.bucket_name, source, destination, auth_token=self.auth.get_access_token())
        headers = ['Source', 'Destination', 'Message']
        table = [[source, destination, response.get('message')]]
        print_table(headers, table)



def create_workbench(bucket_name: str):
    auth_token = os.environ.get('TINYBIO_AUTH_TOKEN')
    if not auth_token:
        print("""
TINYBIO_AUTH_TOKEN NOT FOUND IN ENVIRONMENT VARIABLES

To create a token click here: https://api.tinybio.cloud/readme-docs/login

SET YOUR TOKEN AS AN ENVIRONMENT VARIABLE:
import os
os.environ['TINYBIO_AUTH_TOKEN']='YOUR_TOKEN_HERE'

To gain access to your bucket, run:
workbench = tiny.Workbench(bucket_name="WORKBENCH_NAME")

Check out these comprehensive tutorials on RNA-Seq, ATAC-Seq, and Variant calling on our docs here: http://docs.tinybio.cloud
                """)
        return
    try:
        bucket = create_bucket(bucket_name, auth_token=auth_token)
    except Exception as e:
        print(e)
        return

    workbench_name = bucket.get('workbench_name')
    print(f"""
The {workbench_name} workbench is now available. 

The command workbench.ls() will return the list of files in your workbench. Note, by default, we've included files for running through an RNA-Seq, ATAC-Seq, and variant calling experiments which are outline here:

https://docs.tinybio.cloud/docs

The command workbench.run(tool=TOOL_NAME, full_command=COMMAND) will create an instance that has 10 cores w/ 32GB RAM. The specified tool preinstalled and will run the command specified in full_command. 

To check the status of your commands for a workbench please run. workbench('JOBID').logs(). 

To upload a file directly from your machine run workbench.upload('file_path_on_your_machine'). Please note, if you're uploading from a colab notebook, you will need to first upload the file to the colab instance and then upload it from that instance. 

To upload from a remote machine run workbench.upload_job(method="curl or wget", files=[("public_file_url","destination_path_on_workbench")]). 

To download a file run the following workbench.download('file_path_on_the_workbench'). This will generate a download URL.
    """)

    return Workbench(workbench_name)


class Job:
    def __init__(
            self,
            job_id: str,
            tool: str,
            version: str,
            full_command: str,
            workbench: Workbench,
            status: str = JobStatus.QUEUED,
    ):
        self.job_id = job_id
        self.tool = tool
        self.version = version
        self.full_command = full_command
        self.workbench = workbench
        self.status = status

    def __str__(self):
        headers = ['Job ID', 'Tool', 'Version', 'Status', 'Get Logs', 'Full Command']
        data = [[self.job_id, self.tool, self.version, self.get_status(), f"workbench.jobs('{self.job_id}').logs()", self.full_command]]
        print_table(headers, data)

    def get_status(self):
        if getattr(JobStatus, self.status.__str__().upper()) in [JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.DELETION_IN_PROGRESS]:
            return self.status.__str__()
        status = get_job(self.job_id, auth_token=self.workbench.auth.get_access_token())
        self.status = status
        return status.__str__()

    def logs(self):
        try:
            return get_job_logs(self.job_id, auth_token=self.workbench.auth.get_access_token())
        except Exception as e:
            print(e)

    def stream_logs(self):
        try:
            stream_job_logs(self.job_id, auth_token=self.workbench.auth.get_access_token())
        except Exception as e:
            print(e)
