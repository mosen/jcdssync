from typing import Union, Optional
from urllib.parse import urlparse
import jss


class SyncOperation:

    def __init__(
            self,
            source: str,
            destination: str,
            delete: bool=False,
            username: Optional[str]=None,
            password: Optional[str]=None):


        # self.source = source
        # self.destination = destination
        # self.delete = delete
        #
        # source_parsed = urlparse(source)
        # if source_parsed.scheme == 'https':
        #     self.source_is_jss = True
        # else:
        #     self.source_is_jss = False
        #
        # dest_parsed = urlparse(destination)
        # if dest_parsed.scheme == 'https':
        #     self.dest_is_jss = True
        # else:
        #     self.dest_is_jss = False

        self._jss = jss.JSS(
            url=source,
            user=username,
            password=password,
        )

        c = jss.Casper(self._jss)
        c.update()

        print(c)
