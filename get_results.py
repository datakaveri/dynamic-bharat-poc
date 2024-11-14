import slicing


def get_results(topLeft, bottomRight):
    try:
        hyd1_b = slicing.get_img_slice("images/b_hyd1_ard-cps-tsk-max-new-cps.tif",minLat=topLeft[1],maxLat=bottomRight[1],maxLong=topLeft[0],minLong=bottomRight[0])
        hyd2_b = slicing.get_img_slice("images/b_hyd2_ard-cps-tsk-max-new-cps.tif",minLat=topLeft[1],maxLat=bottomRight[1],maxLong=topLeft[0],minLong=bottomRight[0])
        results_b = slicing.get_layer_change(hyd1_b, hyd2_b)

        hyd1_r = slicing.get_img_slice("images/r_hyd1_ard-cps-tsk-max-new-cps.tif",minLat=topLeft[1],maxLat=bottomRight[1],maxLong=topLeft[0],minLong=bottomRight[0])
        hyd2_r = slicing.get_img_slice("images/r_hyd2_ard-cps-tsk-max-new-cps.tif",minLat=topLeft[1],maxLat=bottomRight[1],maxLong=topLeft[0],minLong=bottomRight[0])
        results_r = slicing.get_layer_change(hyd1_r, hyd2_r)

        hyd1_t = slicing.get_img_slice("images/t_hyd1_ard-cps-tsk-max-new-cps.tif",minLat=topLeft[1],maxLat=bottomRight[1],maxLong=topLeft[0],minLong=bottomRight[0])
        hyd2_t = slicing.get_img_slice("images/t_hyd2_ard-cps-tsk-max-new-cps.tif",minLat=topLeft[1],maxLat=bottomRight[1],maxLong=topLeft[0],minLong=bottomRight[0])
        results_t = slicing.get_layer_change(hyd1_t, hyd2_t)

        hyd1_w = slicing.get_img_slice("images/w_hyd1_ard-cps-tsk-max-new-cps.tif",minLat=topLeft[1],maxLat=bottomRight[1],maxLong=topLeft[0],minLong=bottomRight[0])
        hyd2_w = slicing.get_img_slice("images/w_hyd2_ard-cps-tsk-max-new-cps.tif",minLat=topLeft[1],maxLat=bottomRight[1],maxLong=topLeft[0],minLong=bottomRight[0])
        results_w = slicing.get_layer_change(hyd1_w, hyd2_w)

        return [results_b, results_r,  results_t, results_w]
    
    except Exception as e:
        print(e)
