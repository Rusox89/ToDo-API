# ToDo-API

## The task at hand

Build an API service in Flask to manage a simple To-Do list.
The application provides APIs only. There is no web UI or client application for this service, only a stand alone service with RESTful APIs.

The application must be able to

 - Use username and password (or equivalent) to log in users
 - Use cookies (or effective alternative) to authenticate all API requests
 - Create a new todo item (containing a text description)
 - List a user’s set of todo items
 - Mark any single todo item as completed
 - Delete any single todo item
 - Log a user out
 - Run using Python 3.6 or higher
 - Use JSON for data exchange

Considerations:
 - Creation of new users is out of scope.  The set of users can be hardcoded (at least one user)
 - The APIs should be RESTful
 - A quick, sure and repeatable proof that every element of the code works as intended, should be delivered alongside the service
 - Any libraries and frameworks can be used as long as they are publically available or included with the code.
 - No time restrictions are set, however, we expect this to be completed in a reasonable timeframe


## Installation requirements

The service is dockerized and so you will need to install Docker first to be able to run it, after installing Docker you will need to install `docker-compose`. Refer to docker official docs on how to do so for each of the linux distributions.

For Debian/Ubuntu users:

`sudo apt-get install -y docker.io`
`sudo pip3 install docker-compose`

## How to run

The project contains it's own `docker-compose.yml` where all the services are described, a test container is used as an entrypoint to execute the tests, more on this is explained below.

To run the stack just use

`docker-compose -f docker/docker-compose.yml up`


## How to run the tests

The tests can be run using the below command whilst the stack is up an running (including the test container)

`docker exec docker_tests_1 python /app/tests/main.py`


## How to use

To use the API you will need some credentials at first, those credentials are

- Email: root@localhost
- Password: toor

This will set a cookie, and for this reason it is recommended to use `requests.session` as it will handle the cookie managment for you as long as you keep using the same session to make requests after login.

To login you will need to hit the login endpoint, the snippet below show you how.

```python
>>> from requests import session
>>> s = session()
>>> s.post(
...  'http://localhost:5000/auth/login',
...  json={
...   'email': 'root@localhost',
...   'password': 'toor'
...  }
... )
<Response [200]>
```

Now you are logged in, after this you can add new todo entries, to do so you can use the snipped below using the same session

```python
>>> s.post(
...  'http://localhost:5000/todo/entry',
...  json={
...   'title': 'My interview tech task',
...   'description': 'Design a ToDo API with user managment',
...   'completed': False
...  }
... )
<Response [201]>
```

Now we can retrieve the tasks to be completed by listing all of the ones belonging to the user logged in

```python
>>> task_list = s.get(
...  'http://localhost:5000/todo/entry',
...  json={}
... )
>>> task_list
<Response [200]>
>>> import json
>>> print(json.dumps(task_list.json(), indent=4))
[
    {
        "description": "Design a ToDo API with user managment",
        "userid": 1,
        "entryid": 178,
        "completed": false,
        "title": "My interview tech task"
    }
]
```

Now we are going to mark it as completed

```python
>>> task = s.put(
...  'http://localhost:5000/todo/entry/{}'.format(str(eid)),
...  json={
...   'completed': True
...  }
... )
>>> task
<Response [200]>
>>> print(json.dumps(task.json(), indent=4))
{
    "description": "Design a ToDo API with user managment",
    "userid": 1,
    "entryid": 178,
    "completed": true,
    "title": "My interview tech task"
}
```

And now that it is completed we do not need to keep it right?

```python
>>> s.delete(
...  'http://localhost:5000/todo/entry/{}'.format(str(eid)),
...  json={}
... )
<Response [200]>
```

Also do not forget to logout


```python
>>> s.get(
...  'http://localhost:5000/auth/logout',
...  json={}
... )
<Response [200]>
```
