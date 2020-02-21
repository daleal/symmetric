# Symmetric

A simple wrapper over **[Flask](https://github.com/pallets/flask)** to speed up basic API deployments.

## Why Symmetric?

While `Flask` is a powerful tool to have, getting it to work from scratch can be a bit of a pain, specially if you have never used it before. The idea behind `Symmetric` is to be able to take any module and transform it into a working API, instead of having to design the module ground-up to work with `Flask`.

## Installing

Install using pip!

```bash
pip install --user symmetric
```

## Usage

```py
from symmetric import router, app
```

The module consists of two main objects: the `router` decorator and the `app` object. Let's start with the `app` object:

```py
if __name__ == '__main__':
    app.run()
```

Add that code to one of your modules. Then, run `python module.py`. A `Flask` instance will be spawned immediately and can be reached at [http://127.0.0.1:5000](http://127.0.0.1:5000). We don't have any endpoints yet, so we'll add some (given that `app` is a `Flask` object, any `WGSI` server can be used to run the API, [gunicorn](https://gunicorn.org/) is a good example).

Let's now analyze our `router` decorator:

```py
@router("/some-route", methods=["get"], response_code=200)
```

The decorator recieves 3 arguments: the `route` argument (the endpoint of the API to which the decorated function will map), the `methods` argument (a list of the methods accepted to connect to that endpoint, defaults in only `GET` requests) and the `response_code` argument (the response code of the endpoint if everything goes according to the plan. Defaults to `200`).

Now let's imagine that we have the following method:

```py
def some_function():
    return "Hello World!"
```

To transform that method into an API endpoint, all you need to do is add one line:

```py
@router("/sample")
def some_function():
    return "Hello World!"
```

Run `python module.py` and send a `GET` request to `http://127.0.0.1:5000/sample`. You should get a `Hello World!` in response! (To try it with a browser, just click [this link](http://127.0.0.1:5000/sample)).

But what about methods with arguments? Of course they can be API'd too! Let's now say that you have the following function:

```py
def another_function(a, b):
    return a + b
```

To transform that method into an API endpoint, all you need to do, again, is add one line:

```py
@router("/add")
def another_function(a, b):
    return a + b
```

To give the parameters to the function, all we need to do is send a `json` body with the name of the parameters as key. Let's see how! Run `python module.py` and send a `GET` request to `http://127.0.0.1:5000/add`, now using the `requests` module.

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

Build the project:

```bash
poetry build
```

Push to `TestPyPi`:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi
```

Download from `TestPyPi`:

```bash
deactivate
rm -rf .testing-venv
python3 -m venv .testing-venv
. .testing-venv/bin/activate
python -m pip install --index-url https://test.pypi.org/simple/ symmetric
```

Push to `PyPi`:

```bash
poetry publish
```