import time
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
        self.client.post("/insert", json={"id": 0, "fact":"This is a new fact!"})
        time.sleep(1)

    @task
    def put_update_record(self):
        self.client.put("/update/50", json={"id": 50, "fact":"This is an updated fact!"})
        time.sleep(1)

    @task
    def delete_random_record(self):
        for item_id in range(2, 10):
            self.client.delete(f"/delete/{item_id}")
            time.sleep(1)
