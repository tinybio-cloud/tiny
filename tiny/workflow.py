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


def get_job(job_id: str, auth_token: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{job_id}'
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.get(url=url, headers=headers)
    if r.status_code != 200:
        raise Exception(f'Failed to get job: {r.text}')
    return r.json()


def get_job_logs(job_id: str, auth_token: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{job_id}/logs'
    headers = {'Authorization': f'Bearer {auth_token}'}
    r = httpx.get(url=url, timeout=None, headers=headers)
    if r.status_code != 200:
        raise Exception(f'Failed to get job logs: {r.text}')
    return r.json()
