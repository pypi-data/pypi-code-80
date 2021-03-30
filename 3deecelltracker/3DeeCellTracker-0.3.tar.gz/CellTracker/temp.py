def match(volume2, par_image, par_tracker, par_path, par_subregions, r_coordinates_segment_pre, r_coordinates_tracked_pre,
          r_coordinates_confirmed_vol1, cells_on_boundary, unet_model, FFN_model, r_displacement_from_vol1,
          seg_cells_interpolated_corrected):
    """
    Match current volume and another volume2
    """
    print('t=%i' % volume2)

    #######################################################
    # skip frames that cannot be tracked
    #######################################################
    if volume2 in par_image["miss_frame"]:
        print("volume2 is a miss_frame")
        return None

    ########################################################
    # generate automatic segmentation in current volume
    ########################################################
    image_cell_bg, l_center_coordinates, _, image_gcn = \
        segmentation(volume2, par_image, par_tracker, par_path, unet_model,
                     method="min_size", neuron_num=par_tracker["neuron_num"])

    t = time.time()
    r_coordinates_segment_post = displacement_image_to_real(l_center_coordinates, par_image)
    #######################################
    # track by fnn + prgls
    #######################################
    # calculate the mean predictions of each cell locations
    r_coordinates_prgls = predict_pos_once(r_coordinates_segment_pre, r_coordinates_segment_post,
                                           r_coordinates_tracked_pre, par_tracker, FFN_model, draw=True)
    print('fnn + pr-gls took %.1f s' % (time.time() - t))

    #####################
    # boundary cells
    #####################
    cells_bd = np.where(reduce(np.logical_or,
                               [r_coordinates_prgls[:, 0] < 6,
                                r_coordinates_prgls[:, 1] < 6,
                                r_coordinates_prgls[:, 0] > par_image["x_siz"] - 6,
                                r_coordinates_prgls[:, 1] > par_image["y_siz"] - 6,
                                r_coordinates_prgls[:, 2] / par_image["z_xy_ratio"] < 0,
                                r_coordinates_prgls[:, 2] / par_image["z_xy_ratio"] > par_image["z_siz"]]))

    print("cells on boundary:", cells_bd[0] + 1)
    cells_on_boundary[cells_bd] = 1

    ###################################
    # accurate correction
    ###################################
    t = time.time()
    # calculate r_displacements from the first volume
    # r_displacement_from_vol1: accurate displacement; i_displacement_from_vol1: displacement using voxels numbers as unit
    r_displacement_from_vol1 = r_displacement_from_vol1 + r_coordinates_prgls - r_coordinates_tracked_pre
    i_displacement_from_vol1 = displacement_real_to_interpolatedimage(r_displacement_from_vol1, par_image)

    i_cumulated_disp = i_displacement_from_vol1 * 0.0

    print("FFN + PR-GLS: Left: x-y; Right: x-z")
    plt.pause(10)
    print("Accurate correction:")
    plt.figure(figsize=(16,2))
    rep_correction = 5
    for i in range(20):
        r_displacement_from_vol1, i_displacement_from_vol1, r_displacement_correction = correction_once_interp(
            i_displacement_from_vol1, par_image, par_subregions, cells_on_boundary,
            r_coordinates_confirmed_vol1, image_cell_bg, image_gcn, seg_cells_interpolated_corrected
        )

        i_disp_test = r_displacement_correction.copy()
        i_disp_test[:, 2] *= par_image["z_scaling"] / par_image["z_xy_ratio"]
        i_cumulated_disp += i_disp_test

        # draw correction
        if i == rep_correction-1:
            r_coordinates_correction = r_coordinates_confirmed_vol1 + r_displacement_from_vol1
            plt.figure(figsize=(16, 4))
            plt.subplot(1, 2, 1)
            tracking_plot(r_coordinates_prgls, r_coordinates_segment_post, r_coordinates_correction)
            plt.subplot(1, 2, 2)
            tracking_plot_zx(r_coordinates_prgls, r_coordinates_segment_post, r_coordinates_correction)

        if i == 0:
            print("max correction:", end=" ")
        if min(np.nanmax(np.abs(i_disp_test)), np.nanmax(np.abs(i_cumulated_disp))) >= 0.5:
            print(np.nanmax(np.abs(i_disp_test)), end=",")
        else:
            print(np.nanmax(np.abs(i_disp_test)))
            break

    return r_displacement_correction