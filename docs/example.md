---
layout: content
title: Example
permalink: /docs/example/
---

# The Whole Example

In this documentation, some example code was given. The whole example can be found in this page. We will be assuming that the code is inside a file called `example.py`.

## Original file without `symmetric`

the original `example.py` file looked like this before `symmetric`:

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

## Modified file with `symmetric`

The complete final `example.py` file with `symmetric` should look like this:

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

Finally, to run the server, just run `symmetric run example`. Now, you can send `POST` requests to `http://127.0.0.1:5000/add` and `GET` requests to `http://127.0.0.1:5000/sample` and `http://127.0.0.1:5000/secret`.

## Querying the API

Here is a simple file to get you started querying your API:

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

## The `/docs` endpoint

The `/docs` endpoint would look something like this:

![](/assets/images/example-redoc.png)

## OpenAPI documentation

Running `symmetric docs example` would result in a file `openapi.json` being created with the following content:

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "Example API",
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

## ~~Markdown documentation~~

**Important Note**: This feature is still supported, but it is **deprecated**. It will not receive updates and will probably be removed in favor of the more standard and complete **OpenAPI documentation** on some major release.

Running `symmetric docs example --markdown` would result in a file `documentation.md` being created with the following content:

``````pandoc
# Example API Documentation

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
