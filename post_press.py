# -*- coding: utf-8 -*-
from locust import HttpLocust, TaskSet, task,between
import json

header = {
    "User-Agent": "Mozilla/5.0"
}

data = {
    "test_msg": "hello world",
}


class ReplayAction(TaskSet):

    @task
    def postPressTest(self):
        try:

            url = "/test/post"

            with self.client.post(url=url, data=data, headers=header,name="postPressTest", catch_response=True) as response:

                if response.status_code != 200:
                    response.failure("Failed")
                print(response.content.decode("utf-8"))
                result = json.loads(response.content.decode("utf-8"))
                # print(result)
                if result["result_code"] == 600008:
                    response.success()
                else:
                    response.failure(result["result_code"])

        except Exception as e:
            print("捕获的异常:{}".format(e))


class RePlayer(HttpLocust):
    #min_wait = 5
    #max_wait = 5
    wait_time = between(0, 0)
    host = "http://127.0.0.1:8081"
    task_set = ReplayAction
