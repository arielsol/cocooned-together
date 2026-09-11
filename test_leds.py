import time
from rpi_ws281x import PixelStrip, Color

strip = PixelStrip(100, 18, 800000, 10, False, 255)
strip.begin()

for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(255, 180, 60))
strip.show()

time.sleep(10)
