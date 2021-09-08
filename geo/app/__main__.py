import sys

import app.gis_db.builder
import app.arguments

if __name__ == "__main__":
    args = app.arguments.parse(sys.argv[1:])

    commands = {
        "serve": app.gis_db.builder.run,
    }

    commands[args.command](args)
