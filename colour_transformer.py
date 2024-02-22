class RGBColourTransformer():
  def __init__(s, rgb_sequence):
    s.col = rgb_sequence
    s.red = s.col[0]
    s.green = s.col[1]
    s.blue = s.col[2]
    
  def brighten(s, amount):
    r = s.red+amount
    if r > 255: r=255
    if r < 0: r=0
    g = s.green+amount
    if g > 255: g=255
    if g < 0: g=0
    b = s.blue+amount
    if b > 255: b=255
    if b < 0: b=0

    return (r, g, b)