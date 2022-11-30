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
from tiny.rnaseq import RNASeq

rna_job = RNASeq(
    core_data='core-dataset', 
    fasta_file='core_ref/genome.fa', 
    gtf_file='core_ref/genes.gtf', 
    sample_sheet='samplesheet_core.csv'
)

rna_job.upload_data()
>>> output/ with contents  uploaded to rnaseq-20221130113524359827.
>>> working/ with contents  uploaded to rnaseq-20221130113524359827.
>>> Created bucket rnaseq-20221130113524359827 in US with storage class COLDLINE
>>> File core-dataset/SRR6357072_2.fastq.gz uploaded to input/core-dataset/SRR6357072_2.fastq.gz
>>> File core-dataset/SRR6357081_1.fastq.gz uploaded to input/core-dataset/SRR6357081_1.fastq.gz
>>> File core-dataset/SRR6357080_2.fastq.gz uploaded to input/core-dataset/SRR6357080_2.fastq.gz
>>> File core-dataset/SRR6357073_1.fastq.gz uploaded to input/core-dataset/SRR6357073_1.fastq.gz
>>> File core-dataset/SRR6357076_1.fastq.gz uploaded to input/core-dataset/SRR6357076_1.fastq.gz
>>> File core-dataset/SRR6357077_2.fastq.gz uploaded to input/core-dataset/SRR6357077_2.fastq.gz
>>> File core-dataset/SRR6357070_2.fastq.gz uploaded to input/core-dataset/SRR6357070_2.fastq.gz
>>> File core-dataset/SRR6357071_1.fastq.gz uploaded to input/core-dataset/SRR6357071_1.fastq.gz
>>> File core-dataset/SRR6357078_2.fastq.gz uploaded to input/core-dataset/SRR6357078_2.fastq.gz
>>> ... 10 more files
>>> File core_ref/genome.fa uploaded to input/genome.fa
>>> File core_ref/genes.gtf uploaded to input/genes.gtf
>>> File samplesheet_core.csv uploaded to input/samplesheet_core.csv

rna_job.run()

rna_job.get_status()
>>> Execution status: ACTIVE
```