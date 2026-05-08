import rasterio
import numpy as np
import matplotlib.pyplot as plt
import time



if __name__ == "__main__":
    raster_data_path = "aus_ppp_2020.tif"
    
    start_time = time.time()
    with rasterio.open("aus_ppp_2020.tif") as ds:
        n = 10000
        resample = False
        #print(ds.width, ds.height)

        window = rasterio.windows.Window(20000, 20000, n, n)
        if resample:
            data = ds.read(1,out_shape=(int(ds.height * 0.01), int(ds.width * 0.01)
                ), resampling=rasterio.enums.Resampling.average
            )
        else:
            data = ds.read(1, window=window)
            #data = ds.read(1)
    
    nodata_value = ds.nodata
    masked = np.ma.masked_equal(data, nodata_value)
    print("--- %s seconds ---" % (time.time() - start_time))

    plt.imshow(masked, cmap="viridis")
    plt.colorbar(label="Population count")
    plt.title("WorldPop Population Count (masked)")
    plt.axis("off")
    #plt.savefig("population_count.png", dpi=300, bbox_inches="tight")
    plt.show()
    
  
