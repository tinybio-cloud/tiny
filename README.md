# tinybio-cli
Tinybio is a python library for quickly running bioinformatics jobs on on a powerful cloud computer. The main feature of tinybio is being able to spin up and run bioinformatics commands on files that are stored on tinybio storage buckets that we’ll refer to as workbenches.

Please visit https://docs.tinybio.cloud/docs/ for the full documentation.

A full list of commands can be found https://docs.tinybio.cloud/docs/tiny-cli-commands

---
# Quick Start
## Installation

The first step is to install the tinybio-cli module. You can do this by opening a terminal or command prompt and running the following command:

```Text shell
pip install tiny-cli
```

## Authentication

After installing the module, you need to authenticate your Google account with tinybio.cloud. To do this, go to <https://api.tinybio.cloud/readme-docs/login> and use your Google account to authenticate. 

Once authenticated, you will be redirected to our api docs and receive a bearer token that you can use to start requests with.

## Usage

#### Set environment variables and import Tiny Cli

```python
import os
os.environ['TINYBIO_AUTH_TOKEN']='YOUR_TOKEN_HERE'

import tiny
```

#### We created a starter bench with samples when you signed up to help you get started. This is how you can see your active Workbenches

```python
tiny.list_workbenches()
+----------------------------------------------+----------+----------------+
| Workbench Name                               | Size     | Last Updated   |
+==============================================+==========+================+
| tiny-26-starter-samples-20230501181335640599 | 161.7 GB | 2 day ago      |
+----------------------------------------------+----------+----------------+
```

#### Initialize your starter Workbench or create a new one

```python
workbench = tiny.Workbench('user-id-4-starter-samples-20230419172317820288')

or

workbench = tiny.create_workbench('foobar')
The foobar-20230410160630063331 workbench is now available.
```

#### Take a look at the files on the Workbench

