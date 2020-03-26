---
layout: documentation
title: Basic Usage
permalink: /docs/basic-usage/
---

# Basic Usage

For the basic usage introduction we will be wrapping a simple _hello world_ function into an API.

## Installation

Install using pip!

```bash
pip install symmetric
```

Once installed, you should be able to get the version number from the CLI:

```bash
symmetric --version
```

If you see something like `symmetric version 3.4.2`, then you are ready to use `symmetric`.

## Running the development server

To start the development server, just run:

```bash
symmetric run <module>
```

Where `<module>` is your module name (in the examples, we will be writing in a file named `example.py`, so the module name will be just `example`). A `Flask` instance will be spawned immediately and can be reached at [http://127.0.0.1:5000](http://127.0.0.1:5000) by default. **Do not use this in production**. The `Flask` server is meant for development only. Instead, you can use any `WSGI` server to run the API. For example, to run the API using [gunicorn](https://gunicorn.org/), you just need to run `gunicorn example:symmetric` and a production ready server will be spawned.

## Wrapping a function

Now let's imagine that we have the following method:

```py
def some_function():
    """Greets the world."""
    return "Hello World!"
```

To transform that method into an API endpoint, all you need to do is add two lines:

```py
from symmetric import symmetric

@symmetric.router("/sample", methods=["get"])
def some_function():
    """Greets the world."""
    return "Hello World!"
```

The first line imports the `symmetric` object into the file and the second line transforms the function into an API endpoint reachable at `/sample`.

## It just works.

Run `symmetric run example` and send a `GET` request to `http://127.0.0.1:5000/sample`. You should get a `Hello World!` in response! (To try it with a browser, make sure to run the above command and click [this link](http://127.0.0.1:5000/sample)).

Crazy, right? That's just **the start** of what `symmetric` can do, so keep on reading the documentation!
