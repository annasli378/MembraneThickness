import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hmean
from functions import get_mask, get_blobs, get_widths_bwd
import scipy.io
## Read mask
num_pom_eks = [27, 18, 17, 9, 14, 18, 4, 15, 8, 8, 14, 20, 14, 20, 11, 17, 19, 27, 17, 26]
obr_num = 1
pth = "D:/GRUBA_MEMBRANA_PROJEKT/Proj_1/CALE_OBRAZKI/Masks/1_Mask.mat"
MASK = scipy.io.loadmat(pth)
mask = MASK['ABCD']

# Smoothe mask
maska_membrana = get_mask(mask)
plt.imshow(maska_membrana, cmap='gray')
plt.show()

# Get regions
mask_attributes_struct, num_blobs = get_blobs(maska_membrana)

# Get widths
step = 20
start = 30
widths = get_widths_bwd(start, step, mask_attributes_struct, num_blobs)

# pix -> nm
nm_pix = 0.15
widths_nm = widths / nm_pix

# Harmonic average
N = num_pom_eks[obr_num - 1]
r = np.random.choice(len(widths_nm), N, replace=False)
h_mean = hmean(widths_nm)
h_mean_r20 = hmean(widths_nm[r])

print("Harmonic mean:", h_mean)
print("Harmonic mean with random 20 samples:", h_mean_r20)