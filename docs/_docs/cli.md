---
layout: documentation
title: CLI
permalink: /docs/cli/
---

# Command Line Interface

You've already learned how to use the command line interface to do some things. This chapter documents all the available commands.

To get help from the command line, simply run `symmetric -h` to see the complete list of commands, then `-h` combined with any of those can give you more information.

## Global Options

- `--help (-h)`: Display help information and exit.
- `--version (-v)`: Display `symmetric`'s version number and exit.

## `run`

This command will start `flask`'s **development** server.

```bash
symmetric run <module>
```

It will search for the `symmetric` object inside `<module>`. Failing to find it will result in `symmetric` raising an `AppImportError` exception. **Do not use this in production**. The `Flask` server is meant for development only. Instead, you can use any `WSGI` server to run the API. For example, to run the API using [gunicorn](https://gunicorn.org/), you just need to run `gunicorn module:symmetric` and a production ready server will be spawned (you can treat the `symmetric` object as a `WSGI` object).

By default, the server will run in `127.0.0.1:5000` and in debug mode.

### Options

- `--help (-h)`: Display help information and exit.
- `--server <server> (-s <server>)`: Specify the server hostname in which the application will run.
- `--port <port> (-p <port>)`: Specify the port in which the webserver will listen.
- `--no-debug (-d)`: Do not run in debug mode.

## `docs`

This command will generate documentation for the API.

```bash
symmetric docs <module>
```

It will search for the `symmetric` object inside `<module>`. Failing to find it will result in `symmetric` raising an `AppImportError` exception.

By default, this will **automagically** generate a `json` file named `openapi.json` documenting the API with an OpenAPI specification. Seems too simple to be true, right? Go ahead, try it yourself! Also, don't be afraid of using **[type annotations](https://docs.python.org/3/library/typing.html)**... The annotations will be documented too! They will restrict the parameter types within the OpenAPI generated `json`!

~~Using the `--markdown` flag will result in a markdown file named `documentation.md` documenting each endpoint with the function docstring, required arguments and more data about that endpoint.~~ **Important Note**: This feature is still supported, but it is **deprecated**. It will not receive updates and will probably be removed in favor of the more standard and complete **OpenAPI documentation** on some major release.

### Options

- `--help (-h)`: Display help information and exit.
- `--filename <filename> (-f <filename>)`: Specify the name of the file in which the documentation will be written.
- ~~`--markdown (-m)`: Generate simpler, human-readable Markdown documentation.~~ **Deprecated**