```python
workbench.ls()

tiny-26-starter-samples-20230501181335640599
├── input
│   ├──
│   │   └── input/ (0 Bytes)
│   ├── atac-seq
│   │   ├── SRR10261591_1.fastq.gz
│   │   │   └── input/atac-seq/SRR10261591_1.fastq.gz (592.4 MB)
│   │   ├── SRR10261591_2.fastq.gz
│   │   │   └── input/atac-seq/SRR10261591_2.fastq.gz (1.3 GB)
│   │   ├── SRR10261592_1.fastq.gz
│   │   │   └── input/atac-seq/SRR10261592_1.fastq.gz (1.9 GB)
│   │   ├── SRR10261592_2.fastq.gz
│   │   │   └── input/atac-seq/SRR10261592_2.fastq.gz (1.9 GB)
│   │   ├── SRR10261593_1.fastq.gz
│   │   │   └── input/atac-seq/SRR10261593_1.fastq.gz (1.4 GB)
│   │   ├── SRR10261593_2.fastq.gz
│   │   │   └── input/atac-seq/SRR10261593_2.fastq.gz (1.4 GB)
│   │   ├── SRR10261594_1.fastq.gz
│   │   │   └── input/atac-seq/SRR10261594_1.fastq.gz (1.6 GB)
│   │   ├── SRR10261594_2.fastq.gz
│   │   │   └── input/atac-seq/SRR10261594_2.fastq.gz (1.7 GB)
│   │   ├── SRR10261595_1.fastq.gz
│   │   │   └── input/atac-seq/SRR10261595_1.fastq.gz (1.3 GB)
│   │   ├── SRR10261595_2.fastq.gz
│   │   │   └── input/atac-seq/SRR10261595_2.fastq.gz (1.4 GB)
│   │   ├── SRR10261596_1.fastq.gz
│   │   │   └── input/atac-seq/SRR10261596_1.fastq.gz (1.3 GB)
│   │   ├── SRR10261596_2.fastq.gz
│   │   │   └── input/atac-seq/SRR10261596_2.fastq.gz (1.4 GB)
│   │   ├── ref_gen
│   │   │   ├── SC.amb
│   │   │   │   └── input/atac-seq/ref_gen/SC.amb (45 Bytes)
│   │   │   ├── SC.ann
│   │   │   │   └── input/atac-seq/ref_gen/SC.ann (515 Bytes)
│   │   │   ├── SC.bwt
│   │   │   │   └── input/atac-seq/ref_gen/SC.bwt (12.2 MB)
│   │   │   ├── SC.pac
│   │   │   │   └── input/atac-seq/ref_gen/SC.pac (3.0 MB)
│   │   │   ├── SC.sa
│   │   │   │   └── input/atac-seq/ref_gen/SC.sa (6.1 MB)
│   │   │   ├── S_cerevisiae_masked_rRNA.fasta
│   │   │   │   └── input/atac-seq/ref_gen/S_cerevisiae_masked_rRNA.fasta (12.4 MB)
│   │   │   ├── S_uvarum.fasta
│   │   │   │   └── input/atac-seq/ref_gen/S_uvarum.fasta (11.6 MB)
│   │   │   ├── Saccharomyces_cerevisiae.R64-1-1.106.gtf
│   │   │   │   └── input/atac-seq/ref_gen/Saccharomyces_cerevisiae.R64-1-1.106.gtf (9.6 MB)
│   │   │   ├── Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
│   │   │   │   └── input/atac-seq/ref_gen/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa (12.4 MB)
│   │   │   ├── Sbay.ultrascaf
│   │   │   │   └── input/atac-seq/ref_gen/Sbay.ultrascaf (11.5 MB)
│   │   │   ├── Sbay.unplaced
│   │   │   │   └── input/atac-seq/ref_gen/Sbay.unplaced (118.3 kB)
│   │   │   ├── hybrid.amb
│   │   │   │   └── input/atac-seq/ref_gen/hybrid.amb (5.9 kB)
│   │   │   ├── hybrid.ann
│   │   │   │   └── input/atac-seq/ref_gen/hybrid.ann (7.3 kB)
│   │   │   ├── hybrid.bwt
│   │   │   │   └── input/atac-seq/ref_gen/hybrid.bwt (23.8 MB)
│   │   │   ├── hybrid.fasta
│   │   │   │   └── input/atac-seq/ref_gen/hybrid.fasta (24.0 MB)
│   │   │   ├── hybrid.pac
│   │   │   │   └── input/atac-seq/ref_gen/hybrid.pac (5.9 MB)
│   │   │   ├── hybrid.sa
│   │   │   │   └── input/atac-seq/ref_gen/hybrid.sa (11.9 MB)
│   │   │   └── mask_rRNA.bed
│   │   │       └── input/atac-seq/ref_gen/mask_rRNA.bed (36 Bytes)
│   │   └── rscript
│   │       ├── diffbind_qc.R
│   │       │   └── input/atac-seq/rscript/diffbind_qc.R (2.5 kB)
│   │       └── occupancy_and_diff_accessibility.R
│   │           └── input/atac-seq/rscript/occupancy_and_diff_accessibility.R (2.4 kB)
│   ├── rna-seq
│   │   ├── SRR1278968_1.fastq.gz
│   │   │   └── input/rna-seq/SRR1278968_1.fastq.gz (1.0 GB)
│   │   ├── SRR1278968_2.fastq.gz
│   │   │   └── input/rna-seq/SRR1278968_2.fastq.gz (1.1 GB)
│   │   ├── SRR1278969_1.fastq.gz
│   │   │   └── input/rna-seq/SRR1278969_1.fastq.gz (1.0 GB)
│   │   ├── SRR1278969_2.fastq.gz
│   │   │   └── input/rna-seq/SRR1278969_2.fastq.gz (1.1 GB)
│   │   ├── SRR1278970_1.fastq.gz
│   │   │   └── input/rna-seq/SRR1278970_1.fastq.gz (1.0 GB)
│   │   ├── SRR1278970_2.fastq.gz
│   │   │   └── input/rna-seq/SRR1278970_2.fastq.gz (1.1 GB)
│   │   ├── SRR1278971_1.fastq.gz
│   │   │   └── input/rna-seq/SRR1278971_1.fastq.gz (966.6 MB)
│   │   ├── SRR1278971_2.fastq.gz
│   │   │   └── input/rna-seq/SRR1278971_2.fastq.gz (961.4 MB)
│   │   ├── SRR1278972_1.fastq.gz
│   │   │   └── input/rna-seq/SRR1278972_1.fastq.gz (1.0 GB)
│   │   ├── SRR1278972_2.fastq.gz
│   │   │   └── input/rna-seq/SRR1278972_2.fastq.gz (1.0 GB)
│   │   ├── SRR1278973_1.fastq.gz
│   │   │   └── input/rna-seq/SRR1278973_1.fastq.gz (982.2 MB)
│   │   ├── SRR1278973_2.fastq.gz
│   │   │   └── input/rna-seq/SRR1278973_2.fastq.gz (983.3 MB)
│   │   ├── ref_gen
│   │   │   ├── C_parapsilosis_CDC317_current_chromosomes.fasta
│   │   │   │   └── input/rna-seq/ref_gen/C_parapsilosis_CDC317_current_chromosomes.fasta (13.2 MB)
│   │   │   └── C_parapsilosis_CDC317_current_features.gff
│   │   │       └── input/rna-seq/ref_gen/C_parapsilosis_CDC317_current_features.gff (5.8 MB)
│   │   └── rscript
│   │       ├── DE.R
│   │       │   └── input/rna-seq/rscript/DE.R (2.3 kB)
│   │       └── GO.R
│   │           └── input/rna-seq/rscript/GO.R (1.9 kB)
│   └── variants-calling
│       ├── SRR15498471_1.fastq.gz
│       │   └── input/variants-calling/SRR15498471_1.fastq.gz (1.4 GB)
│       ├── SRR15498471_2.fastq.gz
│       │   └── input/variants-calling/SRR15498471_2.fastq.gz (1.5 GB)
│       └── ref_gen
│           ├── C_glabrata_CBS138_current_chromosomes.fasta
│           │   └── input/variants-calling/ref_gen/C_glabrata_CBS138_current_chromosomes.fasta (13.0 MB)
│           └── C_glabrata_CBS138_current_features.gff
│               └── input/variants-calling/ref_gen/C_glabrata_CBS138_current_features.gff (5.3 MB)
├── output
│   ├──
│   │   └── output/ (0 Bytes)
│   ├── atac-seq
│   │   └──
│   │       └── output/atac-seq/ (0 Bytes)
│   ├── rna-seq
│   │   └──
│   │       └── output/rna-seq/ (0 Bytes)
│   └── variants-calling
│       └──
│           └── output/variants-calling/ (0 Bytes)
└── working
    └──
        └── working/ (0 Bytes)
```

