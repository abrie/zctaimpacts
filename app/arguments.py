import argparse


def parse(args):
    parser = argparse.ArgumentParser(
        description="Sustainable Communities Hackathon 2021 Prototype")
    subparser = parser.add_subparsers(
        dest="command", required=True)
    parser_scrape = subparser.add_parser(
        'run', description="Run the prototype")
    parser_scrape.add_argument(
        '--secrets', required=True, dest="secrets", default=None, type=argparse.FileType('r', encoding='UTF-8'), help="Contains required secrets")
    return parser.parse_args(args)
