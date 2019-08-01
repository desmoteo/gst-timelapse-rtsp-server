import begin

from GstTimelapseRtspServer.Servers import GstTimelapseServer

@begin.start
def main(folder):

    gts = GstTimelapseServer(folder)

    gts.run()

    print('Bye')
