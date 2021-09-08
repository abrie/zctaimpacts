import argparse


def parse(args):
    parser = argparse.ArgumentParser(
        description="Sustainable Communities Hackathon 2021"
    )
    subparser = parser.add_subparsers(dest="command", required=True)
    parser_0 = subparser.add_parser("serve", description="Starts the webserver")
    parser_0.add_argument(
        "--db", dest="db", default="db.sqlite3", type=str, help="Name of the database"
    )
    return parser.parse_args(args)
