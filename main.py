import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hmean
from functions import get_mask, get_blobs, get_widths_bwd
import scipy.io
## Read mask
number_experts_mes = [27, 18, 17, 9, 14, 18, 4, 15, 8, 8, 14, 20, 14, 20, 11, 17, 19, 27, 17, 26]
obr_num = 1
pth = "D:/GRUBA_MEMBRANA_PROJEKT/Proj_1/CALE_OBRAZKI/Masks/1_Mask.mat"
MASK = scipy.io.loadmat(pth)
mask = MASK['ABCD']

# Smoothe mask
maska_membrana = get_mask(mask)
plt.imshow(maska_membrana, cmap='gray')
plt.show()

# Get regions
result_array_for_masks, result_array_for_skels,result_array_for_edges, num_blobs = get_blobs(maska_membrana)

# Get widths
step = 20
start = 30
widths = get_widths_bwd(start, step, result_array_for_masks,result_array_for_skels, num_blobs)

# pix -> nm
nm_pix = 0.15
widths_nm = np.array(widths)/nm_pix

# Harmonic average
N = number_experts_mes[obr_num - 1]
r = np.random.choice(len(widths_nm), N, replace=False)
h_mean = hmean(widths_nm)
h_mean_r20 = hmean(widths_nm[r])

print("Harmonic mean: ", h_mean)
print("Harmonic mean with random 20 samples: ", h_mean_r20)
h_mean_r20 = hmean(widths_nm[r])

