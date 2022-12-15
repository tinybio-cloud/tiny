import json

import requests

from .settings import PROD_BASE_URL


def execute_workflow(tool: str, arguments: dict) -> json:
    url = f'{PROD_BASE_URL}/jobs/{tool}'
    r = requests.post(url=url, json=arguments)
    if r.status_code != 200:
        raise Exception(f'Failed to execute job: {r.text}')
    return r.json()


def get_workflow(tool: str, execution_id: str) -> json:
    url = f'{PROD_BASE_URL}/jobs/{tool}/{execution_id}'
    r = requests.get(url=url)
    if r.status_code != 200:
        raise Exception(f'Failed to get job: {r.text}')
    return r.json()
