from rdpy.protocol.rdp import rdp
from twisted.internet import reactor


class MyRDPFactory(rdp.ClientFactory):

    def __init__(self, username, password,domain):
        self._username = username
        self._password = password
        self._domain = domain
        self._security = rdp.SecurityLevel.RDP_LEVEL_SSL

    def clientConnectionLost(self, connector, reason):
        print(reason)
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed')
        reactor.stop()

    def buildObserver(self, controller, addr):
        controller.setUsername(self._username)
        controller.setPassword(self._password)
        controller.setDomain(self._domain)
        class MyObserver(rdp.RDPClientObserver):

            def onReady(self):
                """
                @summary: Call when stack is ready
                """
                # send 'r' key
                self._controller.sendKeyEventUnicode(ord(unicode("r", encoding="UTF-8")), True)
                # mouse move and click at pixel 200x200
                self._controller.sendPointerEvent(200, 200, 1, True)

            def onUpdate(self, destLeft, destTop, destRight, destBottom, width, height, bitsPerPixel, isCompress, data):
                """
                @summary: Notify bitmap update
                @param destLeft: xmin position
                @param destTop: ymin position
                @param destRight: xmax position because RDP can send bitmap with padding
                @param destBottom: ymax position because RDP can send bitmap with padding
                @param width: width of bitmap
                @param height: height of bitmap
                @param bitsPerPixel: number of bit per pixel
                @param isCompress: use RLE compression
                @param data: bitmap data
                """

            def onSessionReady(self):
                """
                @summary: Windows session is ready
                """

            def onClose(self):
                """
                @summary: Call when stack is close
                """

        return MyObserver(controller)




reactor.connectTCP("192.168.48.130", 3389, MyRDPFactory(username='lynulyq',domain='',password='12345678'))
reactor.run()