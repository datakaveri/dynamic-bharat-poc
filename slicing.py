import warnings
warnings.filterwarnings("ignore")
import numpy as np
from pyproj import Transformer
import xarray as xr

def convert_coords(lon, lat, target_epsg):

    # Create a transformer from WGS84 (EPSG:4326) to the target EPSG
    transformer = Transformer.from_crs("EPSG:4326", str(target_epsg), always_xy=True)
    x, y = transformer.transform(lon, lat)

    return x, y


def get_img_slice(file,minLat, maxLat, minLong, maxLong):
    geosat_ar = xr.open_dataset(file,engine='rasterio')
    geosat_ar.band_data.values = (geosat_ar.band_data.values>0.4).astype('uint8')
    minLong, maxLat = convert_coords(minLong,maxLat,geosat_ar.rio.crs)
    maxLong, minLat = convert_coords(maxLong,minLat,geosat_ar.rio.crs)
    print(minLong, maxLat,maxLong, minLat)


    selected_slice = geosat_ar.sel(x=slice( maxLong,minLong), y=slice(maxLat, minLat ))
    return selected_slice







def get_layer_change(xarr1, xarr2):
    # Step 1: Calculate the difference array
    print("started calculating larger change")
    
    # Step 2: Count 0s and 1s in xarr1 and xarr2
    count_1_xarr1 = np.count_nonzero(xarr1.band_data.values == 1)
    count_0_xarr1 = np.count_nonzero(xarr1.band_data.values == 0)
    count_1_xarr2 = np.count_nonzero(xarr2.band_data.values == 1)
    count_0_xarr2 = np.count_nonzero(xarr2.band_data.values == 0)

    # Step 3: Calculate absolute change
    abs_change_1 = count_1_xarr2 - count_1_xarr1
    abs_change_0 = count_0_xarr2 - count_0_xarr1
    
    # Step 4: Calculate percentage change
    epsilon = 1e-8
    # Use counts from xarr1 as the baseline to avoid division by zero
    pct_change_1 = (abs_change_1 / (count_1_xarr1 + epsilon)) * 100
    pct_change_0 = (abs_change_0 / (count_0_xarr1 + epsilon)) * 100

    # Return results in a dictionary for clarity
    results = {
        "count_1_xarr1":count_1_xarr1,
        "count_1_xarr2":count_1_xarr2,
        "absolute_change_1": abs_change_1,
        "percentage_change_1": pct_change_1,
        "absolute_change_0": abs_change_0,
        "percentage_change_0": pct_change_0,
    }

    return results













