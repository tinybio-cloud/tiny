import json

import httpx

from .settings import PROD_BASE_URL


def execute_workflow(workflow: str, arguments: dict) -> json:
    url = f'{PROD_BASE_URL}/jobs/{workflow}'
    r = httpx.post(url=url, json=arguments)
    if r.status_code != 200:
        raise Exception(f'Failed to execute job: {r.text}')
    return r.json()


def get_workflow(tool: str, execution_id: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{tool}/{execution_id}'
    r = httpx.get(url=url)
    if r.status_code != 200:
        raise Exception(f'Failed to get job: {r.text}')
    return r.json()
