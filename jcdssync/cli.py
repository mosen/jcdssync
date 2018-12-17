import os
import argparse
from jcdssync.sync import SyncOperation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("-u", "--username", help="JAMF Pro API Username", default=os.getenv("JSS_USER"))
    parser.add_argument("-p", "--password", help="JAMF Pro API Password", default=os.getenv("JSS_PASSWORD"))
    parser.add_argument("-d", "--delete", help="Delete extraneous files in destination", action="store_true")
    args = parser.parse_args()

    op = SyncOperation(args.source, args.destination)
    op.sync()


if __name__ == '__main__':
    main()
