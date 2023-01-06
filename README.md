# TINY BIO

### To use (with caution) for testing, simply do:
**Currently, this utilizes your local google oauth credentials.**

### Install
```
git clone https://github.com/tinybio-cloud/tiny.git
cd tiny

python -m venv env
source env/bin/activate 
pip install .
```

### Usage
```shell
import tiny

# initialize your workbench
workbench = tiny.Workbench('rna-seq-test')

# Upload files to your workbench
workbench.upload('/path/to/file/samplesheet_core.csv')
Uploading /path/to/file/samplesheet_core.csv to samtools-test-20221208212343699098
{'/path/to/file/samplesheet_core.csv': 'input/samplesheet_core.csv'}

# Run a job
# all jobs run are stored as Job objects on the workbench to access them use workbench.jobs
fastqc = workbench.run(
    tool="fastqc", 
    full_command="fastqc -o /mnt/gcs/output/qc/raw_reads /mnt/gcs/input/core-dataset/*.fastq.gz"
)

# Get status of a job
fastqc.status()
or
workbench.jobs[0].status()
{'id': 'job-fastqc-20230106-203225397382', 'state': 'State.QUEUED'}

# Get logs of a job
fastqc.logs()
or
workbench.jobs[0].logs()
[, 'Analysis complete for SRR6357070_1.fastq.gz', '\n', 'Started analysis of SRR6357070_2.fastq.gz\n', 'Approx 5% complete for SRR6357070_2.fastq.gz\n', ....]

# list files on your workbench
workbench.list_files()
['input/', 'input/wgEncodeRikenCageGm12878CellPapAlnRep1.bam', 'output/', 'output/cli-test-out.sam', 'working/']

# Download the output file
workbench.download('cli-test-out.sam')
{'download_url': 'https://storage.googleapis.com/samtools-test-20221208212343699098/cli-test-out.sam?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=tiny-api%40nextflow-test-366601.iam.gserviceaccount.com%2F20221215%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221215T181037Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=host&X-Goog-Signature=2f9fe015912c436d5be285853e51c1897189d1df9ac66fdae68a11d69535ddaafbc54923d24a9044608390c74e54c9ebf924f62957d9d47aa69112d4788b6bd1020f435ab27069d4f5a9df816fd98f6967c5b1cf6eaf95cc978bf8d245202f4e5a3dd58f4b17ed84221f5e73f74ea78e6a4459b9998b5194ebe3a86a2f9ad7f0517d0fd0297e6a02f3e856baa85ee341afe7c26e788f687ba5632a2e3db4729e17f53c37bd5d5592fe22e9acbdde396c111a22dabeb4a28023e493ff1113489e4f815a96d37c9eab3830b5613fb93ae396ca3aa829b475c885073497371c592dd6923d82d6c7182674a0015bedaae2916b91802d0be6d61bd109d253d3024ebc'}

```

### Distribute package to PIP
```shell
# bump version in setup.py
python setup.py sdist
twine upload dist/tiny-cli-{version}.tar.gz
```