from perlin_noise import PerlinNoise
from _chunk import Chunk
from block import Block
from random import randint

noise = PerlinNoise(octaves=4, seed=7)
xpix = 1000
world_noise = [[noise([j/xpix]) for j in range(xpix)]]

# The world will be stored in columns, of 1 block 
# vertical. It will be stored in a list of lists
# with block objects

# World builder
def generate_world(SCREEN, block_size, camera_x):
    world = []
    visable_world = []
    world_size = 1000
    
    for chunk_x in range(world_size):
        chunk = Chunk(chunk_x) # create new chunk
        for block in range(round((world_noise[0][chunk_x])*100)+30):
            chunk.blocks.append(Block(type='dirt', y=block*-1+30))
        chunk.blocks.reverse()

        for depth, block in enumerate(chunk.blocks):
            if depth == 0 or depth == randint(0, 1):
                block.type='grass'
            if depth > randint(4,5):
                block.type='stone'
        world.append(chunk)
    
        if not (chunk_x*block_size<0+100 or chunk_x*block_size+camera_x>SCREEN.get_width()-100):
            visable_world.append(chunk)
    
    return world, visable_world