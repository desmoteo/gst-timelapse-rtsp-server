import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Gstreamer Timelapse RTSP Server",
    version="0.0.1",
    author="Matteo Ferrabone",
    author_email="matteo.ferrabone@gmail.com",
    description="Utility for serving a timelapse over RTSP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/desmoteo/gst-timelapse-rtsp-server",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
)
