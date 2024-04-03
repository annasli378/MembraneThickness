import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt
from skimage.morphology import binary_closing, binary_opening, disk, binary_dilation, binary_erosion, remove_small_holes, remove_small_objects
from skimage.measure import label, regionprops
from skimage.morphology import skeletonize, remove_small_objects

def get_blobs(maska_membrana):
    labeled_image, num_blobs = label(maska_membrana, return_num=True)
    rows, cols = maska_membrana.shape

    result_array_for_masks = np.zeros([num_blobs, rows + 10, cols + 10], dtype=np.uint8)
    result_array_for_skels = np.zeros([num_blobs, rows + 10, cols + 10], dtype=np.uint8)
    result_array_for_edges = np.zeros([num_blobs, rows + 10, cols + 10], dtype=np.uint8)

    cnt_blob = 0

    for i in range(1, num_blobs + 1):
        image_i = (labeled_image == i)

        # Pad the image with zeros
        padded_image = np.pad(image_i, pad_width=5, mode='constant', constant_values=0)

        # Skeletonize
        skiel = skeletonize(padded_image)

        # Calculate edges
        edges = np.abs(padded_image.astype(np.uint8) - binary_dilation(padded_image, footprint=disk(3))).astype(
            np.uint8)

        # Calculate properties of edges
        props_edges = regionprops(edges.astype(int))
        pix_list_edges = props_edges[0].coords
        len_edges = len(pix_list_edges)

        len_tx, len_bx, len_ry, len_ly = 0, 0, 0, 0
        for e in pix_list_edges:
            if e[0] <= 5:
                len_tx += 1
            elif e[0] >= rows:
                len_bx += 1
            if e[1] <= 5:
                len_ly += 1
            elif e[1] >= cols:
                len_ry += 1

        # print(len_tx)
        # print(len_bx)
        # print(len_ry)
        # print(len_ly)
        # print(len_edges)

        # Check if more than 1/4 of the edge is connected to the image edge
        if len_tx > len_edges / 4 or len_bx > len_edges / 4 or len_ly > len_edges / 4 or len_ry > len_edges / 4:
            print("Object is too adjacent to the edge")
        else:
            if np.sum(skiel) > 0:
                result_array_for_masks[cnt_blob] = padded_image
                result_array_for_skels[cnt_blob] = skiel
                result_array_for_edges[cnt_blob] = edges
                cnt_blob += 1

    return result_array_for_masks, result_array_for_skels, result_array_for_edges, cnt_blob - 1


def get_mask(m):
    mask_m = (m == 1)
    ex = regionprops(mask_m.astype(int))
    so = disk(15)
    for prop in ex:
        if prop.extent < 0.1:
            so = disk(5)

    BC = binary_closing(mask_m, footprint=disk(15))
    BO = binary_opening(BC, footprint=so)
    BO = binary_dilation(BO, footprint=disk(15))

    filled = remove_small_holes(BO, area_threshold=18000)
    holes = filled & ~BO
    bigholes = remove_small_objects(holes, min_size=18000)
    smallholes = holes & ~bigholes

    new = BO | smallholes

    new = binary_erosion(new, footprint=disk(15))
    new = binary_dilation(new, footprint=disk(5))

    return new


def get_widths_bwd(start, step, result_array_for_masks, result_array_for_skels, num_blobs):
    widths_good = []

    for i in range(num_blobs):
        blob_skel = result_array_for_skels[i]
        skel_pix = regionprops(blob_skel)[0].coords
        skel_len = len(skel_pix)
        print(skel_len)
        stop = skel_len - start
        blob_mask = result_array_for_masks[i]

        edt_image = np.array(distance_transform_edt(~blob_mask), dtype=np.float32)
        diameter_image = 2 * edt_image * blob_skel.astype(np.float32)
        widths = diameter_image[diameter_image > 0]
        for w in range(start, stop, step):
            widths_good.append(widths[w])

        plt.imshow(diameter_image, cmap='gray')
        plt.show()

    return widths_good