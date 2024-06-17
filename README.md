# Methane Emission Estimation from Remote Sensing Data

This project estimates methane emissions from paddy fields using remote sensing data. The process involves calculating temperature stress (Ts), fraction of water (fw), methane emissions, and saving the results as TIFF images. The resulting methane emission map is also masked using a shapefile.


## Requirements

- Python 3.x
- NumPy
- GDAL

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/methane-emission-estimation.git
    cd methane-emission-estimation
    ```

2. Install the required Python packages:

    ```bash
    pip install numpy gdal
    ```

## Usage

1. Ensure you have the required input files:
   - LST (Land Surface Temperature) image (e.g., `Plot6_LST_14Dec.tif`)
   - Mean LST image (e.g., `Mean_LST_Season_mask.tif`)
   - Shapefile for masking (e.g., `T6_plot_paddy.shp`)

2. Run the script:

    ```python
    python calculate_methane.py
    ```

3. The script will prompt you to enter values for:
   - Evapotranspiration (E)
   - Rainfall (P)
   - A constant value for the calculation

4. The script processes the input data and generates the methane emission map.

5. The resulting methane emission map will be saved and masked according to the provided shapefile.

## Functions

### `calculate_ts(lst_image_path)`

Calculates the temperature stress (Ts) from an LST image.

- **Parameters:**
  - `lst_image_path` (str): Path to the LST image file.
- **Returns:** numpy.ndarray: Ts array.

### `calculate_mean_ts(mean_lst_image_path)`

Calculates the mean temperature stress (mean Ts) from a mean LST image.

- **Parameters:**
  - `mean_lst_image_path` (str): Path to the mean LST image file.
- **Returns:** numpy.ndarray: Mean Ts array.

### `calculate_fw(E, P)`

Calculates the fraction of water (fw).

- **Parameters:**
  - `E` (float): Evapotranspiration value.
  - `P` (float): Rainfall value.
- **Returns:** float: Fraction of water (fw).

### `calculate_ft(FTs_array, mean_FTs_array)`

Calculates the fraction of temperature stress (ft).

- **Parameters:**
  - `FTs_array` (numpy.ndarray): Ts array.
  - `mean_FTs_array` (numpy.ndarray): Mean Ts array.
- **Returns:** numpy.ndarray: Fraction of temperature stress (ft).

### `calculate_methane(ft_array, fw, constant_value)`

Calculates the methane emission.

- **Parameters:**
  - `ft_array` (numpy.ndarray): Fraction of temperature stress array.
  - `fw` (float): Fraction of water.
  - `constant_value` (float): A constant value used in the calculation.
- **Returns:** numpy.ndarray: Methane emission array.

### `save_tiff(image_array, output_path, input_image_path)`

Saves an array as a TIFF image.

- **Parameters:**
  - `image_array` (numpy.ndarray): Array to be saved.
  - `output_path` (str): Path where the output image will be saved.
  - `input_image_path` (str): Path to the input image (for geotransform and projection).
- **Returns:** bool: True if successful, False otherwise.

### `mask_image_with_shapefile(input_image_path, output_image_path, shapefile_path)`

Masks an image using a shapefile.

- **Parameters:**
  - `input_image_path` (str): Path to the input image.
  - `output_image_path` (str): Path where the masked image will be saved.
  - `shapefile_path` (str): Path to the shapefile.
- **Returns:** bool: True if successful, False otherwise.


