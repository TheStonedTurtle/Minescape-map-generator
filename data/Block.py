class Block:
    def __init__(self, display_name: str, _id: str, block_name: str, sprite_idx=-1):
        self.display_name = display_name
        self.id = _id
        self.block_name = block_name
        self.sprite_idx = sprite_idx
