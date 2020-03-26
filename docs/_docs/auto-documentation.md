---
layout: documentation
title: Auto Documentation
permalink: /docs/auto-documentation/
---

# Automatic Docs

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

## ReDoc Documentation

By default, you can `GET` the `/docs` endpoint (using a browser) to access the **interactive auto-generated documentation** about your API. It will include request bodies for each endpoint, response codes, authentication required, default values, and much more!

![](/assets/images/example-redoc.png)

**Tip**: Given that the [ReDoc Documentation](https://github.com/Redocly/redoc) is based on the OpenAPI standard, using **type annotations** in your code will result in a more detailed interactive documentation. Instead of the parameters being allowed to be any type, they will be forced into the type declared in your code. Cool, right?
