"""This script runs flask app programmatically in order to use debugger"""
import os
import argparse

from app import app

def main(args):
    if args.production:
        os.environ['FLASK_ENV'] = 'production'
    else:
        os.environ['FLASK_ENV'] = 'development'

    if args.hostall:
        host = "0.0.0.0"
    else:
        host = "127.0.0.1"

    app.run(debug=args.debug, host=host, port=args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='sum the integers at the command line')
    parser.add_argument('--production', type=bool, default=False, help='enable production mode')
    parser.add_argument('--debug', type=bool, default=True, help='enable debug mode')
    parser.add_argument('--hostall', type=bool, default=True, help='host globally accessible')
    parser.add_argument('--port', type=int, default=5100, help='port to connect to')
    args = parser.parse_args()

    main(args)
