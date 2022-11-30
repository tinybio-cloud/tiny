import time
import json
from datetime import datetime

from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta
from google.cloud.workflows.executions_v1beta.types import executions, Execution

from .storage import create_bucket, upload_files


class RNASeq():
    def __init__(self, core_data: str, fasta_file: str, gtf_file: str, sample_sheet: str):
        self.local_core_data = core_data
        self.local_fasta_file = fasta_file
        self.local_gtf_file = gtf_file
        self.local_sample_sheet = sample_sheet
        self.bucket_name = None
        self.sample_sheet_cloud_path = None
        self.gtf_cloud_path = None
        self.fasta_cloud_path = None

    def _create_bucket(self):
        bucket_name = f"rnaseq-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        try:
            bucket = create_bucket(bucket_name)
            self.bucket_name = bucket.name
            return bucket
        except Exception as e:
            raise e

    def _upload_files(self, local_folder):
        if self.bucket_name:
            return upload_files(self.bucket_name, local_folder)
        else:
            raise Exception("No bucket created")

    def upload_data(self):
        # TODO: only create bucket if existing bucket is not provided
        self._create_bucket()
        self._upload_files(self.local_core_data)
        fasta_path_mapping = self._upload_files(self.local_fasta_file)
        gtf_path_mapping = self._upload_files(self.local_gtf_file)
        sample_sheet_path_mapping = self._upload_files(self.local_sample_sheet)
        self.fasta_cloud_path = fasta_path_mapping[self.local_fasta_file]
        self.gtf_cloud_path = gtf_path_mapping[self.local_gtf_file]
        self.sample_sheet_cloud_path = sample_sheet_path_mapping[self.local_sample_sheet]

    def run(self):
        # TODO: move these to constants
        project = 'nextflow-test-366601'
        location = 'us-central1'
        workflow = 'rnaseq_alpha'
        arguments = {
            "existingBucket": True,
            "fastaPath": self.fasta_cloud_path,
            "gtfPath": self.gtf_cloud_path,
            "inputBucket": self.bucket_name,
            "sampleSheet": self.sample_sheet_cloud_path,
        }

        if not project:
            raise Exception('GOOGLE_CLOUD_PROJECT env var is required.')

        # Set up API clients.
        execution_client = executions_v1beta.ExecutionsClient()
        workflows_client = workflows_v1beta.WorkflowsClient()

        # Construct the fully qualified location path.
        parent = workflows_client.workflow_path(project, location, workflow)

        # Execute the workflow.
        execution = Execution(argument=json.dumps(arguments))
        response = execution_client.create_execution(request={"parent": parent, "execution": execution})
        print(f"Created execution: {response.name}")

        # Wait for execution to finish, then print results.
        execution_finished = False
        backoff_delay = 1  # Start wait with delay of 1 second
        print('Poll every second for result...')
        while not execution_finished:
            execution = execution_client.get_execution(request={"name": response.name})
            execution_finished = execution.state != executions.Execution.State.ACTIVE

            # If we haven't seen the result yet, wait a second.
            if not execution_finished:
                print('- Waiting for results...')
                time.sleep(backoff_delay)
                backoff_delay *= 2  # Double the delay to provide exponential backoff.
            else:
                print(f'Execution finished with state: {execution.state.name}')
                print(execution.result)
                return execution.result
