"""Console script for nfe_parser."""
import argparse
import sys

# import requests

from nfe_parser import nfe_parser


def main():
    """Console script for nfe_parser."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("_", nargs="*")
    args = arg_parser.parse_args()
    print("Arguments: " + str(args._))

    url1 = (
        "https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx?"
        "p=43190275315333012115655100001061161048579172|2|1|1|"
        "C75202C1699F567ED4B92ED4007634E2FA6A68CF"
    )

    n = nfe_parser.parse_nfe_from_url(url1)
    print(n)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
