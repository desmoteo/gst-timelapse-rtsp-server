import time
from PIL import Image
import numpy as np
from gi.repository import GObject, Gst, GstVideo, GstRtspServer

class SampleGenerator:

    def __init__(self, fps, images, delta=5):
        self._last_t_v = -31337
        self._last_t_frame = -31337

        self.dts = 0

        self.fps = int(fps)
        self.images = images
        self.cnt = 0
        self.delta = delta
        self.image0 = None
        self.image1 = None

    def needdataGrey(self, src, length):

        t = time.time()
        if t - self._last_t_frame >= self.delta:
            self.cnt = self.cnt+1
            self._last_t_frame = t
            self.image0 = Image.open(self.images[self.cnt]).convert('L')
            self.image1 = Image.open(self.images[self.cnt+1]).convert('L')
        imageblend = Image.blend(
            self.image0, self.image1, (t - self._last_t_frame)/self.delta)
        data = np.array(imageblend).astype(np.uint8)
        self._last_t_v = t

        data = data.tostring()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        #buf = Gst.Buffer.new_wrapped(data.tostring())
        assert buf is not None
        buf.fill(0, data)
        buf.pts = buf.dts = self.dts
        self.dts = self.dts + (1.0/self.fps) * 1000000000.0
        buf.duration = (1.0/self.fps) * 1000000000.0
        # time.sleep((1.0/30.))
        src.emit('push-buffer', buf)

    def needdata(self, src, length):

        t = time.time()
        if t - self._last_t_frame >= self.delta:
            self.cnt = self.cnt+1
            self._last_t_frame = t
            self.image0 = Image.open(self.images[self.cnt])
            self.image1 = Image.open(self.images[self.cnt+1])
        imageblend = Image.blend(
            self.image0, self.image1, (t - self._last_t_frame)/self.delta)
        data = np.array(imageblend.convert('YCbCr')).astype(
            np.uint8).reshape((1920, 1080, 3))
        self._last_t_v = t
        print(data.size)
        y = data[..., 0]
        u = data[..., 1]
        v = data[..., 2]

        data = y.tostring() + u.tostring() + v.tostring()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        #buf = Gst.Buffer.new_wrapped(data.tostring())
        assert buf is not None
        buf.fill(0, data)
        buf.pts = buf.dts = self.dts
        self.dts = self.dts + (1.0/self.fps) * 1000000000.0
        buf.duration = (1.0/self.fps) * 1000000000.0
        # time.sleep((1.0/30.))
        src.emit('push-buffer', buf)