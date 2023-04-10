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

# build auth page
get your auth token from https://tiny.bio/login

>>> import tiny

# Add your auth token to the environment
>>> export TINYBIO_AUTH_TOKEN=your_auth_token
or
>>> import os
>>> os.environ['TINYBIO_AUTH_TOKEN']='YOUR_TOKEN_HERE'

# Create a workbench or use your existing workbench
>>> workbench = tiny.create_workbench('workbench_name')
The testing-delete-me-20230410160630063331 workbench is now available. 

The command workbench.ls() will return the list of files in your workbench. Note, by default, we've included files for running through an RNA-Seq, ATAC-Seq, and variant calling experiments which are outline here:

https://docs.tinybio.cloud/docs

The command workbench.run(tool=TOOL_NAME, full_command=COMMAND) will create an instance that has 10 cores w/ 32GB RAM. The specified tool preinstalled and will run the command specified in full_command. 

To check the status of your commands for a workbench please run. workbench('JOBID').logs(). 

To upload a file directly from your machine run workbench.upload('file_path_on_your_machine'). Please note, if you're uploading from a colab notebook, you will need to first upload the file to the colab instance and then upload it from that instance. 

To upload from a remote machine run workbench.upload_job(method="curl or wget", files=[("public_file_url","destination_path_on_workbench")]). 

To download a file run the following workbench.download('file_path_on_the_workbench'). This will generate a download URL.
    
Workbench(testing-delete-me-20230410160630063331)


# initialize your workbench
>>> workbench = tiny.Workbench('rna-seq-test')

# Upload files to your workbench
>>> workbench.upload('/path/to/file/samplesheet_core.csv')
Uploading /path/to/file/samplesheet_core.csv to samtools-test-20221208212343699098
{'/path/to/file/samplesheet_core.csv': 'input/samplesheet_core.csv'}

# Run a job
# all jobs run are stored as Job objects on the workbench to access them use workbench.jobs
>>> fastqc = workbench.run(
    tool="samtools", 
    full_command="samtools quickcheck /mnt/gcs/output/mapping/sorted/CRR119890_Aligned_sorted.bam"
)
+---------------------+----------+----------+----------------------------------------------+---------------------------------------------------------------------------------+
| Job ID              | Tool     | Status   | Get Logs                                     | Full Command                                                                    |
+=====================+==========+==========+==============================================+=================================================================================+
| samtools-9284deada3 | samtools | Queued   | workbench.jobs['samtools-9284deada3'].logs() | samtools quickcheck /mnt/gcs/output/mapping/sorted/CRR119890_Aligned_sorted.bam |
+---------------------+----------+----------+----------------------------------------------+---------------------------------------------------------------------------------+

# Get status of all jobs
>>> workbench.jobs()
+---------------------+----------+-----------+----------------------------------------------+---------------------------------------------------------------------------------+
| Job ID              | Tool     | Status    | Get Logs                                     | Full Command                                                                    |
+=====================+==========+===========+==============================================+=================================================================================+
| samtools-9284deada3 | samtools | Scheduled | workbench.jobs['samtools-9284deada3'].logs() | samtools quickcheck /mnt/gcs/output/mapping/sorted/CRR119890_Aligned_sorted.bam |
+---------------------+----------+-----------+----------------------------------------------+---------------------------------------------------------------------------------+


# Get status of a single job
>>> fastqc.status()
or
>>> workbench.jobs['jobID'].get_status()
state.RUNNING

# Get logs of a job
>>> fastqc.logs()
or
>>> workbench.jobs[0].logs()
[, 'Analysis complete for SRR6357070_1.fastq.gz', '\n', 'Started analysis of SRR6357070_2.fastq.gz\n', 'Approx 5% complete for SRR6357070_2.fastq.gz\n', ....]

# list files on your workbench
>>> workbench.list_files()
reproduce-covid-paper-20230404201606359927
└── output
    └── mapping
        ├── 
        │   └── output/mapping/ (0 Bytes)
        ├── CRR119890_Aligned.out.bam
        │   └── output/mapping/CRR119890_Aligned.out.bam (17.6 GB)
        ├── CRR119890_Aligned.toTranscriptome.out.bam
        │   └── output/mapping/CRR119890_Aligned.toTranscriptome.out.bam (14.4 GB)
        ├── CRR119890_Log.final.out
        │   └── output/mapping/CRR119890_Log.final.out (2.0 kB)

