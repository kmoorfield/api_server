#!/usr/bin/python3

import pytest
import sys
from api_library import TestLibraryAPIClass

class TestApiClass:
    @staticmethod
    def test_api_get_first():
        result = TestLibraryAPIClass.get_api_request("http://webapi/first")
        assert result.status_code == 200
        assert result.json() == {"id": 1,"fact": "All dogs can be traced back 40 million years ago to a weasel animal called the Miacis which dwelled in trees and dens. The Miacis later evolved into the Tomarctus, a direct forbear of the genus Canis, which includes the wolf and jackal as well as the dog."}

    @staticmethod
    def test_api_get_last():
        result = TestLibraryAPIClass.get_api_request("http://webapi/last")
        assert result.status_code == 200
        assert result.json() == {"id": 357, "fact": "Dogs can discriminate the emotional expressions of human faces."}

    @staticmethod
    def test_api_get_random():
        result = TestLibraryAPIClass.get_api_request("http://webapi/random")
        assert result.status_code == 200
        assert result.json()["id"] is not None
        assert result.json()["fact"] is not None
        result2 = TestLibraryAPIClass.get_api_request("http://webapi/random")
        assert result.status_code == 200
        assert result.json()["id"] != result2.json()["id"]
        assert result.json()["fact"] != result2.json()["fact"]

    @staticmethod
    def test_api_get_all():
        result = TestLibraryAPIClass.get_api_request("http://webapi/all")
        assert result.status_code == 200
        assert result.json() is not None

    @staticmethod
    def test_api_get_record():
        result = TestLibraryAPIClass.get_api_request("http://webapi/record/1")
        assert result.status_code == 200
        assert result.json() == {"id": 1, "fact": "All dogs can be traced back 40 million years ago to a weasel animal called the Miacis which dwelled in trees and dens. The Miacis later evolved into the Tomarctus, a direct forbear of the genus Canis, which includes the wolf and jackal as well as the dog."}

    @staticmethod
    def test_api_get_record_invalid_id():
        result = TestLibraryAPIClass.get_api_request("http://webapi/record/-1")
        assert result.status_code == 400
        assert result.json() == {"error": "This is not a valid ID!"}

    @staticmethod
    def test_api_get_record_non_existant_id():
        result = TestLibraryAPIClass.get_api_request("http://webapi/record/400")
        assert result.status_code == 404
        assert result.json()["title"] == "Not Found"

    @staticmethod
    def test_api_post():
        data = {"id": 0, "fact": "This is api test post adding new fact!"}
        headers = {"Content-type": "application/json"}
        result = TestLibraryAPIClass.post_api_request("http://webapi/insert", data, headers)
        assert result.status_code == 201
        assert result.json() == {"id": 358, "fact": "This is api test post adding new fact!"}
        result2 = TestLibraryAPIClass.get_api_request("http://webapi/record/358")
        assert result2.status_code == 200
        assert result2.json() == {"id": 358, "fact": "This is api test post adding new fact!"}

    @staticmethod
    def test_api_post_no_id():
        data = {"fact": "This is an api test post no id!"}
        headers = {"Content-type": "application/json"}
        result = TestLibraryAPIClass.post_api_request("http://webapi/insert", data, headers)
        assert result.status_code == 201
        assert result.json() == {"id": 359, "fact": "This is an api test post no id!"}
        result2 = TestLibraryAPIClass.get_api_request("http://webapi/record/359")
        assert result2.status_code == 200
        assert result2.json() == {"id": 359, "fact": "This is an api test post no id!"}

    @staticmethod
    def test_api_post_with_id():
        data = {"id": 1, "fact": "This is an api test post with id!"}
        headers = {"Content-type": "application/json"}
        result = TestLibraryAPIClass.post_api_request("http://webapi/insert", data, headers)
        assert result.status_code == 400
        assert result.json() == {"error": "ID should not exist!"}

    @staticmethod
    def test_api_post_with_invalid_id():
        data = {"id": -1, "fact": "This is an api test post with invalid id!"}
        headers = {"Content-type": "application/json"}
        result = TestLibraryAPIClass.post_api_request("http://webapi/insert", data, headers)
        assert result.status_code == 400
        assert result.json() == {"error": "ID should not exist!"}

    @staticmethod
    def test_api_post_with_non_existant_id():
        data = {"id": 400, "fact": "This is an api test post with non exsitant id!"}
        headers = {"Content-type": "application/json"}
        result = TestLibraryAPIClass.post_api_request("http://webapi/insert", data, headers)
        assert result.status_code == 400
        assert result.json() == {"error": "ID should not exist!"}

    @staticmethod
    def test_api_put():
        result = TestLibraryAPIClass.get_api_request("http://webapi/record/3")
        assert result.status_code == 200
        assert result.json() == {"id": 3, "fact": "Small quantities of grapes and raisins can cause renal failure in dogs. Chocolate, macadamia nuts, cooked onions, or anything with caffeine can also be harmful."}
        data = {"id": 3, "fact": "This is an api test put with id!"}
        headers = {"Content-type": "application/json"}
        result2 = TestLibraryAPIClass.put_api_request("http://webapi/update/3", data, headers)
        assert result2.status_code == 200
        assert result2.json() == {"id": 3, "fact": "This is an api test put with id!"}
        result3 = TestLibraryAPIClass.get_api_request("http://webapi/record/3")
        assert result3.status_code == 200
        assert result3.json() == {"id": 3, "fact": "This is an api test put with id!"}

    @staticmethod
    def test_api_put_invalid_id():
        result = TestLibraryAPIClass.get_api_request("http://webapi/record/2")
        assert result.status_code == 200
        assert result.json() == {"id": 2, "fact": "Ancient Egyptians revered their dogs. When a pet dog would die, the owners shaved off their eyebrows, smeared mud in their hair, and mourned aloud for days."}
        data = {"id": 2, "fact": "This is an api test put with id!"}
        headers = {"Content-type": "application/json"}
        result2 = TestLibraryAPIClass.put_api_request("http://webapi/update/-1", data, headers)
        assert result2.status_code == 400
        assert result2.json() == {"error": "This is not a valid ID!"}
        result3 = TestLibraryAPIClass.get_api_request("http://webapi/record/2")
        assert result3.status_code == 200
        assert result3.json() == {"id": 2, "fact": "Ancient Egyptians revered their dogs. When a pet dog would die, the owners shaved off their eyebrows, smeared mud in their hair, and mourned aloud for days."}

    @staticmethod
    def test_api_put_non_existant_id():
        result = TestLibraryAPIClass.get_api_request("http://webapi/record/2")
        assert result.status_code == 200
        assert result.json() == {"id": 2, "fact": "Ancient Egyptians revered their dogs. When a pet dog would die, the owners shaved off their eyebrows, smeared mud in their hair, and mourned aloud for days."}
        data = {"id": 2, "fact": "This is an api test put with id!"}
        headers = {"Content-type": "application/json"}
        result2 = TestLibraryAPIClass.put_api_request("http://webapi/update/400", data, headers)
        assert result2.status_code == 400
        assert result2.json() == {"error": "Provided ID does not match Body ID!"}
        result3 = TestLibraryAPIClass.get_api_request("http://webapi/record/2")
        assert result3.status_code == 200
        assert result3.json() == {"id": 2, "fact": "Ancient Egyptians revered their dogs. When a pet dog would die, the owners shaved off their eyebrows, smeared mud in their hair, and mourned aloud for days."}

    @staticmethod
    def test_api_put_no_id():
        data = {"fact": "This is an api test put with id!"}
        headers = {"Content-type": "application/json"}
        result = TestLibraryAPIClass.put_api_request("http://webapi/update/2", data, headers)
        assert result.status_code == 400
        assert result.json() == {"error": "Provided ID does not match Body ID!"}

    @staticmethod
    def test_api_put_no_fact():
        data = {"id": 2}
        headers = {"Content-type": "application/json"}
        result = TestLibraryAPIClass.put_api_request("http://webapi/update/2", data, headers)
        assert result.status_code == 400
        assert result.json()["errors"] == {"Fact": ["The Fact field is required."]}

    @staticmethod
    def test_api_delete():
        result = TestLibraryAPIClass.delete_api_request("http://webapi/delete/1")
        assert result.status_code == 204
        result2 = TestLibraryAPIClass.get_api_request("http://webapi/record/1")
        assert result2.status_code == 404
        assert result2.json()["title"] == "Not Found"

    @staticmethod
    def test_api_delete_invalid_id():
        result = TestLibraryAPIClass.delete_api_request("http://webapi/delete/-1")
        assert result.status_code == 400
        assert result.json() == {"error": "This is not a valid ID!"}

    @staticmethod
    def test_api_delete_non_existant_id():
        result = TestLibraryAPIClass.delete_api_request("http://webapi/delete/400")
        assert result.status_code == 404
        assert result.json()["title"] == "Not Found"
