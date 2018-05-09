Need install
```
apt-get install redis-server mysql-server
```

RUN:
```
python app.py
```

RUN TASK:

```
import time
import random


def main():
    time.sleep(random.randint(0, 10))
```

Task in `config.py`

```
DRWEB_TASK = 'task.main'
```


REST API DESCRIPTION:

ADD TASK

POST: http://0.0.0.0:8080/api/tasks/

{
    "process": "-",
    "exec_time": "-",
    "task_id": "3fe52d63-d9fc-42f7-8424-f9b755159921",
    "start_time": "-",
    "create_time": "2018.05.09 16:30:16.537410",
    "status": "In Queue"
}

GET LIST

GET: http://0.0.0.0:8080/api/tasks/

[
    {
        "create_time": "2018.05.09 16:19:21.000000",
        "exec_time": 8.00787,
        "process": "Process-1",
        "start_time": "2018.05.09 16:19:21.000000",
        "status": "Completed",
        "task_id": "01768f62-37ac-449a-b752-8c05eccfcdbe"
    },
    {
        "create_time": "2018.05.09 14:54:03.000000",
        "exec_time": "-",
        "process": "-",
        "start_time": "-",
        "status": "In Queue",
        "task_id": "0290a131-d2ca-44cc-badc-0526327994b8"
    },

 ...

]

GET ITEM

GET: http://0.0.0.0:8080/api/tasks/3fe52d63-d9fc-42f7-8424-f9b755159921/

[
    {
        "create_time": "2018.05.09 16:30:16.537410",
        "exec_time": 9.00695,
        "process": "Process-2",
        "start_time": "2018.05.09 16:30:16.538431",
        "status": "Completed",
        "task_id": "3fe52d63-d9fc-42f7-8424-f9b755159921"
    }
]