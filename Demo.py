import numpy as np
import matplotlib.pyplot as plt

import FocusISM_lib as fism

plt.close('all')

#%% Read dataset

img = np.load('demo_img.npy')

img_closed = img[:,:,12]

img_sum = np.sum(img, axis = -1)

#%% Apply Focus-ISM

Signal, Bkg, Ism = fism.focusISM(img)

#%% Show results

plt.subplots(2,2, sharex = True, sharey = True)

plt.subplot(2, 2, 1)
plt.imshow(img_closed)
plt.axis('off')
plt.title('Confocal image (0.28 AU)')
plt.colorbar()

plt.subplot(2, 2, 2)
plt.imshow(img_sum)
plt.axis('off')
plt.title('Confocal image (1.40 AU)')
plt.colorbar()

plt.subplot(2, 2, 3)
plt.imshow(Ism)
plt.axis('off')
plt.title('ISM image')
plt.colorbar()

plt.subplot(2, 2, 4)
plt.imshow(Signal)
plt.axis('off')
plt.title('Focus-ISM image')
plt.colorbar()

plt.tight_layout()