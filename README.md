# Membrane Thickness Analysis
This repository is a collection of functions designed to measure the thickness of the podocyte foot membrane based on experts masks. 

## Main functions
### 1. Mask Smoothing
Function: get_mask(m)

Description: Smoothes the input binary mask by performing morphological operations such as closing, opening, and filling holes.

Usage: smoothed_mask = get_mask(orginal_mask)

### 2. Blob Extraction
Function: get_blobs(mask)

Description: Identifies and extracts individual membrane blobs from a binary membrane image. It filters out blobs that are too close to the image borders and computes additional attributes for each blob.

Usage: result_array_for_masks, result_array_for_skels, result_array_for_edges, num_blobs = get_blobs(mask)

### 3. Width Measurement
Function: get_widths_bwd(start, step, result_array_for_masks,result_array_for_skels, num_blobs)

Description: Measures membrane widths along the skeletonized membrane structures using backward distance transform-based measurement.

Usage: widths = get_widths_bwd(start, step, result_array_for_masks,result_array_for_skels, num_blobs)

## Usage
 - Import the  functions into your Python environment.
 - Load your binary membrane image.
 - Apply get_mask to smoothen the mask if needed.
 - Use get_blobs to extract membrane blobs and their attributes.
 - Measure membrane widths using either get_widths_inc or get_widths_bwd.
 - Calculate the harmonic mean of membrane widths using hmean.
 - Analyze and interpret the results for your specific application.
