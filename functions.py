import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt
from skimage.morphology import binary_closing, binary_opening, disk, binary_dilation, binary_erosion, remove_small_holes, remove_small_objects
from skimage.measure import label, regionprops
from skimage.morphology import skeletonize, remove_small_objects
from skimage.segmentation import clear_border

def remove_small_branches(binary_image, min_branch_length):
    binary_image = binary_image.astype(bool)
    skeleton = skeletonize(binary_image)
    labeled_skeleton = label(skeleton)

    # Iterate through each label (branch) and calculate its length
    branch_lengths = {}
    for region in regionprops(labeled_skeleton):
        # Calculate the length of the branch
        branch_length = np.sum(region.image)
        branch_label = region.label
        branch_lengths[branch_label] = branch_length

    # Create a mask to filter out branches shorter than the minimum length
    valid_branches_mask = np.zeros_like(skeleton)
    for branch_label, branch_length in branch_lengths.items():
        if branch_length >= min_branch_length:
            valid_branches_mask[labeled_skeleton == branch_label] = 1

    clean_mask = clear_border(valid_branches_mask)
    return clean_mask

def get_blobs(maska_membrana):
    labeled_image, num_blobs = label(maska_membrana, return_num=True)
    rows, kols = maska_membrana.shape

    mask_atr = []
    for i in range(1, num_blobs + 1):
        skiel = skeletonize(labeled_image == i)
        edges = remove_small_branches(labeled_image == i, min_branch_length=200)

        pix_list_edges = regionprops(edges.astype(int), coordinates='xy')[0].coords
        len_edges = len(pix_list_edges)

        len_tx, len_bx, len_ry, len_ly = 0, 0, 0, 0
        for e in pix_list_edges:
            pixe = e
            if pixe[0] == 0:
                len_ly += 1
            elif pixe[0] == kols:
                len_ry += 1
            if pixe[1] == 0:
                len_tx += 1
            elif pixe[1] == rows:
                len_bx += 1

        if len_tx > len_edges / 4 or len_bx > len_edges / 4 or len_ly > len_edges / 4 or len_ry > len_edges / 4:
            print("object is too adjacent to the edge")
        else:
            if np.sum(skiel) > 0:
                mask_atr.append({'mask': labeled_image == i, 'skel': skiel, 'edges': edges})

    return mask_atr, len(mask_atr)


def get_mask(m):
    mask_m = (m == 1)
    ex = regionprops(mask_m.astype(int), extra_properties=['extent'])
    so = disk(15)
    for prop in ex:
        if prop.extent < 0.1:
            so = disk(5)

    BC = binary_closing(mask_m, selem=disk(15))
    BO = binary_opening(BC, selem=so)
    BO = binary_dilation(BO, selem=disk(15))

    filled = remove_small_holes(BO, area_threshold=18000)
    holes = filled & ~BO
    bigholes = remove_small_objects(holes, min_size=18000)
    smallholes = holes & ~bigholes

    new = BO | smallholes

    new = binary_erosion(new, selem=disk(15))
    new = binary_dilation(new, selem=disk(5))

    return new


def get_widths_bwd(start, step, mask_atr, num_blobs):
    widths_good = []

    for i in range(num_blobs):
        skel_pix = regionprops(mask_atr[i]['skel'].astype(int), coordinates='xy')[0].coords
        skel_len = len(skel_pix)
        stop = skel_len - start
        mask = mask_atr[i]['mask']
        skel_image = mask_atr[i]['skel']

        edt_image = np.array(distance_transform_edt(~mask), dtype=np.float32)
        diameter_image = 2 * edt_image * skel_image.astype(np.float32)
        widths = diameter_image[diameter_image > 0]

        for w in range(start, stop, step):
            widths_good.append(widths[w])

        plt.imshow(diameter_image, cmap='gray')
        plt.show()

    return widths_good