#### Start using the tools available on TinyBio

```
workbench.run(
  tool="fastqc", 
  full_command="fastqc -t 10 /input/atac-seq/*gz -o /output/atac-seq/fastqc_initial"
)
+------------------+--------+-----------+----------+-------------------------------------------+----------------------------------------------------------------------+
| Job ID           | Tool   | Version   | Status   | Get Logs                                  | Full Command                                                         |
+==================+========+===========+==========+===========================================+======================================================================+
| fastqc85b9ac7494 | fastqc | 0.11.8    | Queued   | workbench.jobs('fastqc85b9ac7494').logs() | fastqc -t 10 /input/atac-seq/*.gz -o /output/atac-seq/fastqc_initial |
+------------------+--------+-----------+----------+-------------------------------------------+----------------------------------------------------------------------+
```

#### View status of Jobs on your Workbench session

```
workbench.jobs()

+------------------+--------+-----------+----------+-------------------------------------------+----------------------------------------------------------------------+
| Job ID           | Tool   | Version   | Status   | Get Logs                                  | Full Command                                                         |
+==================+========+===========+==========+===========================================+======================================================================+
| fastqc85b9ac7494 | fastqc | 0.11.8    | Running  | workbench.jobs('fastqc85b9ac7494').logs() | fastqc -t 10 /input/atac-seq/*.gz -o /output/atac-seq/fastqc_initial |
+------------------+--------+-----------+----------+-------------------------------------------+----------------------------------------------------------------------+
```

🎉 Congratulations! You have successfully set up and used TinyBio to run a basic bioinformatic pipeline! 👏🏽

## Guides

👀 Check out one of our existing Google Colab notebooks :notebook-with-decorative-cover: to discover more on what Tinybio can do

[ATAC-Seq Colab Notebook](https://colab.research.google.com/drive/1Bwn8PDW8SZK1eypoTEuuh0yiapZKq0sK?usp=sharing)

[Variants Calling Colab Notebook](https://colab.research.google.com/drive/1JKYUwOd72r9MGLL4IjeUgKoh3A3aZ5-c?usp=sharing)

[RNA-Seq Colab Notebook](https://colab.research.google.com/drive/10Xz46EgSTLsEKH3kcyKVlRBrnPD-xHAB?usp=sharing)

See a full list of supported tools by using our API
```shell
curl -X 'GET' \
  'https://api.tinybio.cloud/available-tools' \
  -H 'accept: application/json'
```

----

### Distribute package to PIP
```shell
# bump version in setup.py
python setup.py sdist
twine upload dist/tiny-cli-{version}.tar.gz
```
