import os
import argparse
import logging
from jcdssync.sync import SyncOperation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("-u", "--username", help="JAMF Pro API Username", default=os.getenv("JSS_USER"))
    parser.add_argument("-p", "--password", help="JAMF Pro API Password", default=os.getenv("JSS_PASSWORD"))
    parser.add_argument("-d", "--delete", help="Delete extraneous files in destination", action="store_true")
    args = parser.parse_args()

    logger = logging.getLogger("jcdssync")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    op = SyncOperation(args.source, args.destination, username=args.username, password=args.password, logger=logger)
    logger.info("Scanning for differences between the source and destination...")
    to_copy = op.scan()
    logger.info("There are %d file(s) to copy", len(to_copy))
    op.run(to_copy)


if __name__ == '__main__':
    main()
