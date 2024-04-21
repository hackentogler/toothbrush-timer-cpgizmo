import displayio
import terminalio
from adafruit_display_text import label
#from adafruit_bitmap_font import bitmap_font
from adafruit_gizmo import tft_gizmo
from adafruit_circuitplayground import cp
import time

# Only works with bitmap font
degree_sign = u'\u00B0'

def get_temperature():
    return f"Temperature:\n{(cp.temperature * 1.8 + 32): .1f} {degree_sign}F"

# Create the TFT Gizmo display
display = tft_gizmo.TFT_Gizmo()

# One group to rule them all
splash = displayio.Group()
display.root_group = splash

# Background color
color_bitmap = displayio.Bitmap(240, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000088
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Label for temperature
text_group = displayio.Group(scale=2, x=0, y=10)
text = get_temperature()
# Uncomment the next two lines for using a bitmap font (performance suffers)
# the_font = bitmap_font.load_font("/font/Helvetica-Bold-16.bdf")
# text_label = label.Label(the_font, text=text, color=0xFFFF00)
temp_text_label = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(temp_text_label)
splash.append(text_group)

# Label for timer
text_group = displayio.Group(scale=4, x=0, y=100)
text = "Starting..."
text_label = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
# Uncomment the next line for using a bitmap font (performance suffers)
# text_label = label.Label(the_font, text=text, color=0xFFFF00)
text_group.append(text_label)
splash.append(text_group)

# How long to brush each side
seconds = 30
# for range is exclusive, so add 1
num_iters = seconds + 1
# As a human, you should only have 4 of these
num_sides = 4
# Number of times to cycle through colors for change side message
num_flashes = 5

for j in range(num_sides):
    temp_text_label.text = get_temperature()
    text_label.color = 0x00FFFF
    # Uncomment to rest bg color
    #color_palette[0] = 0x000088
    for i in range(num_iters):
        # debug
        # milli_sec = int(round(time.time() * 1000))
        # print(milli_sec)
        # text_label.text = f"Side {j+1}:\n{seconds} " + ("seconds" if seconds != 1 else "second")
        text_label.text = f"Side {j+1}:\n{seconds} seconds"
        # Hardware is slow, this is closer to 30 seconds when seconds = 30
        time.sleep(.8)
        seconds = seconds - 1
        # milli_sec = int(round(time.time() * 1000))
        # print(milli_sec)
    
    cp.play_tone(2000, 0.2)
    if j < num_sides - 1:
        seconds = 30
        text_label.text = "CHANGE\nSIDES"
        for k in range(num_flashes):
            # Uncomment to change bg color
            # color_palette[0] = 0xFFFFFF 
            text_label.color = 0xFFFFFF
            time.sleep(.1)
            # color_palette[0] = 0x000000
            text_label.color = 0x00FF00
            time.sleep(.1)
            text_label.color = 0xFF0000
            time.sleep(.1)

text_label.color = 0x00FFFF
text_label.text = "DONE"

while True:
    pass
