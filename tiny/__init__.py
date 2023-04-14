import os
from .main import Job, Workbench, Auth, create_workbench, list_workbenches

auth_token = os.environ.get('TINYBIO_AUTH_TOKEN')
if not auth_token:
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