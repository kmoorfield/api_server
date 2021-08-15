import time
from datetime import datetime, timezone
import json
from locust import HttpUser, task, between

class TestLoadClass(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_first_record(self):
        self.client.get("/first")

    @task
    def get_last_record(self):
        self.client.get("/last")

    @task
    def get_random_record(self):
        self.client.get("/random")

    @task
    def get_all_records(self):
        self.client.get("/all")

    @task
    def get_specific_record(self):
        self.client.get("/record/52")

    @task
    def post_record(self):
        created_record = self.client.post("/insert", json={"id": 0, "fact":"This is a new fact!"})
        time.sleep(1)
        id = created_record.json()["id"]
        self.client.delete(f"/delete/{id}")
        time.sleep(1)

    @task
    def put_update_record(self):
        random_record = self.client.get("/random")
        id = random_record.json()["id"]
        datetime_string = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
        response = self.client.put(f"/update/{id}", json={"id": id, "fact": f"This is an updated fact! Updated at {datetime_string}"}, catch_response=True)

        if response.status_code == 404:
            response.success()
        elif response.status_code == 200:
            response.success()
        else:
            response.failure(response.content)

        time.sleep(1)