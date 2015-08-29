from client_base import ClientBase

from twisted.internet import stdio, reactor

class SimpleClient(ClientBase):
    def __init__(self):

        # location of next shot to make
        self.shooting_x = 0
        self.shooting_y = 0

    ###################################################################
    def get_ship_locations(self):
        locations = []
        for y in range(self.num_ships):
            locations.append("{x} {y} {orientation}".format(x=0, y=y, orientation="H"))
        self.send("ship locations", *locations)

    ###################################################################
    def get_shots(self, num_shots):
        shots = []
        for i in range(int(num_shots)):
            shots.append("{x} {y}".format(x=self.shooting_x, y=self.shooting_y))
            self.shooting_x += 1
            if self.shooting_x == self.grid_width:
                self.shooting_x = 0
                self.shooting_y += 1
        str_shots = "|".join(shots)
        self.send("shots", str_shots)

if __name__ == "__main__":
    stdio.StandardIO(SimpleClient())
    reactor.run()
