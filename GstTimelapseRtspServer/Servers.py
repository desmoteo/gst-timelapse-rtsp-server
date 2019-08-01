import sys
import os
import time
import re
import cv2
import glob

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import GObject, Gst, GstVideo, GstRtspServer

from .Generators import SampleGenerator

class GstTimelapseServer:
    def __init__(self, folder, ext='/*.jpg', fps=15, delta=1, width=1920, height=1080, service='9994', endpoint='timelapse', format='GRAY8'):
        # GObject.threads_init()
        Gst.init(None)

        self.width = width
        self.height = height
        self.service = service
        self.endpoint = endpoint
        self.format = format

        self.mainloop = GObject.MainLoop()

        self.server = GstRtspServer.RTSPServer()

        self.mounts = self.server.get_mount_points()

        self.factory = GstRtspServer.RTSPMediaFactory()
        self.factory.set_launch(
            '( appsrc name=vidsrc ! videoconvert !  x264enc pass=5 quantizer=22 speed-preset=4 profile=1 ! rtph264pay name=pay0  )')

        self.mounts.add_factory('/{0}'.format(endpoint), self.factory)
        self.server.set_service(service)
        self.server.attach(None)

        images = sorted(glob.glob(folder + ext))

        self.s = SampleGenerator(fps, images, delta=delta)
        self.factory.connect('media-configure', GstTimelapseServer.media_configure, self)
        print('Liesening on: {0}:{1}'.format(
            self.server.get_address(), self.server.get_bound_port()))

    def run(self):
        self.mainloop.run()

    @staticmethod
    def media_configure(factory, media, me):
        element = GstRtspServer.RTSPMedia.get_element(media)
        src_v = Gst.Bin.get_by_name_recurse_up(element, 'vidsrc')
        caps = Gst.Caps.from_string(
            'video/x-raw,format=(string){0},width={1},height={2},framerate=30/1'.format(me.format, me.width, me.height))
        src_v.set_property('caps', caps)
        src_v.set_property('format', Gst.Format.TIME)
        src_v.connect('need-data', me.s.needdataGrey)


