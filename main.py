import pygame
from pygame.locals import *
from world_generator import generate_world
from block import Block
from player import Player
from colour_matrix import ColourMatrix
from colour_transformer import RGBColourTransformer
from math import cos, floor

pygame.init()
SCREEN = pygame.display.set_mode((2560, 1080))

block_size = 50
player = Player()
clock = pygame.time.Clock()
camera_x = 0#-(world_size*block_size)/2
camera_y = 0
hotbar_slot = 0
hotbar = ['stone', 'dirt', 'grass', 'wood', 'door']
half_block = block_size / 2
half_screen_w = SCREEN.get_width()/2
half_screen_h = SCREEN.get_height()/2
statistics_font = pygame.font.Font('assets/statfont.ttf', 20)
f = 0
fps = 60
dt = clock.tick(fps)/1000
falling = True
left = False
canleft = True
right = False
canright = True

world, visable_world = generate_world(SCREEN, block_size, camera_x)

running = True
while running:
  
  break_selected = False
  mouse_pos = pygame.mouse.get_pos()
  block_x = floor((mouse_pos[0]-camera_x) / block_size)
  x = floor((SCREEN.get_width()/2-camera_x) / block_size)
  block_y = floor(((mouse_pos[1]-camera_y)*-1) / block_size + block_size/2)
  y = floor((SCREEN.get_height()/2-camera_y*-1) / block_size) + 3
  f += 1
  SCREEN.fill("#aabbff")
  player.rect = pygame.Rect(half_screen_w, half_screen_h, block_size, block_size*2)
  # update the player rect based on the player's location

  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_BACKSPACE: running = False
      if event.key == K_SPACE:
        if canjump: player.v = 10
      if event.key == K_LEFT or event.key == K_a: left = True   # move left
      if event.key == K_RIGHT or event.key == K_d: right = True # move right
      if event.key == K_1: hotbar_slot = 0
      if event.key == K_2: hotbar_slot = 1
      if event.key == K_3: hotbar_slot = 2
      if event.key == K_4: hotbar_slot = 3
    if event.type == KEYUP:
      if event.key == K_LEFT or event.key == K_a: left = False
      if event.key == K_RIGHT or event.key == K_d: right = False
    
    if event.type == MOUSEBUTTONDOWN:
      if event.button == BUTTON_LEFT:
        break_selected = True
      if event.button == BUTTON_RIGHT:
        # placing!!
        world[block_x].blocks.insert(0, Block(hotbar[hotbar_slot], block_y*-1))
      
  canjump = True
      
  falling = True
  canleft = True
  canright = True

  # World renderer!
  lc = visable_world[0]
  if lc.x*block_size+camera_x>-block_size*2:
    visable_world.insert(0, world[lc.x-1])
    
  rc = visable_world[len(visable_world)-1]
  if rc.x*block_size+camera_x<SCREEN.get_width()+block_size*2:
    visable_world.append(world[rc.x+1])

  
  for chunk in visable_world:
    if chunk.x*block_size+camera_x<-block_size*2 or chunk.x*block_size+camera_x>SCREEN.get_width()+block_size*2:
      visable_world.remove(chunk)
      continue

    for block in chunk.blocks:
      if block.y*block_size+camera_y < 300 and block.y*block_size+camera_y+1200 < SCREEN.get_height():
        
        
        colour, shape, ghost = ColourMatrix().sort(block.type)
        if shape == 'block': rect = pygame.Rect(chunk.x*block_size+camera_x, block.y*block_size+1200+camera_y, block_size, block_size)
        if shape == 'door': rect = pygame.Rect(chunk.x*block_size+camera_x-block_size, block.y*block_size+1200+camera_y, block_size-40, block_size*2)
        pygame.draw.rect(SCREEN, colour, rect)
        # Player colliders
        if not ghost:
          if rect.colliderect((SCREEN.get_width()/2, player.rect.top, block_size-12, 2)): canjump = False
          if rect.colliderect((SCREEN.get_width()/2, player.rect.bottom-10, block_size-12, 2)): falling = False
          if rect.colliderect((SCREEN.get_width()/2-2, player.rect.top+half_block, half_block-10, block_size+half_block-12)): canleft = False
          if rect.colliderect((SCREEN.get_width()/2+half_block, player.rect.top+half_block, half_block-5, block_size+half_block-12)): canright = False
        if rect.collidepoint(pygame.mouse.get_pos()):
          pygame.draw.rect(SCREEN, RGBColourTransformer(colour).brighten(cos(f/15)*15), rect)
          pygame.draw.rect(SCREEN, RGBColourTransformer(colour).brighten(-20), rect, 3)
          if break_selected:
            chunk.blocks.remove(block)      
  
  if left and canleft: camera_x += 10#100*dt
  if right and canright: camera_x -= 10#100*dt
  
  # player
  if falling == True or player.v > 0:
    player.v -= 0.5
    player.y -= player.v
  else:
    player.y += player.v / 2
    player.v = 0
    
  camera_y += (player.y*-1 - camera_y)

  # player
  pygame.draw.rect(SCREEN, (255, 255, 0), pygame.Rect(SCREEN.get_width()/2, SCREEN.get_height()/2, block_size-10, block_size*2-10))
  
  for slot, item in enumerate(hotbar):
    pygame.draw.rect(SCREEN, (200, 200, 200), (SCREEN.get_width()-300-len(hotbar)+slot*(block_size+15), 5, block_size+10, block_size+10))
    if slot == hotbar_slot:
      pygame.draw.rect(SCREEN, (130, 130, 130), (SCREEN.get_width()-300-len(hotbar)+slot*(block_size+15), 5, block_size+10, block_size+10), 3)
    colour, shape, ghost = ColourMatrix().sort(item)
    if shape == 'block':
      pygame.draw.rect(SCREEN, colour, (SCREEN.get_width()-300-len(hotbar)+slot*(block_size+15)+7, 12, block_size-4, block_size-4))
    elif shape == 'door':
      pygame.draw.rect(SCREEN, colour, (chunk.x*block_size+camera_x-block_size, block.y*block_size+1200+camera_y, block_size-40, block_size))
  
  SCREEN.blit(statistics_font.render(f"x:{x}, y:{y}", True, (0,0,0)), (5,5))
  SCREEN.blit(statistics_font.render(f"looking at: x:{block_x}, y:{block_y}", True, (0,0,0)), (5,30))
  
  pygame.display.flip()
  clock.tick(fps)