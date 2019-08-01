# gst-timelapse-rtsp-server
Serves an RTSP stream of a timelapse obtained from static images.

## Basic Usage

Start a server as follows, where "path to folder" is the path to a folder containing the images you want to use in the timelapse stream: 

```python
from GstTimelapseRtspServer.Servers import GstTimelapseServer


gts = GstTimelapseServer("path to folder")

gts.run()
```

play the stream:

```bash
ffplay rtsp://localhost:9994/timelapse
```
