# # #TO DETECT THE PHOTO IS OF WHICH POLE
from osgeo import gdal
import numpy as np

gdal.PushErrorHandler('CPLQuietErrorHandler')

files = {
    'cpr': r"E:\ISRO_IMG\ch2_sar_ndxl_20250630mpcpspeast_d_fp_xxx\data\derived\20250630\ch2_sar_ndxl_20250630mpcpspeast_d_cpr_xx_fp_xx_xxx.tif",
    'srd': r"E:\ISRO_IMG\ch2_sar_ndxl_20250630mpcpspeast_d_fp_xxx\data\derived\20250630\ch2_sar_ndxl_20250630mpcpspeast_d_srd_xx_fp_xx_xxx.tif",
    'trt': r"E:\ISRO_IMG\ch2_sar_ndxl_20250630mpcpspeast_d_fp_xxx\data\derived\20250630\ch2_sar_ndxl_20250630mpcpspeast_d_trt_xx_fp_xx_xxx.tif",
}

for name, path in files.items():
    ds = gdal.Open(path)
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray().astype(np.float32)
    valid = data[~np.isnan(data)]
    
    print(f"{name}: min={np.nanmin(data):.4f}, max={np.nanmax(data):.4f}, "
          f"mean={np.nanmean(data):.4f}, median={np.nanmedian(data):.4f}")

import numpy as np
from osgeo import gdal

gdal.PushErrorHandler('CPLQuietErrorHandler')

# Load CPR and SRD
cpr = gdal.Open("E:\ISRO_IMG\ch2_sar_ndxl_20250630mpcpspeast_d_fp_xxx\data\derived\20250630\ch2_sar_ndxl_20250630mpcpspeast_d_cpr_xx_fp_xx_xxx.tif").GetRasterBand(1).ReadAsArray().astype(np.float32)
srd = gdal.Open("E:\ISRO_IMG\ch2_sar_ndxl_20250630mpcpspeast_d_fp_xxx\data\derived\20250630\ch2_sar_ndxl_20250630mpcpspeast_d_srd_xx_fp_xx_xxx.tif").GetRasterBand(1).ReadAsArray().astype(np.float32)

# Ice detection: High CPR + Low SRD (low coherence = depolarization)
ice_probability = np.where(
    (cpr > 1.0) & (srd < 0.2),  # Strong CPR + weak coherence
    1.0,  # High confidence ice
    np.where(
        (cpr > 0.8) & (srd < 0.3),  # Moderate CPR + moderate coherence
        0.5,  # Medium confidence
        0.0   # Not ice
    )
)

# Save as GeoTIFF for QGIS visualization
print(f"Ice pixels (high conf): {(ice_probability == 1.0).sum()}")
print(f"Ice pixels (med conf): {(ice_probability == 0.5).sum()}")