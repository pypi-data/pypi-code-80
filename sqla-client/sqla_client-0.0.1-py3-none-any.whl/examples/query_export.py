import click
import requests
from sqla_client import SQLA

template = u"""/*
Name: {name}
Data source: {data_source}
Created By: {created_by}
Last Updated At: {last_updated_at}
*/
{query}"""


def save_queries(queries):
    for query in queries:
        filename = "query_{}.sql".format(query["id"])
        with open(filename, "w") as f:
            content = template.format(
                name=query["name"],
                data_source=query["data_source_id"],
                created_by=query["user"]["name"],
                last_updated_at=query["updated_at"],
                query=query["query"],
            )
            f.write(content)


@click.command()
@click.argument("sqla_url")
@click.option(
    "--pat",
    "pat",
    required=True,
    envvar="SQLA_USER_PAT",
    show_envvar=True,
    prompt="PAT",
    help="User Personal Access Token",
)
def main(sqla_url, pat):
    client = SQLA(sqla_url, pat)
    queries = client.paginate(client.queries)
    save_queries(queries)


if __name__ == "__main__":
    main()
