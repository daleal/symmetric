"""
A module to route the CLI traffic.
"""

import sys
import argparse

import symmetric.cli_utils


def dispatcher():
    """
    Main CLI method, recieves the command line action and dispatches it to
    the corresponding method.
    """
    parser = generate_parser()

    args = parser.parse_args()

    try:
        if args.action == "run":
            symmetric.cli_utils.start_server(
                args.module, args.server, args.port, args.debug
            )
        elif args.action == "docs":
            symmetric.cli_utils.document_api(args.module, args.filename)
    except AttributeError:
        print("An argument is required for the symmetric command.")
        parser.print_help()
        sys.exit(1)


def generate_parser():
    """Generates the CLI parser for the module."""
    # Create parser
    parser = argparse.ArgumentParser(
        description="Command line interface tool for symmetric."
    )

    # In order to allow the CLI utility grow, the parser will include an
    # initial argumment to determine which subparser will be executed.

    # Create subparsers
    subparsers = parser.add_subparsers(help="Action to be executed.")

    # Runner parser
    generate_runner_subparser(subparsers)

    # Documentation parser
    generate_documentation_subparser(subparsers)

    return parser


def generate_runner_subparser(subparsers):
    """Generates the subparser for the run server option."""
    runner_parser = subparsers.add_parser("run")
    runner_parser.set_defaults(action="run")

    # Module name
    runner_parser.add_argument(
        "module",
        metavar="module",
        help="Name of the module that uses the symmetric object."
    )

    # Host
    runner_parser.add_argument(
        "-s", "--server",
        dest="server",
        default="127.0.0.1",
        help="Server hostname in which the application will run."
    )

    # Port
    runner_parser.add_argument(
        "-p", "--port",
        dest="port",
        type=int,
        default=5000,
        help="Port for the webserver."
    )

    # Debug
    runner_parser.add_argument(
        "-d", "--no-debug",
        dest="debug",
        action='store_const',
        default=True,  # debug is set to True by default
        const=False,   # if the flag is used, sets debug to False
        help="Do not run in debug mode."
    )


def generate_documentation_subparser(subparsers):
    """Generates the subparser for the auto-documentation option."""
    documentation_parser = subparsers.add_parser("docs")
    documentation_parser.set_defaults(action="docs")

    # Module name
    documentation_parser.add_argument(
        "module",
        metavar="module",
        help="Name of the module that uses the symmetric object."
    )

    # Filename
    documentation_parser.add_argument(
        "-f", "--filename",
        dest="filename",
        default="documentation.md",
        help="Name of the file in where to write the documentation."
    )


if __name__ == "__main__":
    dispatcher()
