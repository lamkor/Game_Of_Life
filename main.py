from PIL import Image
import numpy as np
im = Image.open('Untitled.jpg')
a = np.asarray(im)
im = Image.fromarray(a)
print(im.show())