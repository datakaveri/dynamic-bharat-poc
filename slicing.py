import warnings
warnings.filterwarnings("ignore")
import numpy as np
from pyproj import Transformer
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds

def convert_coords(lon, lat, target_crs):
    # Create a transformer from WGS84 (EPSG:4326) to the target CRS
    transformer = Transformer.from_crs("EPSG:4326", target_crs, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

def get_img_slice(file, minLat, maxLat, minLong, maxLong):
    with rasterio.open(file) as src:
        # Get the CRS of the raster
        raster_crs = src.crs
        
        # Convert coordinates to raster CRS
        minLong, maxLat = convert_coords(minLong, maxLat, raster_crs)
        maxLong, minLat = convert_coords(maxLong, minLat, raster_crs)
        print(minLong, maxLat, maxLong, minLat)
        
        # Ensure proper coordinate ordering (left, bottom, right, top)
        left = min(minLong, maxLong)
        bottom = min(minLat, maxLat)
        right = max(minLong, maxLong)
        top = max(minLat, maxLat)
        
        try:
            # Create a window from the bounds
            window = from_bounds(left, bottom, right, top, src.transform)
            
            # Ensure the window is within raster bounds
            window = window.intersection(
                rasterio.windows.Window(0, 0, src.width, src.height)
            )
            
            # Read the data within the window
            data = src.read(window=window)
            
            # Apply threshold and convert to uint8
            data = (data > 0.4).astype('uint8')
            
            # Get the transform for the windowed data
            windowed_transform = src.window_transform(window)
            
            # Create a dictionary with the sliced data and metadata
            selected_slice = {
                'data': data,
                'transform': windowed_transform,
                'crs': src.crs,
                'window': window,
                'profile': src.profile.copy()
            }
            
            # Update profile for the windowed data
            selected_slice['profile'].update({
                'height': data.shape[1],
                'width': data.shape[2],
                'transform': windowed_transform,
                'dtype': data.dtype
            })
            
            return selected_slice
            
        except Exception as e:
            print(f"Error creating window: {e}")
            # Fallback: read entire raster and slice using array indexing
            data = src.read()
            
            # Convert bounds to pixel coordinates
            row_start, col_start = src.index(left, top)
            row_end, col_end = src.index(right, bottom)
            
            # Ensure proper ordering
            row_start, row_end = min(row_start, row_end), max(row_start, row_end)
            col_start, col_end = min(col_start, col_end), max(col_start, col_end)
            
            # Slice the data
            data_slice = data[:, row_start:row_end, col_start:col_end]
            
            # Apply threshold and convert to uint8
            data_slice = (data_slice > 0.4).astype('uint8')
            
            # Create a simple return structure
            selected_slice = {
                'data': data_slice,
                'transform': src.transform,
                'crs': src.crs,
                'window': None,
                'profile': src.profile.copy()
            }
            
            return selected_slice

def get_layer_change(slice1, slice2):
    # Step 1: Calculate the difference array
    print("started calculating layer change")
    
    # Extract data arrays from the slices
    data1 = slice1['data'] if isinstance(slice1, dict) else slice1
    data2 = slice2['data'] if isinstance(slice2, dict) else slice2
    
    # Step 2: Count 0s and 1s in data1 and data2
    count_1_data1 = np.count_nonzero(data1 == 1)
    count_0_data1 = np.count_nonzero(data1 == 0)
    count_1_data2 = np.count_nonzero(data2 == 1)
    count_0_data2 = np.count_nonzero(data2 == 0)

    # Step 3: Calculate absolute change
    abs_change_1 = count_1_data2 - count_1_data1
    abs_change_0 = count_0_data2 - count_0_data1
    
    # Step 4: Calculate percentage change
    epsilon = 1e-8
    # Use counts from data1 as the baseline to avoid division by zero
    pct_change_1 = (abs_change_1 / (count_1_data1 + epsilon)) * 100
    pct_change_0 = (abs_change_0 / (count_0_data1 + epsilon)) * 100

    # Return results in a dictionary for clarity
    results = {
        "count_1_xarr1": count_1_data1,
        "count_1_xarr2": count_1_data2,
        "absolute_change_1": abs_change_1,
        "percentage_change_1": pct_change_1,
        "absolute_change_0": abs_change_0,
        "percentage_change_0": pct_change_0,
    }

    return results

# Helper function to save sliced raster if needed
def save_slice(slice_dict, output_path):
    """Save the sliced raster to a new file"""
    with rasterio.open(output_path, 'w', **slice_dict['profile']) as dst:
        dst.write(slice_dict['data'])

# Helper function to get basic info about the slice
def get_slice_info(slice_dict):
    """Get basic information about the raster slice"""
    data = slice_dict['data']
    return {
        'shape': data.shape,
        'dtype': data.dtype,
        'crs': slice_dict['crs'],
        'transform': slice_dict['transform'],
        'bounds': rasterio.transform.array_bounds(
            data.shape[1], data.shape[2], slice_dict['transform']
        )
    }