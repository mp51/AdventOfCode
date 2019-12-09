WIDTH = 25
HEIGHT = 6


def print_image(image):
   for i in range(HEIGHT):
      row = image[i*WIDTH:i*WIDTH+WIDTH]
      for pixel in row:
         if pixel == 0:
            print(' ', end='')
         else:
            print('#', end='')
      print()


encoding = [int(i) for i in input()]


layers = []

i = 0
layer_idx = 0
for i in range(0, len(encoding), WIDTH*HEIGHT):
   layer = encoding[i:i+WIDTH*HEIGHT]
   layer_idx += 1
   layers.append((layer.count(0), layer_idx, layer))


image = [None for _ in range(WIDTH*HEIGHT)]

for layer in layers:
   for i, pixel in enumerate(layer[2]):
      if image[i] is None and pixel != 2: # 2- transparent pixel
         image[i] = pixel

print_image(image)