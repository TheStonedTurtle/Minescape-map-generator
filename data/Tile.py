class Tile:
    def __init__(self):
        self.height = None
        self.settings = 0
        self.overlay_id = 0
        self.overlay_path = 0
        self.overlay_rotation = 0
        self.underlay_id = 0
        self.attribute_opcode = 0
        self.objects = []

    # Checks if the 2nd bit is a 1
    def is_bridge(self):
        return (self.settings & 2) != 0

    # Checks if the 2nd, 4th, and 5th bits are 0
    def is_drawn(self):  # TODO rename this method pulled from MapImageDumper.java:L180
        return (self.settings & 26) == 0
