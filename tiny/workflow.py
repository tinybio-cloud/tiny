import json

from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta
from google.cloud.workflows.executions_v1beta.types import executions, Execution

PROJECT = 'nextflow-test-366601'
LOCATION = 'us-central1'


def execute(arguments: dict, workflow: str) -> str:
    # Set up API clients.
    execution_client = executions_v1beta.ExecutionsClient()
    workflows_client = workflows_v1beta.WorkflowsClient()

    # Construct the fully qualified location path.
    parent = workflows_client.workflow_path(PROJECT, LOCATION, workflow)

    # Execute the workflow.
    execution = Execution(argument=json.dumps(arguments))
    response = execution_client.create_execution(request={"parent": parent, "execution": execution})
    return response.name


def get_execution(execution_name: str) -> Execution:
    execution_client = executions_v1beta.ExecutionsClient()
    execution = execution_client.get_execution(request={"name": execution_name})
    return execution
