import numpy as np
from osgeo import gdal

def calculate_ts(lst_image_path):
    # Open the LST image
    lst_ds = gdal.Open(lst_image_path)
    if lst_ds is None:
        print("Failed to open the LST image.")
        return None

    # Read the LST image as an array
    lst_array = lst_ds.ReadAsArray()
    
    # Calculate Ts using the formula
    # Conversion from Kelvin to Celsius
    Ts_array = lst_array - 273.15

    # Calculate FTs using the provided formula
    exp_term = np.exp(0.334 * (Ts_array - 23))
    FTs_array = exp_term / (1 + exp_term)

    return FTs_array


def calculate_mean_ts(mean_lst_image_path):
    # Open the LST image
    mean_lst_ds = gdal.Open(mean_lst_image_path)
    if mean_lst_ds is None:
        print("Failed to open the LST image.")
        return None

    # Read the LST image as an array
    mean_lst_array = mean_lst_ds.ReadAsArray()

    # Calculate Ts using the formula
    # Conversion from Kelvin to Celsius
    mean_Ts_array =  mean_lst_array - 273.15

    # Calculate FTs using the provided formula
    mean_exp_term = np.exp(0.334 * (mean_Ts_array - 23))
    mean_FTs_array = mean_exp_term / (1 + mean_exp_term)

    return mean_FTs_array
#print(mean_FTs_array,'Mean')


def calculate_fw(E, P):
    if P < E:
        fw = P / E
    else:
        fw = 1
    return fw

def calculate_ft(FTs_array,mean_FTs_array):
    ft_array=FTs_array/mean_FTs_array
    return ft_array


def calculate_methane(ft_array, fw, constant_value):
    # Calculate methane array
    methane_array = ft_array * fw * constant_value
    return methane_array

def save_tiff(image_array, output_path, input_image_path):
    # Open the input image to get geotransform and projection information
    input_ds = gdal.Open(input_image_path)
    if input_ds is None:
        print("Failed to open the input image.")
        return False

    # Get geotransform and projection information
    geotransform = input_ds.GetGeoTransform()
    projection = input_ds.GetProjection()

    # Save the array as a TIFF image
    driver = gdal.GetDriverByName("GTiff")
    output_ds = driver.Create(output_path, image_array.shape[1], image_array.shape[0], 1, gdal.GDT_Float32)
    output_ds.SetGeoTransform(geotransform)
    output_ds.SetProjection(projection)
    output_ds.GetRasterBand(1).WriteArray(image_array)
    output_ds.FlushCache()
    output_ds = None

    return True

def mask_image_with_shapefile(input_image_path, output_image_path, shapefile_path):
    # Open the input image
    input_ds = gdal.Open(input_image_path)
    if input_ds is None:
        print("Failed to open the input image.")
        return False

    # Perform masking using the shapefile
    options = gdal.WarpOptions(cutlineDSName=shapefile_path, cropToCutline=True, dstNodata=-9999)  # Set the NoData value
    gdal.Warp(output_image_path, input_ds, options=options)

    return True

# Example usage
lst_image_path = r"H:\MMC_Client\StringBio\Paddy\NewPaddy\T6PLot\Plot6_LST_14Dec.tif"
mean_lst_image_path=r"H:\MMC_Client\StringBio\Paddy\NewPaddy\T6PLot\Mean_LST_Season_mask.tif"
shapefile_path = r"H:\MMC_Client\StringBio\Paddy\Paddy\T6_plot_paddy.shp"

# Calculate Ts
FTs_array = calculate_ts(lst_image_path)

# Get user input for Evapotranspiration (E), Rainfall (P), and constant value
E = float(input("Enter Evapotranspiration (E) value: "))
P = float(input("Enter Rainfall (P) value: "))
constant_value = float(input("Enter constant value: "))

# Calculate Fraction of water (fw)
fw = calculate_fw(E, P)
print("Fraction of water (fw):", fw)

mean_FTs_array=calculate_mean_ts(mean_lst_image_path)

ft_array=calculate_ft(FTs_array,mean_FTs_array)

# Calculate methane
methane_array = calculate_methane(ft_array, fw, constant_value)

# Save the methane image
output_methane_path = r"H:\MMC_Client\StringBio\Paddy\NewPaddy\T6PLot\methane.tif"
save_tiff(methane_array, output_methane_path, lst_image_path)

# Mask the methane image with the shapefile
masked_methane_path = r"H:\MMC_Client\StringBio\Paddy\NewPaddy\T6PLot\FinalMethaneMap.tif"
mask_image_with_shapefile(output_methane_path, masked_methane_path, shapefile_path)
print("Masked methane image saved at:", masked_methane_path)
