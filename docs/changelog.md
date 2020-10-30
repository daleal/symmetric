---
layout: content
title: Change Log
permalink: /changelog/
---

# Change Log

## [3.4.3](https://github.com/daleal/symmetric/releases/tag/3.4.3) - 30-10-2020

### End of life

`symmetric` has reached its end of life! 💀 But don't worry! You can use its spiritual successor, [`asymmetric`](https://github.com/daleal/asymmetric). Its API is almost identical! You can learn more on the `README.md` file!

### Changed

- Changed a bunch of stuff for the documentation
- Added a **disclaimer** section to warn about the project's status

### Fixed

- Fixed documentation bug that happened when no default parameters existed on a decorated function.

## [3.4.2](https://github.com/daleal/symmetric/releases/tag/3.4.2) - 26-03-2020

### Added

- Added a landing page to the website
- Added a deprecation warning to markdown documentation generator

### Changed

- Change "slogan"

### Fixed

- Fixed mobile navbar to include a 5th element

## [3.4.1](https://github.com/daleal/symmetric/releases/tag/3.4.1) - 23-03-2020

### Added

- Added a `--version (-v)` flag to the CLI to get `symmetric`'s version
- Added a Change Log to the documentation
- Added some assets to the project

### Changed

- Change documentation's navbar

## [3.4.0](https://github.com/daleal/symmetric/releases/tag/3.4.0) - 22-03-2020

### Added

- Complete docs can now be located at a [dedicated webpage](https://symmetric.one/docs/)

### Changed

- Changed `README.md` file to include only necessary documentation

## [3.3.0](https://github.com/daleal/symmetric/releases/tag/3.3.0) - 21-03-2020

### Added

- Added methods to change the default authentication token names

### Changed

- Now the `Symmetric` class is named `_Symmetric` and it's a _singleton_ class

## [3.2.0](https://github.com/daleal/symmetric/releases/tag/3.2.0) - 20-03-2020

### Changed

- Change function handling to allow normal underlying module usage (that includes calling and testing functions)
- Modularized CLI code

### Fixed

- Fixed function testing capabilities (see the _Changed_ section of this release)

## [3.1.0](https://github.com/daleal/symmetric/releases/tag/3.1.0) - 16-03-2020

### Added

- Added a `/docs` endpoint to enter through the browser and access **auto-generated interactive** [ReDoc](https://github.com/Redocly/redoc) documentation

### Changed

- API token is now received inside the request header instead of the request body
- The auto-generated OpenAPI compliant documentation now includes the API token requirement
- Refactor OpenAPI spec generator

## [3.0.0](https://github.com/daleal/symmetric/releases/tag/3.0.0) - 15-03-2020

### Added

- Added [OpenAPI specification](https://swagger.io/docs/specification/about/) compliant auto-documentation feature

### Changed

- Change default `HTTP` method from `GET` to `POST` to allow OpenAPI documentation out of the box, making it incompatible with previous `symmetric` versions

## [2.1.1](https://github.com/daleal/symmetric/releases/tag/2.1.1) - 01-03-2020

### Changed

- Changed badges style
- Changed badge positions
- Change workflow name

## [2.1.0](https://github.com/daleal/symmetric/releases/tag/2.1.0) - 01-03-2020

### Changed

- Changed every `URL` occurance to `route`
- Move logging config to its own file
- Change CLI utilities to its own file

## [2.0.0](https://github.com/daleal/symmetric/releases/tag/2.0.0) - 29-02-2020

### Added

- Added a _regex_ to allow only certain _paths_, making it incompatible with previous `symmetric` versions
- Added tests for helper methods
- Added a GitHub workflow to automatically run the tests

## [1.6.2](https://github.com/daleal/symmetric/releases/tag/1.6.2) - 28-02-2020

### Added

- Added downloads per month badge to the `README.md` file

### Changed

- Updated metadata

## [1.6.1](https://github.com/daleal/symmetric/releases/tag/1.6.1) - 28-02-2020

### Changed

- Added authentication token feature to the `README.md` file

## [1.6.0](https://github.com/daleal/symmetric/releases/tag/1.6.0) - 27-02-2020

### Added

- Added native token authentication support
- Added a custom error for authentication failures

### Changed

- Change short description and symmetric router parameters in `README.md` file

## [1.3.0](https://github.com/daleal/symmetric/releases/tag/1.3.0) - 25-02-2020

### Added

- Added an argument filter for the function call

### Changed

- Minor changes to the linter rules

## [1.2.3](https://github.com/daleal/symmetric/releases/tag/1.2.3) - 25-02-2020

### Fixed

- Fix an error that would cause the `run` command from the `symmetric` CLI to fail when spawned

## [1.2.2](https://github.com/daleal/symmetric/releases/tag/1.2.2) - 24-02-2020

### Added

- Added `poetry` back as the dependency manager, builder and publisher engine

### Fixed

- The CLI now won't fail if the `symmetric` command is called without an argument

## [1.2.1](https://github.com/daleal/symmetric/releases/tag/1.2.1) - 24-02-2020

### Added

- Added a _Why Symmetric?_ section to the `README.md` file

### Changed

- Minor changes in installation instructions.

### Fixed

- Fixed some _typos_.

## [1.2.0](https://github.com/daleal/symmetric/releases/tag/1.2.0) - 23-02-2020

### Added

- Added a CLI to auto run the `flask` development server
- Added API auto documentation

### Changed

- Removed `poetry`

## [1.1.1](https://github.com/daleal/symmetric/releases/tag/1.1.1) - 23-02-2020

### Added

- Added linters and a workflow to lint the repository

### Fixed

- Correct badge URL typo

## [1.0.0](https://github.com/daleal/symmetric/releases/tag/1.0.0) - 22-02-2020

### Added

- Added a Pull Request template

### Changed

- Change the `router` method and the `app` object into a single object called `symmetric`, making it incompatible with previous `symmetric` versions

## [0.0.5](https://github.com/daleal/symmetric/releases/tag/0.0.5) - 21-02-2020

### Added

- Added full example of `symmetric` usage
- Added `setup.cfg` file

### Fixed

- Change manual deployment documentation

## [0.0.4](https://github.com/daleal/symmetric/releases/tag/0.0.4) - 21-02-2020

Initial release
