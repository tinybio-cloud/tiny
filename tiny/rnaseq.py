from datetime import datetime
from os import listdir
from os.path import isfile, join
import storage


class RNASeq():
    def __init__(self, core_data, fasta_file, gtf_files, input_file):
        self.core_data = core_data
        self.fasta_file = fasta_file
        self.gtf_files = gtf_files
        self.input_file = input_file

    def _create_bucket(self):
        bucket_name = f"rnaseq-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        try:
            bucket = storage.create_bucket(bucket_name)
            return bucket
        except Exception as e:
            raise e

    def _upload_files(self, bucket, local_folder):
        try:
            files = [f for f in listdir(local_folder) if isfile(join(local_folder, f))]
            for file in files:
                local_file = local_folder + file
                blob = bucket.blob(bucketFolder + file)
                blob.upload_from_filename(local_file)

            storage._upload_blob(bucket.name, self.fasta_file, "fasta_file")
            for gtf_file in self.gtf_files:
                storage._upload_blob(bucket.name, gtf_file, "gtf_file")
            storage._upload_blob(bucket.name, self.input_file, "input_file")
        except Exception as e:
            raise e

def rnaseq():
    '''
    tiny.rnaseq(core_data='', fasta='', gtf='')
./nextflow -c nextflow_batch.config run nf-core/rnaseq -profile docker --outdir ${OUTPUT_DIR} -w ${WORKING_DIR} --pseudo_aligner salmon --fasta core_ref/genome.fa --gtf core_ref/genes.gtf --input samplesheet_core.csv -resume
    :return:
    '''
