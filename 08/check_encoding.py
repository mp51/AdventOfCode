encoding = [int(i) for i in input()]

WIDTH = 25
HEIGHT = 6

layers = []

i = 0
layer_idx = 0
for i in range(0, len(encoding), WIDTH*HEIGHT):
   layer = encoding[i:i+WIDTH*HEIGHT]
   layer_idx += 1
   layers.append((layer.count(0), layer_idx, layer))

print("Layers count:", len(layers))
found_layer = min(layers, key=lambda l: l[0])
print("Found layer:", found_layer)
layer = found_layer[2]
print(layer.count(0))
count_1 = layer.count(1)
count_2 = layer.count(2)
print(count_1, "*", count_2, "=", count_1*count_2)