import os
import argparse
import logging
from jcdssync.sync import SyncOperation

logging.basicConfig()
logger = logging.getLogger("jcdssync")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("-u", "--username", help="JAMF Pro API Username", default=os.getenv("JSS_USER"))
    parser.add_argument("-p", "--password", help="JAMF Pro API Password", default=os.getenv("JSS_PASSWORD"))
    parser.add_argument("-d", "--delete", help="Delete extraneous files in destination", action="store_true")
    args = parser.parse_args()

    op = SyncOperation(args.source, args.destination, username=args.username, password=args.password)
    to_copy = op.scan()
    op.run(to_copy)


if __name__ == '__main__':
    main()
