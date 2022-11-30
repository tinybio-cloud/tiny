from datetime import datetime

from .storage import create_bucket, upload_files
from .workflow import execute, get_execution


class RNASeq():
    WORKFLOW = 'rnaseq_alpha'
    def __init__(self, core_data: str, fasta_file: str, gtf_file: str, sample_sheet: str):
        self.local_core_data = core_data
        self.local_fasta_file = fasta_file
        self.local_gtf_file = gtf_file
        self.local_sample_sheet = sample_sheet
        self.bucket_name = None
        self.sample_sheet_cloud_path = None
        self.gtf_cloud_path = None
        self.fasta_cloud_path = None
        self.workflow_name = None
        self.workflow_execution = None

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
        if not (self.bucket_name or self.sample_sheet_cloud_path or self.gtf_cloud_path or self.fasta_cloud_path):
            raise Exception("Data not uploaded")

        workflow: str = 'rnaseq_alpha'
        arguments = {
            "existingBucket": True,
            "fastaPath": self.fasta_cloud_path,
            "gtfPath": self.gtf_cloud_path,
            "inputBucket": self.bucket_name,
            "sampleSheet": self.sample_sheet_cloud_path,
        }

        self.workflow_name = execute(arguments, workflow)
        print(f"Created execution: {self.workflow_name}")

    def get_status(self):
        execution = get_execution(self.workflow_name)
        print(f"Execution status: {execution.state.name}")
        if execution.result:
            print(f"Execution result: {execution.result}")
        if execution.error:
            print(f"Execution result: {execution.error}")

        self.workflow_execution = execution
