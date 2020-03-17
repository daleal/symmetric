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

### The `symmetric` token authentication

To speed up your API creation even more, `symmetric` includes native support for a simple token authentication. **Disclaimer**: **never** use the `symmetric` token in production without enforcing `HTTPS`. The token travels inside the header of the request, so it wil be visible to **anyone** sniffing the traffic in your network. The token works like this:

1. **Set up the token in the server.**

    In the environment where your API is going to run, add an environmental variable named `SYMMETRIC_API_KEY` and set its value to be the _[pre-shared](https://en.wikipedia.org/wiki/Pre-shared_key)_ token. If you don't set the environmental key, the _default_ `SYMMETRIC_API_KEY` value will be `symmetric_token` (in your development environment that's probably fine, but in the production server you should **never** use the default value of the `symmetric` token).

2. **Force one of your endpoints to use an authentication token.**

    Let's say your module has a method like this:

    ```py
    def secret_function():
        """Greets the world (secretly)."""
        return "Hello World in secret!"
    ```

    Add the `symmetric` router decorator in the following manner:

    ```py
    @symmetric.router("/secret", methods=["get"], auth_token=True)
    def secret_function():
        """Greets the world (secretly)."""
        return "Hello World in secret!"
    ```

    Now, your endpoint won't respond to any request that is not correctly authenticated.

3. **Query your endpoint.**

    To query your endpoint, the request headers must include a key named `symmetric_api_key` with a value to match the one of the environment's `SYMMETRIC_API_KEY`. So, for instance, if you are using the default `SYMMETRIC_API_KEY` value (`symmetric_token`), the request headers for the `/secrets` endpoint should be:

    ```py
    headers = {
        "symmetric_api_key": "symmetric_token"
    }
    ```

    By sending that payload in the request headers, the endpoint can be accessed correctly.

### Auto-generating the API documentation

Generating API documentation is simple with `symmetric`. Just run the following command:

```bash
symmetric docs <module>
```

This will **automagically** generate a `json` file documenting the API with an OpenAPI specification. Seems too simple to be true, right? Go ahead, try it yourself! Also, don't be afraid of using **[type annotations](https://docs.python.org/3/library/typing.html)**... The annotations will be documented too! They will restrict the parameter types within the OpenAPI generated `json`!

You can also generate a more simple and human-readable documentation file with the `-m` or the `--markdown` flag.

```bash
symmetric docs <module> --markdown
```

This will also **automagically** generate a markdown file documenting each endpoint with the function docstring, required arguments and more data about that endpoint.

You can also specify the name of the documentation file (defaults to `openapi.json` for the default documentation and to `documentation.md` for the markdown documentation) using the `-f` or the `--filename` flag.

### ReDoc Documentation

By default, you can `GET` the `/docs` endpoint (using a browser) to access to **interactive auto-generated documentation** about your API. It will include request bodies for each endpoint, response codes, authentication required, default values, and much more!

**Tip**: Given that the [ReDoc Documentation](https://github.com/Redocly/redoc) is based on the OpenAPI standard, using **type annotations** in your code will result in a more detailed interactive documentation. Instead of the parameters being allowed to be any type, they will be forced into the type declared in your code. Cool, right?

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


def secret_function():
    """Greets the world (secretly)."""
    return "Hello World in secret!"
```

The complete final `module.py` file with `symmetric` should look like this:

```py
from symmetric import symmetric


@symmetric.router("/sample", methods=["get"])
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


@symmetric.router("/secret", methods=["get"], auth_token=True)
def secret_function():
    """Greets the world (secretly)."""
    return "Hello World in secret!"
```

To run the server, just run `symmetric run module`. Now, you can send `POST` requests to `http://127.0.0.1:5000/add` and `GET` requests to `http://127.0.0.1:5000/sample` and `http://127.0.0.1:5000/secret`. Here is a simple file to get you started querying your API:

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
    response = requests.post("http://127.0.0.1:5000/add", json=payload)
    return response.json()


def call_secret():
    headers = {
        "symmetric_api_key": "symmetric_token"
    }
    response = requests.get("http://127.0.0.1:5000/secret", headers=headers)
    return response.text


if __name__ == '__main__':
    print(call_sample())
    print(call_add())
    print(call_secret())
```

Running `symmetric docs module` would result in a file `openapi.json` being created with the following content:

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "Module API",
    "version": "0.0.1"
  },
  "paths": {
    "/add": {
      "post": {
        "description": "Adds :a and :b and returns the result of\nthat operation.",
        "responses": {
          "200": {
            "$ref": "#/components/responses/SuccesfulOperation"
          },
          "500": {
            "$ref": "#/components/responses/InternalError"
          }
        },
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "a": {
                    "oneOf": [
                      {
                        "type": "string"
                      },
                      {
                        "type": "number"
                      },
                      {
                        "type": "integer"
                      },
                      {
                        "type": "boolean"
                      },
                      {
                        "type": "array"
                      },
                      {
                        "type": "object"
                      }
                    ]
                  },
                  "b": {
                    "oneOf": [
                      {
                        "type": "string"
                      },
                      {
                        "type": "number"
                      },
                      {
                        "type": "integer"
                      },
                      {
                        "type": "boolean"
                      },
                      {
                        "type": "array"
                      },
                      {
                        "type": "object"
                      }
                    ],
                    "default": 372
                  }
                },
                "additionalProperties": false
              }
            }
          }
        }
      }
    },
    "/sample": {
      "get": {
        "description": "Greets the world.",
        "responses": {
          "200": {
            "$ref": "#/components/responses/SuccesfulOperation"
          },
          "500": {
            "$ref": "#/components/responses/InternalError"
          }
        }
      }
    },
    "/secret": {
      "post": {
        "description": "Greets the world (secretly).",
        "responses": {
          "200": {
            "$ref": "#/components/responses/SuccesfulOperation"
          },
          "500": {
            "$ref": "#/components/responses/InternalError"
          },
          "401": {
            "$ref": "#/components/responses/UnauthorizedError"
          }
        },
        "security": [
          {
            "APIKeyAuth": []
          }
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "APIKeyAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "symmetric_api_key"
      }
    },
    "responses": {
      "SuccesfulOperation": {
        "description": "Successful operation"
      },
      "UnauthorizedError": {
        "description": "Invalid or non-existent authentication credentials."
      },
      "InternalError": {
        "description": "Unexpected internal error (API method failed, probably due to a missuse of the underlying function)."
      }
    }
  }
}
```

Running `symmetric docs module --markdown` would result in a file `documentation.md` being created with the following content:

``````pandoc
# Module API Documentation

Endpoints that require an authentication token should send it in a key named `symmetric_api_key` inside the request headers.

## `/add`

### Description

Adds :a and :b and returns the result of
that operation.

### Metadata

`HTTP` methods accepted: `POST`

Does not require an authentication token.

### Parameters

```py
{
    a,
    b,  # defaults to 372
}
```

## `/sample`

### Description

Greets the world.

### Metadata

`HTTP` methods accepted: `GET`

Does not require an authentication token.

### Parameters

No required parameters.

## `/secret`

### Description

Greets the world (secretly).

### Metadata

`HTTP` methods accepted: `GET`

Requires an authentication token.

### Parameters

No required parameters.

``````

## Logging

By default, the logs in the server will be written into the `stdout` and into a file named `symmetric.log`. You can change the name of the file by specifying the `LOG_FILE` environmental variable, if you want to.

## Route rules

There are some rules regarding the correct routes that can be used. Failing to follow the `symmetric` route rules will result in the API not being run and an error being thrown and logged. To follow the rules, a route:

1. **Can't** be defined twice.
2. **Can't** have repetitions of `/`, `-` or `_`.
3. **Can't** have concatenations of `/` with `-` or of `_` with `-`.
4. **Can't** include characters other than letters (uppercase and/or lowercase), `/`, `-` and `_`.
5. **Can't** end with a `/`, a `-` or a `_`. The **only** exception of this rule is when the route is just `/`, in which case, it **can** end with `/`.
6. **Must** start with a `/`.

Here are some examples.

### Correct route patterns

- `/`
- `/symmetric`
- `/hi/hello`
- `/hello-world/basic_syntax`
- `/_element/BIGelement`

### Incorrect route patterns

- `/hi//hello`
- `element`
- `/another-element/`
- `/bad-_composition`
- `/-worse`
- `/element__two`
- `/element2`
- `/oof-number-one-`
- `/oof_number_two_`

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
