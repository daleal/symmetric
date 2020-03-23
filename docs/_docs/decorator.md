---
layout: documentation
title: The Decorator
permalink: /docs/decorator/
---

# The Decorator

The module consists of a main object called `symmetric`, which includes an important element: the `router` decorator. This chapter documents its functionality.

```py
from symmetric import symmetric

@symmetric.router("/some-route", methods=["post"], response_code=200, auth_token=False)
```

The decorator recieves 4 arguments: the `route` argument (the endpoint of the API to which the decorated function will map), the `methods` argument (a list of the methods accepted to connect to that endpoint, defaults in only `POST` requests), the `response_code` argument (the response code of the endpoint if everything goes according to the plan. Defaults to `200`) and the `auth_token` argument (a boolean stating if the endpoint requires authentication using a `symmetric` token. Defaults to `False`).

## Defining the API endpoints

On the [basic usage](/docs/basic-usage/) chapter we saw that a simple method could be transformed into an API endpoint with this example:

```py
@symmetric.router("/sample", methods=["get"])
def some_function():
    """Greets the world."""
    return "Hello World!"
```

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

This will generate an `POST` endpoint reachable at `/add` that recieves an `a` key and, optionally, a `b` key inside the `json` request body and returns the sum of both numbers.

Note that no two endpoints can exist with the same route. If this happens, `symmetric` will raise an `DuplicatedRouteError` exception. Also note that there are certain [route rules](/docs/route-rules) that must be followed. Failing to follow those rules will result in `symmetric` raising an `IncorrectRouteFormatError` exception.

### Querying API endpoints

To give parameters to a function, all we need to do is send a `json` body with the names of the parameters as keys. Let's see how! Run `symmetric run module` and send a `POST` request (the default `HTTP` method) to `http://127.0.0.1:5000/add`, now using the `requests` module. You can use the following snippet:

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

## The `symmetric` token authentication

To speed up your API creation even more, `symmetric` includes native support for a simple token authentication.

**Disclaimer**: **never** use the `symmetric` token in production without enforcing `HTTPS`. The token travels inside the header of the request, so it wil be visible to **anyone** sniffing the traffic in your network.

With that out of the way, let's get started! The token works like this:

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

### Changing the default token names

Note that you can change the default **client** token name and **server** token name. To change the **client** token name, run the following command at the start of your module:

```py
symmetric.set_client_token_name("new_client_token_name")
```

After that, the key of the token in every request header must be `new_client_token_name`.

To change the **server** token name, run the following command at the start of your module:

```py
symmetric.set_server_token_name("NEW_SERVER_TOKEN_NAME")
```

After that, the key of the token in the server environment must be `NEW_SERVER_TOKEN_NAME`.

If the value given to `set_client_token_name` is not a string or is an empty string, `symmetric` will raise an `InvalidTokenNameError` exception.
