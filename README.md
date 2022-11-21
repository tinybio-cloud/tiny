# TINY BIO

### To use (with caution) for testing, simply do:
**Currently, this utilizes your local google oauth credentials.**

```
git clone https://github.com/tinybio-cloud/tiny.git
cd tiny

python -m venv env
source env/bin/activate 
pip install .

# storage
import tiny

tiny.storage.create_bucket_class_location('bucket-name-test') 
tiny.storage.upload_blob(
    'bucket-name-test', 
    '/Local/Path/testfile', 
    'testfile.jpg'
)
```