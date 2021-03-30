import argparse
import logging

from .extractor import PostgresqlExtractor, PostgresqlRunConfig

logging.basicConfig(
    format="%(asctime)s %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PostgreSQL metadata extractor")
    for parameter in PostgresqlRunConfig.parameters():
        parser.add_argument(parameter, metavar=parameter, type=str, help=parameter)
    args = parser.parse_args()

    extractor = PostgresqlExtractor()
    extractor.run(config=args)
