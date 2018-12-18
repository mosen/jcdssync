from __future__ import print_function
from typing import Union, Optional, Tuple, List, Dict
from urllib.parse import urlparse
import jss
import os.path
import logging
from jss.distribution_point import JCDS
import requests
import hashlib

# From, To
CopyOperation = Tuple[str, str]
CopyOperations = List[CopyOperation]
CasperDictOrPath = Union[str, Dict[str, str]]


def block_generator(handle, block_size=65536):
    """Generator func which iterates through the contents of a file using a given block size."""
    with handle:
        block = handle.read(block_size)
        while len(block) > 0:
            yield block
            block = handle.read(block_size)


logger = logging.getLogger(__name__)


def get_checksum(f):  # type: (CasperDictOrPath) -> str
    """Get the checksum from a filesystem path OR a dict containing a checksum"""
    if isinstance(f, str):
        hasher = hashlib.md5()
        for block in block_generator(open(f, 'rb')):
            hasher.update(block)

        return hasher.hexdigest()
    else:
        return f['checksum']


def needs_sync(a, b):  # type: (CasperDictOrPath, CasperDictOrPath) -> bool
    """Check whether the source file indicated by `a` needs to be synced to the location pointed to by `b`.

    The parameters of the function can be absolute paths to local files, or dicts containing information about a file
    that have been extracted from the Casper.jxml endpoint.

    :param (str or dict) a: Source file, absolute path (must exist) or dict
    :param (str or dict) b: Destination file, absolute path (may not exist) or dict
    """
    if isinstance(b, str):
        if not os.path.exists(b):
            return True

    b_digest = get_checksum(b)
    a_digest = get_checksum(a)

    return a_digest != b_digest


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

            if needs_sync(p, destination_filename):
                operations.append((p['fileURL'], destination_filename,))

        return operations

    def run(self, operations):  # type: (CopyOperations) -> None
        """Execute download/upload operations."""
        for (source, dest) in operations:
            logging.debug("Fetching from source: %s", source)
            response = requests.get(source)
            logging.debug("Writing to destination filename: %s", dest)
            with open(dest, 'wb') as fd:
                fd.write(response.content)




