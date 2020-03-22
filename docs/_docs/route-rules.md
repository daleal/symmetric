---
layout: documentation
title: Route Rules
permalink: /docs/route-rules/
---

# Route Rules

There are some rules regarding the correct routes that can be used. Failing to follow the `symmetric` route rules will result in the API not being run and an error being thrown and logged. To follow the rules, a route:

1. **Can't** be defined twice.
2. **Can't** have repetitions of `/`, `-` or `_`.
3. **Can't** have concatenations of `/` with `-` or of `_` with `-`.
4. **Can't** include characters other than letters (uppercase and/or lowercase), `/`, `-` and `_`.
5. **Can't** end with a `/`, a `-` or a `_`. The **only** exception of this rule is when the route is just `/`, in which case, it **can** end with `/`.
6. **Must** start with a `/`.

Here are some examples.

## Correct route patterns

- `/`
- `/symmetric`
- `/hi/hello`
- `/hello-world/basic_syntax`
- `/_element/BIGelement`

## Incorrect route patterns

- `/hi//hello`
- `element`
- `/another-element/`
- `/bad-_composition`
- `/-worse`
- `/element__two`
- `/element2`
- `/oof-number-one-`
- `/oof_number_two_`
