import os
import json

path = 'D:\Creators\GitHub\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose\output'

files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(os.path.join(r, file))


points = []

for f in files:
    print(f)
    with open(f) as file:
        x = json.loads(file.read())
        print(x)
        points.append(x)

with open('merged.json', 'w') as outfile:
    json.dump(points, outfile)

print(points)
