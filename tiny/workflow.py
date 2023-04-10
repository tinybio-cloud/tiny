import enum
import json

import httpx

from .settings import PROD_BASE_URL


def execute_workflow(bucket_name: str, arguments: dict, auth_token: str) -> json:
    url = f'{PROD_BASE_URL}/workbench/{bucket_name}/run'
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.post(url=url, json=arguments, timeout=None, headers=headers)
    if r.status_code != 200:
        raise Exception(f'Failed to execute job: {r.text}')
    return r.json()


class JobStatus(enum.Enum):
    STATE_UNSPECIFIED = 'STATE UNSPECIFIED'
    QUEUED = 'QUEUED'
    SCHEDULED = 'SCHEDULED'
    RUNNING = 'RUNNING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    DELETION_IN_PROGRESS = 'DELETION IN PROGRESS'
    NOT_STARTED = 'NOT STARTED'

    STATUS_CHOICES = (
        (STATE_UNSPECIFIED, 'State unspecified'),
        (QUEUED, 'Queued'),
        (SCHEDULED, 'Scheduled'),
        (RUNNING, 'Running'),
        (SUCCEEDED, 'Succeeded'),
        (FAILED, 'Failed'),
        (DELETION_IN_PROGRESS, 'Deletion in progress'),
        (NOT_STARTED, 'Not started')
    )

    def __str__(self):
        rep_map = {
            'STATE_UNSPECIFIED': 'State unspecified',
            'QUEUED': 'Queued',
            'SCHEDULED': 'Scheduled',
            'RUNNING': 'Running',
            'SUCCEEDED': 'Succeeded',
            'FAILED': 'Failed',
            'DELETION IN PROGRESS': 'Deletion in progress',
            'NOT STARTED': 'Not started'
        }
        return rep_map.get(self.value)


def get_job(job_id: str, auth_token: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{job_id}'
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.get(url=url, timeout=None, headers=headers)
    if r.status_code != 200:
        return JobStatus.NOT_STARTED
    state = r.json().get('state')
    return JobStatus(state)


def get_job_logs(job_id: str, auth_token: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{job_id}/logs'
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.get(url=url, timeout=None, headers=headers)
    if r.status_code != 200:
        raise Exception(f'Failed to get job logs: {r.text}')
    return r.json()

def stream_job_logs(job_id: str, auth_token: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{job_id}/logs/stream'
    headers = {
        'Authorization': f'Bearer {auth_token}',
    }
    with httpx.stream('GET', url) as r:
        try:
            for chunk in r.iter_raw():  # or, for line in r.iter_lines():
                print(chunk.decode('utf-8').strip())
        except Exception as e:
            print(f"Stream Ended: no more logs to stream.")