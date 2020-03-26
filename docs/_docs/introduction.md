---
layout: documentation
title: Introduction
permalink: /docs/
---

# Symmetric

A powerful tool to enable super fast module-to-**[API](https://en.wikipedia.org/wiki/Web_API)** transformations. Learn in minutes, implement in seconds. Batteries included.

`symmetric` is a lean wrapper over **[Flask](https://github.com/pallets/flask)**, with **much less hassle** and some **very neat features**.

## Why Symmetric?

Raw developing speed and ease of use, that's why. While `Flask` is a powerful tool to have, getting it to work from scratch can be a bit of a pain, especially if you have never used it before. Do you have a machine learning model that you would like to use as a web service but don't want to spend **hours** learning how to build APIs? You can stop searching! The idea behind `symmetric` is to be able to take any module **already written** and transform it into a working API in a matter of seconds, instead of having to design the module ground-up to work with `Flask` (it can also be used to build an API from scratch really fast).

## Cool Features

`symmetric` includes some cool features to **massivley** add value to your API with **no need** for you to think about it! With `symmetric` you get:

- Automatic server logging.
- Server-side error detection and exception handling.
- Auto-generated `/docs` endpoint for your API with **interactive documentation**.
- Native support for an **authentication token** on a per-endpoint basis.
- Auto-generated [OpenAPI Specification](https://swagger.io/docs/specification/about/) ~~and Markdown documentation files~~ for your API.

## Just two lines of code!

Import the `symmetric` object, wrap your function with a decorator and you are all set. No need for additional configuration, no need to document your API... Yes, that's right! Never again worry about documenting your API's endpoints, `symmetric` does that for you! In fact, here's am example of the auto-generated interactive documentation:

![](/assets/images/example-redoc.png)
