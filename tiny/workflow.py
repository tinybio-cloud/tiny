import json

import httpx

from .settings import PROD_BASE_URL


def execute_workflow(bucket_name: str, arguments: dict) -> json:
    url = f'{PROD_BASE_URL}/workbench/{bucket_name}/run'
    r = httpx.post(url=url, json=arguments, timeout=None)
    if r.status_code != 200:
        raise Exception(f'Failed to execute job: {r.text}')
    return r.json()


def get_job(job_id: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{job_id}'
    r = httpx.get(url=url)
    if r.status_code != 200:
        raise Exception(f'Failed to get job: {r.text}')
    return r.json()


def get_job_logs(job_id: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{job_id}/logs'
    r = httpx.get(url=url, timeout=None)
    if r.status_code != 200:
        raise Exception(f'Failed to get job logs: {r.text}')
    return r.json()
