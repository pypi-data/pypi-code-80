#!/usr/bin/env python

import click
import httpx


@click.command()
@click.version_option()
def main():

    pass

    # TODO
    with httpx.Client() as client:
        pass
        config = {"username": "admin_customer14378", "password": "password123", "custom_uri": "test"}
        # PersonResource(client, config)


if __name__ == '__main__':
    main()
