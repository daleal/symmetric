# Symmetric

![PyPI - Version](https://img.shields.io/pypi/v/symmetric?style=for-the-badge&logo=python&color=306998&logoColor=%23fff&label=version)
![PyPI - Downloads](https://img.shields.io/pypi/dm/symmetric?style=for-the-badge&logo=python&color=306998&logoColor=%23fff)

A powerful yet lean wrapper over **[Flask](https://github.com/pallets/flask)** to massively speed up **[API](https://en.wikipedia.org/wiki/Web_API)** creations and enable super fast module-to-**[API](https://en.wikipedia.org/wiki/Web_API)** transformations.

![Tests Workflow](https://img.shields.io/github/workflow/status/daleal/symmetric/tests?label=tests&logo=github&style=for-the-badge)
![Linters Workflow](https://img.shields.io/github/workflow/status/daleal/symmetric/linters?label=linters&logo=github&style=for-the-badge)

## Why Symmetric?

Raw developing speed and ease of use, that's why. While `Flask` is a powerful tool to have, getting it to work from scratch can be a bit of a pain, especially if you have never used it before. The idea behind `symmetric` is to be able to take any module **already written** and transform it into a working API in a matter of minutes, instead of having to design the module ground-up to work with `Flask` (it can also be used to build an API from scratch really fast). With `symmetric`, you will also get some neat features, namely:

- Auto logging.
- Server-side error detection and exception handling.
- Native support for an authentication token on a per-endpoint basis.
- Auto-generated `/docs` endpoint for your API with **interactive documentation**.
- Auto-generated [OpenAPI Specification](https://swagger.io/docs/specification/about/) and Markdown documentation files for your API.

The [complete documentation](https://symmetric.one/docs/basic-usage/) is available on the [official website](https://symmetric.one/).

## Installing

Install using pip!

```bash
pip install symmetric
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

@symmetric.router("/some-route", methods=["post"], response_code=200, auth_token=False)
```

The decorator recieves 4 arguments: the `route` argument (the endpoint of the API to which the decorated function will map), the `methods` argument (a list of the methods accepted to connect to that endpoint, defaults in only `POST` requests), the `response_code` argument (the response code of the endpoint if everything goes according to the plan. Defaults to `200`) and the `auth_token` argument (a boolean stating if the endpoint requires authentication using a `symmetric` token. Defaults to `False`).

Now let's imagine that we have the following method:

```py
def some_function():
    """Greets the world."""
    return "Hello World!"
```

To transform that method into an API endpoint, all you need to do is add one line:

```py
@symmetric.router("/sample", methods=["get"])
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

### Querying API endpoints

To give parameters to a function, all we need to do is send a `json` body with the names of the parameters as keys. Let's see how! Run `symmetric run module` and send a `POST` request (the default `HTTP` method) to `http://127.0.0.1:5000/add`, now using the `requests` module.

```python
import requests

payload = {
    "a": 48,
    "b": 21
}
response = requests.post("http://127.0.0.1:5000/add", json=payload)
print(response.json())
```

We got a `69` response! (`48 + 21 = 69`). Of course, you can return dictionaries from your methods and those will get returned as a `json` body in the response object **automagically**!

With this in mind, you can transform any existing project into a usable API very quickly!

## ReDoc Documentation

By default, you can `GET` the `/docs` endpoint (using a browser) to access to **interactive auto-generated documentation** about your API. It will include request bodies for each endpoint, response codes, authentication required, default values, and much more!

**Tip**: Given that the [ReDoc Documentation](https://github.com/Redocly/redoc) is based on the OpenAPI standard, using **type annotations** in your code will result in a more detailed interactive documentation. Instead of the parameters being allowed to be any type, they will be forced into the type declared in your code. Cool, right?

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

Test install:

```bash
poetry install  # will also install the symmetric CLI
```

Run the tests:

```bash
python -m unittest
```

## Resources

- [Official Website](https://symmetric.one/)
- [Issue Tracker](https://github.com/daleal/symmetric/issues/)
