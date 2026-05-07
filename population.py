import rasterio
import numpy as np
import matplotlib.pyplot as plt



if __name__ == "__main__":
    raster_data_path = "aus_ppp_2020.tif"

    with rasterio.open(raster_data_path) as ds:
        data = ds.read(1,out_shape=(
                int(ds.height * 0.001),
                int(ds.width * 0.001)
            )
        )
        print(ds.nodata)
        nodata_value = ds.nodata
    masked = np.ma.masked_equal(data, nodata_value)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(masked, cmap="viridis", interpolation="nearest")
    plt.colorbar(label="Population count")
    plt.title("WorldPop Population Density (masked)")
    plt.axis("off")
    plt.savefig("population_density.png", dpi=300, bbox_inches="tight")
    plt.show()