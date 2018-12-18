from __future__ import print_function
from typing import Union, Optional, Tuple, List
from urllib.parse import urlparse
import jss
from xml.etree import ElementTree
import os.path
import logging
from jss.distribution_point import JCDS, FileRepository
import requests
import hashlib

# From, To
CopyOperation = Tuple[str, str]
CopyOperations = List[CopyOperation]


def block_generator(handle, block_size=65536):
    """Generator func which iterates through the contents of a file using a given block size."""
    with handle:
        block = handle.read(block_size)
        while len(block) > 0:
            yield block
            block = handle.read(block_size)


logger = logging.getLogger(__name__)


class SyncOperation:

    def __init__(
            self,
            source: str,
            destination: str,
            delete: bool=False,
            username: Optional[str]=None,
            password: Optional[str]=None):

        source_url = urlparse(source)
        if source_url.scheme == 'https' or source_url.scheme == 'http':
            # Assume JAMF Cloud if given a URL
            self.jss = jss.JSS(
                url=source,
                user=username,
                password=password,
                ssl_verify=False,
            )
            self.source = JCDS(jss=self.jss)
        elif source_url.scheme == '' or source_url.scheme == 'file':
            # Assume source is a local directory
            self.source = source

        dest_url = urlparse(destination)
        if dest_url.scheme == 'https' or dest_url.scheme == 'http':
            # Assume JAMF Cloud if given a URL
            self.jss = jss.JSS(
                url=destination,
                user=username,
                password=password,
                ssl_verify=False,
            )
            self.source = JCDS(jss=self.jss)
        elif dest_url.scheme == '' or dest_url.scheme == 'file':
            # Assume dest is a local directory
            self.destination = destination

    def scan(self):  # type: () -> CopyOperations
        """Scan for a list of files to copy by pruning from the source list files which have the same
        name and checksum.

        The result is a list of tuples which is aliased as `CopyOperations`."""
        operations = list()

        src_pkgs = self.source.package_index_using_casper()

        for p in src_pkgs:
            destination_filename = os.path.join(self.destination, p['filename'])

            # Missing in destination? just download/upload
            if not os.path.exists(destination_filename):
                operations.append((p['fileURL'], destination_filename,))
                continue

            # Confirm checksum is valid, if not, overwrite
            hasher = hashlib.md5()
            for block in block_generator(open(destination_filename, 'rb')):
                hasher.update(block)

            if hasher.hexdigest() != p['checksum']:
                logger.info("checksum mismatch in filename: %s, source=%s, destination=%s", p['filename'],
                            p['checksum'], hasher.hexdigest())
                operations.append((p['fileURL'], destination_filename,))
            else:
                logger.debug("checksum match in filename: %s", p['filename'])

        return operations

    def run(self, operations):  # type: (CopyOperations) -> None
        """Execute download/upload operations."""
        for (source, dest) in operations:
            logging.debug("Fetching from source: %s", source)
            response = requests.get(source)
            logging.debug("Writing to destination filename: %s", dest)
            with open(dest, 'wb') as fd:
                fd.write(response.content)




