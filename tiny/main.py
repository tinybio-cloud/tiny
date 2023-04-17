import json
import os
from datetime import datetime
from typing import List, Tuple
import humanize

import httpx
from tabulate import tabulate
from anytree import Node, RenderTree

from .storage import upload_files, download_file, list_files_in_workbench, upload_file_path, create_bucket, move_file, \
    create_directory, get_workbenches, delete_path
from .workflow import execute_workflow, get_job, get_job_logs, JobStatus, stream_job_logs
from .settings import PROD_BASE_URL


def print_table(headers, table_data, maxcolwidths=[None, None, 60, 60, 80], sort=None):
    """
    Print table using specified headers, table data, format, and column width.
    """
    if sort:
        col_idx, order = sort
        table_data = sorted(table_data, key=lambda row: row[col_idx], reverse=order == "desc")

    print(tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=maxcolwidths))


class Auth:
    def __init__(self, access_token: str = None):
        self.access_token = access_token

    def get_access_token(self):
        return self.access_token


class Workbench:
    def __init__(self, workbench_name: str):
        self.name = workbench_name
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

To gain access to your workbench, run:
workbench = tiny.Workbench(name="WORKBENCH_NAME")

Check out these comprehensive tutorials on RNA-Seq, ATAC-Seq, and Variant calling on our docs here: http://docs.tinybio.cloud
            """)

    def __repr__(self):
        return f'Workbench({self.name})'

    def _add_job(self, job: 'Job'):
        self._jobs[job.job_id] = job

    def run(self, tool: str, full_command: str):
        arguments = {
            'full_command': full_command,
            'tool': tool,
        }
        status = JobStatus.QUEUED.__str__()
        try:
            execution = execute_workflow(self.name, arguments, auth_token=self.auth.get_access_token())
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
            uploaded_files = upload_files(self.name, file, auth_token=self.auth.get_access_token())
            return uploaded_files
        except Exception as e:
            print(e)

    def download(self, file) -> dict:
        try:
            return download_file(self.name, file, auth_token=self.auth.get_access_token())
        except Exception as e:
            print(e)

    def file_exists_in_bucket(self, file):
        input_file_path = f'input/{file}'
        return input_file_path in list_files_in_workbench(self.name,
                                                          auth_token=self.auth.get_access_token()), input_file_path

    def ls(self, path: str = None):
        return self.list_files(path)

    def list_files(self, path: str = None):
        files = list_files_in_workbench(
            self.name,
            auth_token=self.auth.get_access_token(),
            path=path
        )
        root = Node(self.name)
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
        upload_jobs = upload_file_path(self.name, files=files, method=method,
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
        try:
            response = move_file(self.name, source, destination, auth_token=self.auth.get_access_token())
            headers = ['Source', 'Destination', 'Message']
            table = [[source, destination, response.get('message')]]
            print_table(headers, table)
        except Exception as e:
            print(e)

    def create_directory(self, directory):
        try:
            response = create_directory(self.name, directory, auth_token=self.auth.get_access_token())
            headers = ['Workbench', 'Directory', 'Message']
            table = [[self.name, response.get('path'), "Directory created"]]
            print_table(headers, table)
        except Exception as e:
            print(e)

    def delete_path(self, path):
        try:
            response = delete_path(self.name, path, auth_token=self.auth.get_access_token())
            headers = ['Workbench', 'Path', 'Message']
            table = [[self.name, response.get('path'), response.get('status')]]
            print_table(headers, table)
        except Exception as e:
            print(e)


def list_workbenches():
    auth_token = os.environ.get('TINYBIO_AUTH_TOKEN')

    workbenches = get_workbenches(auth_token=auth_token)
    table = []
    for workbench in workbenches:
        updated_at = datetime.strptime(workbench.get('updated_at'), '%Y-%m-%dT%H:%M:%S.%f')
        table.append([workbench.get('name'), humanize.naturalsize(workbench.get('size')), humanize.naturaltime(datetime.now() - updated_at)])

    headers = ['Workbench Name', 'Size', 'Last Updated', ]

    # format the table using tabulate
    print_table(headers, table, sort=(0, "asc"))

def create_workbench(workbench_name: str):
    auth_token = os.environ.get('TINYBIO_AUTH_TOKEN')
    try:
        bucket = create_bucket(workbench_name, auth_token=auth_token)
    except Exception as e:
        print(e)
        return

    generate_workbench_name = bucket.get('workbench_name')
    print(f"""
The {generate_workbench_name} workbench is now available. 

The command workbench.ls() will return the list of files in your workbench. Note, by default, we've included files for running through an RNA-Seq, ATAC-Seq, and variant calling experiments which are outline here:

https://docs.tinybio.cloud/docs

The command workbench.run(tool=TOOL_NAME, full_command=COMMAND) will create an instance that has 10 cores w/ 32GB RAM. The specified tool preinstalled and will run the command specified in full_command. 

To check the status of your commands for a workbench please run. workbench('JOBID').logs(). 

To upload a file directly from your machine run workbench.upload('file_path_on_your_machine'). Please note, if you're uploading from a colab notebook, you will need to first upload the file to the colab instance and then upload it from that instance. 

To upload from a remote machine run workbench.upload_job(method="curl or wget", files=[("public_file_url","destination_path_on_workbench")]). 

To download a file run the following workbench.download('file_path_on_the_workbench'). This will generate a download URL.
    """)

    return Workbench(generate_workbench_name)


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
        return print_table(headers, data)

    def get_status(self):
        if getattr(JobStatus, self.status.__str__().upper()) in [JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.DELETION_IN_PROGRESS]:
            return self.status.__str__()
        status = get_job(self.job_id, workbench_name=self.workbench.name, auth_token=self.workbench.auth.get_access_token())
        self.status = status
        return status.__str__()

    def logs(self):
        try:
            return get_job_logs(self.job_id, workbench_name=self.workbench.name, auth_token=self.workbench.auth.get_access_token())
        except Exception as e:
            print(e)

    def stream_logs(self):
        try:
            stream_job_logs(self.job_id, workbench_name=self.workbench.name, auth_token=self.workbench.auth.get_access_token())
        except Exception as e:
            print(e)