# Download the output file
>>> workbench.download('cli-test-out.sam')
{'download_url': 'https://storage.googleapis.com/samtools-test-20221208212343699098/cli-test-out.sam?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=tiny-api%40nextflow-test-366601.iam.gserviceaccount.com%2F20221215%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221215T181037Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=host&X-Goog-Signature=2f9fe015912c436d5be285853e51c1897189d1df9ac66fdae68a11d69535ddaafbc54923d24a9044608390c74e54c9ebf924f62957d9d47aa69112d4788b6bd1020f435ab27069d4f5a9df816fd98f6967c5b1cf6eaf95cc978bf8d245202f4e5a3dd58f4b17ed84221f5e73f74ea78e6a4459b9998b5194ebe3a86a2f9ad7f0517d0fd0297e6a02f3e856baa85ee341afe7c26e788f687ba5632a2e3db4729e17f53c37bd5d5592fe22e9acbdde396c111a22dabeb4a28023e493ff1113489e4f815a96d37c9eab3830b5613fb93ae396ca3aa829b475c885073497371c592dd6923d82d6c7182674a0015bedaae2916b91802d0be6d61bd109d253d3024ebc'}

# Upload  files via a url to your workbench
files = [
    (
        'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR102/093/SRR10261593/SRR10261593_1.fastq.gz', 
        'input/sample_data/SRR10261593_ATAC-Seq_of_S._cerevisiae_at_30C_rep1_1.fastq.gz'
    ), 
    (
        'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR102/093/SRR10261593/SRR10261593_2.fastq.gz', 
        'input/sample_data/SRR10261593_ATAC-Seq_of_S._cerevisiae_at_30C_rep1_2.fastq.gz'
    )
    # (input_url, workbench_destination)
]

>>> workbench.upload_job(method='curl', files=files)
+-----------------+--------+----------+------------------------------------------+----------------------------------------------------------------------------------+
| Job ID          | Tool   | Status   | Get Logs                                 | Full Command                                                                     |
+=================+========+==========+==========================================+==================================================================================+
| curl-e129d17f4c | curl   | Queued   | workbench.jobs['curl-e129d17f4c'].logs() | curl                                                                             |
|                 |        |          |                                          | ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR102/093/SRR10261593/SRR10261593_1.fastq.gz |
+-----------------+--------+----------+------------------------------------------+----------------------------------------------------------------------------------+
| curl-2b319c97c2 | curl   | Queued   | workbench.jobs['curl-2b319c97c2'].logs() | curl                                                                             |
|                 |        |          |                                          | ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR102/093/SRR10261593/SRR10261593_2.fastq.gz |
+-----------------+--------+----------+------------------------------------------+----------------------------------------------------------------------------------+

# move files on your workbench
>>> workbench.move_file('input/sample_data/SRR10261593_1.fastq.gz', 'input/SRR10261593_1-renamed.fastq.gz')

# you can exclude certain statuses from the list of jobs
>>> workbench.jobs(exclude=['Succeeded'])

# Stream logs of a job
>>> workbench.jobs('samtools123').stream_logs()

# List files in a directory on your workbench
>>> workbench.ls('output/')
reproduce-covid-paper-20230404201606359927
└── output
    └── mapping
        ├── 
        │   └── output/mapping/ (0 Bytes)
        ├── CRR119890_Aligned.out.bam
        │   └── output/mapping/CRR119890_Aligned.out.bam (17.6 GB)
        ├── CRR119890_Aligned.toTranscriptome.out.bam
        │   └── output/mapping/CRR119890_Aligned.toTranscriptome.out.bam (14.4 GB)
        ├── CRR119890_Log.final.out
        │   └── output/mapping/CRR119890_Log.final.out (2.0 kB)

```

### Distribute package to PIP
```shell
# bump version in setup.py
python setup.py sdist
twine upload dist/tiny-cli-{version}.tar.gz
```