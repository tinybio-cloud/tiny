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
```
import tiny

samtools = tiny.Job(
    tool="samtools",
    command="view",
    flags=["-h"],
    input=["/path/to/input.bam"],
    output=["/path/to/output.sam"],
    workbench="my-bucket",
)

# Run the job
>>> samtools.run()
{'input': 'input/wgEncodeRikenCageGm12878CellPapAlnRep1.bam', 'output': 'cli-test-out.sam', 'bucket_name': 'samtools-test-20221208212343699098', 'command': 'view', 'flags': ['-h'], 'id': '7d01ec8c-7c12-491b-b50e-fe7e6a1c67f4', 'repr': 'samtools view -h -o cli-test-out.sam input/wgEncodeRikenCageGm12878CellPapAlnRep1.bam'}

# Check the status
>>> samtools.status()
{'workflow_id': '7d01ec8c-7c12-491b-b50e-fe7e6a1c67f4', 'workflow_name': 'samtools', 'state': 'ACTIVE'}

# Download the output file
>>> samtools.download('cli-test-out.sam')
{'download_url': 'https://storage.googleapis.com/samtools-test-20221208212343699098/cli-test-out.sam?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=tiny-api%40nextflow-test-366601.iam.gserviceaccount.com%2F20221215%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221215T181037Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=host&X-Goog-Signature=2f9fe015912c436d5be285853e51c1897189d1df9ac66fdae68a11d69535ddaafbc54923d24a9044608390c74e54c9ebf924f62957d9d47aa69112d4788b6bd1020f435ab27069d4f5a9df816fd98f6967c5b1cf6eaf95cc978bf8d245202f4e5a3dd58f4b17ed84221f5e73f74ea78e6a4459b9998b5194ebe3a86a2f9ad7f0517d0fd0297e6a02f3e856baa85ee341afe7c26e788f687ba5632a2e3db4729e17f53c37bd5d5592fe22e9acbdde396c111a22dabeb4a28023e493ff1113489e4f815a96d37c9eab3830b5613fb93ae396ca3aa829b475c885073497371c592dd6923d82d6c7182674a0015bedaae2916b91802d0be6d61bd109d253d3024ebc'}

# Upload a file
>>> samtools.upload('/path/to/file/samplesheet_core.csv')
Uploading /path/to/file/samplesheet_core.csv to samtools-test-20221208212343699098
{'/path/to/file/samplesheet_core.csv': 'input/samplesheet_core.csv'}

# list files in bucket
>>> samtools.list_files()
['input/', 'input/wgEncodeRikenCageGm12878CellPapAlnRep1.bam', 'output/', 'output/cli-test-out.sam', 'working/']
```

```shell
# Run Job with full command
samtools = tiny.Job(tool='samtools', workbench='my-bucket')
samtools.run("view -h -o cli-test-out.sam /mnt/gcs/input/wgEncodeRikenCageGm12878CellPapAlnRep1.bam")

samtools.status()
```

### Distribute package to PIP
```shell
# bump version in setup.py
python setup.py sdist
twine upload dist/tiny-cli-{version}.tar.gz
```