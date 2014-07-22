"""
Video classes
"""

import logging
import magic

from galaxy import eggs
eggs.require( "bx-python" )


import data

log = logging.getLogger(__name__)

# Currently these supported binary data types must be manually set on upload

class Video( data.Data ):
    pass

class Mp4( Video ):
    file_ext = "mp4"

    def sniff(self, filename):
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            return m.id_filename(filename) is 'video/mp4'

class Flv( Video ):
    file_ext = "mp4"

    def sniff(self, filename):
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            return m.id_filename(filename) is 'video/x-flv'
