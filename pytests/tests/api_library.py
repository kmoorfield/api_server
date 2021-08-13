#!/usr/bin/python3

import pytest
import json
import requests

class TestLibraryAPIClass:
    @staticmethod
    def get_api_request(url, headers=None, params=None, username="test", password="test"):
        response = requests.get(url, headers=headers, params=params, auth=(username, password))
        return response

    @staticmethod
    def post_api_request(url, json_data=None, headers=None, params=None, username="test", password="test"):
        payload = json.dumps(json_data)
        response = requests.post(url, data=payload, headers=headers, params=params, auth=(username, password))
        return response

    @staticmethod
    def put_api_request(url, json_data=None, headers=None, params=None, username="test", password="test"):
        payload = json.dumps(json_data)
        response = requests.put(url, data=payload, headers=headers, params=params, auth=(username, password))
        return response

    @staticmethod
    def patch_api_request(url, json_data=None, headers=None, params=None, username="test", password="test"):
        payload = json.dumps(json_data)
        response = requests.patch(url, data=payload, headers=headers, params=params, auth=(username, password))
        return response

    @staticmethod
    def delete_api_request(url, headers=None, params=None, username="test", password="test"):
        response = requests.delete(url, headers=headers, params=params, auth=(username, password))
        return response