from __future__ import annotations

import json
import os
import sys

import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from todolist.main import app  # noqa


class CommandException(Exception):
    EXIT_CODE = 1


@click.command(help="Generate swagger file.")
@click.option(
    "-o",
    "--output-file",
    "output_file_path",
    default="swagger.json",
    help=(
        "The path of the output file, this file is used to generate a OpenAPI file for "
        "use in the development process. (Default value: swagger.json)"
    ),
)
def main(output_file_path: str) -> None:
    try:
        swagger_dict = app.openapi()
        with open(output_file_path, mode="w") as f:
            f.write(json.dumps(swagger_dict, indent=4))

    except CommandException as e:
        sys.exit(e.EXIT_CODE)


if __name__ == "__main__":
    main()
