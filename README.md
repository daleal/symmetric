# Symmetric

![](https://github.com/daleal/symmetric/workflows/linters/badge.svg)

A simple wrapper over **[Flask](https://github.com/pallets/flask)** to speed up basic **[API](https://en.wikipedia.org/wiki/Web_API)** deployments.

## Why Symmetric?

While `Flask` is a powerful tool to have, getting it to work from scratch can be a bit of a pain, specially if you have never used it before. The idea behind `symmetric` is to be able to take any module and transform it into a working API, instead of having to design the module ground-up to work with `Flask`. With `symmetric`, you will also get some neat features, namely:

- Auto logging.
- Server-side error detection and exception handling.
- Auto-generated documentation for your API.

## Installing

Install using pip!

```bash
pip install --user symmetric
```

## Usage

### Running the development server

To start the development server, just run:

```bash
symmetric run <module>
```

Where `<module>` is your module name (in the examples, we will be writing in a file named `module.py`, so the module name will be just `module`). A `Flask` instance will be spawned immediately and can be reached at [http://127.0.0.1:5000](http://127.0.0.1:5000) by default. We don't have any endpoints yet, so we'll add some later. **Do not use this in production**. The `Flask` server is meant for development only. Instead, you can use any `WSGI` server to run the API. For example, to run the API using [gunicorn](https://gunicorn.org/), you just need to run `gunicorn module:symmetric` and a production ready server will be spawned.

### Defining the API endpoints

The module consists of a main object called `symmetric`, which includes an important element: the `router` decorator. Let's analyze it:

```py
from symmetric import symmetric

@symmetric.router("/some-route", methods=["get"], response_code=200)
```

The decorator recieves 3 arguments: the `route` argument (the endpoint of the API to which the decorated function will map), the `methods` argument (a list of the methods accepted to connect to that endpoint, defaults in only `GET` requests) and the `response_code` argument (the response code of the endpoint if everything goes according to the plan. Defaults to `200`).

Now let's imagine that we have the following method:

```py
def some_function():
    """Greets the world."""
    return "Hello World!"
```

To transform that method into an API endpoint, all you need to do is add one line:

```py
@symmetric.router("/sample")
def some_function():
    """Greets the world."""
    return "Hello World!"
```

Run `symmetric run module` and send a `GET` request to `http://127.0.0.1:5000/sample`. You should get a `Hello World!` in response! (To try it with a browser, make sure to run the above command and click [this link](http://127.0.0.1:5000/sample)).

But what about methods with arguments? Of course they can be API'd too! Let's now say that you have the following function:

```py
def another_function(a, b=372):
    """
    Adds :a and :b and returns the result of
    that operation.
    """
    return a + b
```

To transform that method into an API endpoint, all you need to do, again, is add one line:

```py
@symmetric.router("/add")
def another_function(a, b=372):
    """
    Adds :a and :b and returns the result of
    that operation.
    """
    return a + b
```

### Auto-generating the API documentation

Generating API documentation is simple with `symmetric`. Just run the following command:

```bash
symmetric docs <module>
```

This will **automagically** generate a markdown file documenting each endpoint with the function docstring, required arguments and `HTTP` methods. Seems too simple to be true, right? Go ahead, try it yourself!

You can also specify the name of the documentation file (defaults to `documentation.md`) using the `-f` or the `-filename` flag.

### Querying API endpoints

To give parameters to a function, all we need to do is send a `json` body with the names of the parameters as keys. Let's see how! Run `symmetric run module` and send a `GET` request to `http://127.0.0.1:5000/add`, now using the `requests` module.

```python
import requests

payload = {
    "a": 48,
    "b": 21
}
response = requests.get("http://127.0.0.1:5000/add", json=payload)
print(response.json())
```

We got a `69` response! (`48 + 21 = 69`). Of course, you can return dictionaries from your methods and those will get returned as a `json` body in the response object **automagically**!

With this in mind, you can transform any existing project into a usable API very quickly!

### The whole example

To sum up, if the original `module.py` file looked like this before `symmetric`:

```py
def some_function():
    """Greets the world."""
    return "Hello World!"


def another_function(a, b=372):
    """
    Adds :a and :b and returns the result of
    that operation.
    """
    return a + b
```

The complete final `module.py` file with `symmetric` should look like this:

```py
from symmetric import symmetric


@symmetric.router("/sample")
def some_function():
    """Greets the world."""
    return "Hello World!"


@symmetric.router("/add")
def another_function(a, b=372):
    """
    Adds :a and :b and returns the result of
    that operation.
    """
    return a + b
```

To run the server, just run `symmetric run module`. Now, you can send `GET` requests to `http://127.0.0.1:5000/sample` and `http://127.0.0.1:5000/add`. Here is a simple file to get you started querying your API:

```py
import requests


def call_sample():
    response = requests.get("http://127.0.0.1:5000/sample")
    return response.text


def call_add():
    payload = {
        "a": 48,
        "b": 21
    }
    response = requests.get("http://127.0.0.1:5000/add", json=payload)
    return response.json()


if __name__ == '__main__':
    print(call_sample())
    print(call_add())
```

Running `symmetric docs module` would result in a file `documentation.md` being created with the following content:

``````md
# Module API Documentation

## `/add`

### Description

`HTTP` methods accepted: `GET`

Adds :a and :b and returns the result of
that operation.

### Parameters

```py
{
    a,
    b,  # defaults to 372
}
```

## `/sample`

### Description

`HTTP` methods accepted: `GET`

Greets the world.

### Parameters

No required parameters.

``````

## Developing

Clone the repository:

```bash
git clone https://github.com/daleal/symmetric.git

cd symmetric
```

Recreate environment:

```bash
./environment.sh

. .venv/bin/activate
```

Build the project (install `wheel` first):

```bash
rm -rf dist
python setup.py sdist bdist_wheel
```

Test install:

```bash
deactivate
rm -rf .testing-venv
python3 -m venv .testing-venv
. .testing-venv/bin/activate
pip install click flask
pip install --editable .
```

Push to `TestPyPi`:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Download from `TestPyPi`:

```bash
deactivate
rm -rf .testing-venv
python3 -m venv .testing-venv
. .testing-venv/bin/activate
pip install click
python -m pip install --index-url https://test.pypi.org/simple/ symmetric
```

Push to `PyPi`:

```bash
twine upload dist/*
```
