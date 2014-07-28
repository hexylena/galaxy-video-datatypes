"""
Video classes
"""

import logging
import magic
import subprocess, re

import data
from galaxy.datatypes.binary import Binary
from galaxy.datatypes.metadata import MetadataElement
log = logging.getLogger(__name__)

# Currently these supported binary data types must be manually set on upload

#class Video( data.Data ):
class Video( Binary ):

    MetadataElement( name="resolution_x", default=0, desc="Width of video stream", readonly=True, visible=True, optional=True, no_value=0 )
    MetadataElement( name="resolution_y", default=0, desc="Height of video stream", readonly=True, visible=True, optional=True, no_value=0 )
    MetadataElement( name="fps", default=0, desc="FPS of video stream", readonly=True, visible=True, optional=True, no_value=0 )

    def _get_resolution(self, filename):
        video_stream = re.compile(r'Stream #(?P<str_maj>\d+)\.(?P<str_min>\d+).*: Video: (?P<vid_codec>[^,]*), (?P<colorspace>[^,]*), (?P<resx>\d+)x(?P<resy>\d+) [^,]*, (?P<data_rate>\d+) (?P<data_rate_unit>.b/s), (?P<fps>\d+) fps')
        audio_stream= re.compile(r'Stream #(?P<str_maj>\d+)\.(?P<str_min>\d+).*: Audio: (?P<audio_codec>[^,]*), (?P<freq>\d+)Hz, (?P<channels>[^,]+), [^,]*, (?P<data_rate>\d+) (?P<data_rate_unit>.b/s)')
        #Input #0, mov,mp4,m4a,3gp,3g2,mj2, from '/home/esr/Documents/galaxy-galaxy-dist-d3b1f484c4b6/Juli - Elektrisches Gefhl-ft8DwXUxaB8.mp4':
        #Metadata:
            #major_brand     : mp42
            #minor_version   : 0
            #compatible_brands: isommp42
            #creation_time   : 2014-03-07 06:55:07
        #Duration: 00:03:43.81, start: 0.000000, bitrate: 555 kb/s
            #Stream #0.0(und): Video: h264 (Constrained Baseline), yuv420p, 480x360 [PAR 1:1 DAR 4:3], 457 kb/s, 25 fps, 25 tbr, 25 tbn, 50 tbc
            #Stream #0.1(und): Audio: aac, 44100 Hz, stereo, s16, 95 kb/s
            #Metadata:
            #creation_time   : 2014-03-07 06:55:07


        p = subprocess.Popen(['ffmpeg', '-i', filename],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        match = video_stream.search(stderr)
        if match:
            x = match.group('resx')
            y = match.group('resy')
            fps = match.group('fps')
        else:
            x = y = fps = 0
        return x, y, fps

    def set_meta(self, dataset, **kwd):
        (x, y, fps) = self._get_resolution( dataset.file_name )
        dataset.metadata.resolution_y = y
        dataset.metadata.resolution_x = x
        dataset.metadata.fps = fps

class Mp4( Video ):
    file_ext = "mp4"

    def sniff(self, filename):
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            return m.id_filename(filename) is 'video/mp4'
#Binary.register_unsniffable_binary_ext("mp4")

class Flv( Video ):
    file_ext = "flv"

    def sniff(self, filename):
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            return m.id_filename(filename) is 'video/x-flv'

Binary.register_unsniffable_binary_ext("flv")
