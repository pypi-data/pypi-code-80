#!/usr/bin/env python3

'''
main module;
'''

import os
import sys
import json
import argparse
import jinja2

##  program name;
prog = 'jinja-renderer'

def render_template(template_name, search_path, **template_vars):
    """
    Renders an arbitrary Jinja2 template.

    Args:
        template_name: Name of the template used for rendering the template.
        search_path: Search-path for where this template is located.
        template_vars: A dict containing all template variables that should be used for rendering the template.
    """
    template = _get_jinja2_template(search_path, template_name)
    return template.render(**template_vars)


def _get_jinja2_template(search_path, template_name):
    """
    Returns a jinja2 template by a given name and a given search path.

    Args:
        search_path: Directory where the template exists.
        template_name: Name of the template.

    Returns:
        Jinja2 template-object.
    """
    loader = jinja2.FileSystemLoader(searchpath=search_path)
    env = jinja2.Environment(loader=loader)
    # These two following lines trims whitespaces and empty lines
    env.trim_blocks = True
    env.lstrip_blocks = True
    return env.get_template(template_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--template", required=True, help="Path to the jinja template")
    parser.add_argument("-v", "--variables", required=True,
                        help="May be a string as a JSON which represents the key-value pairs to use for rendering the template. Example (must be on this format; note the double-quotes): -v '{\"VERSION\": \"1.0\"}'. May also be a path to a JSON file that describes a set of variables.")
    parser.add_argument("-d", "--destination", required=True, help="Path to where the rendered template will go")

    args = parser.parse_args()

    print(f"Template: {args.template}")
    print(f"Variables: {args.variables}")
    print(f"Destination: {args.destination}")

    try:
        variables = json.loads(args.variables)
    except Exception as load_exception:
        if not os.path.exists(args.variables):
            print(f"Failed to load variables as a dict and {args.variables} does not appear to be a file either.")
            sys.exit(1)
        else:
            try:
                variables = json.loads(open(args.variables).read())
            except Exception as e:
                print(f"Failed to load contents in file {args.variables}")
                sys.exit(1)

    template_dir, template_file = str(args.template).rsplit("/", 1)
    template = _get_jinja2_template(template_dir, template_file)

    rendered_file = render_template(template_file, template_dir, **variables)
    with open(args.destination, "w") as f:
        f.write(rendered_file)


if __name__ == '__main__':
    main()
