class ColourMatrix():
    def sort(self, block_type):
        if block_type == 'grass': return (63, 208, 68), 'block', False
        elif block_type == 'dirt': return (64, 54, 28), 'block', False
        elif block_type == 'stone': return (170, 170, 187), 'block', False
        elif block_type == 'wood': return (130, 130, 74), 'block', False
        elif block_type == 'door': return (130, 130, 74), 'door', True
        else: raise f'UndefinedBlockError: The block that tried to spawn did not have a handeler ({block_type})'