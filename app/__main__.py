import sys

import app.useeio.main
import app.arguments

if __name__ == '__main__':
    args = app.arguments.parse(sys.argv[1:])

    commands = {
        "run": app.useeio.main.run,
    }

    commands[args.command](args)
