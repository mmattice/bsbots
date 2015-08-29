import sys

from twisted.internet import stdio, reactor
from twisted.protocols import basic

class ClientBase(basic.LineReceiver):
    delimiter = '\n'
    fh = sys.stderr

    def lineReceived(self, line):
        messageparts = line.split('|')[1:-1]
        msgtype = messageparts[0].lower()
        msgkey = messageparts[1].lower()
        assert(messageparts[-1] == 'END')
        arguments = messageparts[2:-1]

        try:
            method = getattr(self,
                             ''.join(('do_', msgtype,
                                      '_', msgkey.replace(' ', '_'))
        except:
            print >>self.fh, "Cannot find method for %s %s %s" %
                                     (msgtype, msgkey, arguments)
        else:
            try:
                print >>self.fh, "calling %s with %s" % (method, arguments)
                method(*arguments)
            except Exception, e:
                print >>self.fh, "Exception %s" % e

    def send(self, msgtype, *data):
        lineparts = ['', 'RESPONSE', msgtype]
        lineparts.extend(data)
        lineparts.extend(( 'END', ''))
        self.sendLine('|'.join(lineparts))

    def do_info_end_game(self):
        self.transport.loseConnection()

    def connectionLost(self, reason):
        self.fh.close()
        reactor.stop()

    def do_info_grid_size(self, gridsize):
        width, height = map(int, gridsize.split())
        self.grid_width = width
        self.grid_height = height

    def do_info_num_ships(self, num_ships):
        self.num_ships = int(num_ships)

    def do_info_ship_sizes(self, *args):
        self.ship_sizes = (int(x) for x in args)

    def do_query_shots(self, str_num_shots):
        self.get_shots(int(str_num_shots))

    def get_shots(self, count):
        raise NotImplementedError()

    def do_query_ship_locations(self):
        self.get_ship_locations()

    def get_ship_locations(self):
        raise NotImplementedError()
