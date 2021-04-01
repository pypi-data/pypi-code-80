import numpy as np


def display(points, rgb_image=None, ignore_value=np.nan):
    try:
        import open3d as o3d
    except ImportError:
        print("Cannot import open3d (http://www.open3d.org/docs/release/getting_started.html) please install it first!")
        return
    keep = np.where(points != [ignore_value] * 3)
    points = points[keep].reshape(-1, 3)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    if rgb_image:
        colours = np.reshape(rgb_image, (rgb_image.shape[0] * rgb_image.shape[1], 3)) / 255.0
        colours = colours[keep].reshape(-1, 3)
        pcd.colors = o3d.utility.Vector3dVector(colours)

    o3d.visualization.draw_geometries([pcd])


def __open3d_display_main():
    try:
        import open3d as o3d
    except ImportError:
        print("Cannot import open3d (http://www.open3d.org/docs/release/getting_started.html) please install it first!")
        return
    import cv2
    import numpy as np
    from PIL import Image

    rgb_path = "/home/raymond/catkin_ws/src/RASberry/rasberry_data_collection/src/database_manager/video/60_rgb.png"
    depth_path = "/home/raymond/catkin_ws/src/RASberry/rasberry_data_collection/src/database_manager/video/60_depth.png"
    info_path = "/home/raymond/catkin_ws/src/RASberry/rasberry_data_collection/src/database_manager/video/60_info.npy"
    rgb = cv2.imread(rgb_path)[..., ::-1]
    depth = np.asarray(Image.open(depth_path))
    info = np.load(info_path, allow_pickle=True, encoding="latin1").item()
    fx, fy, cx, cy = info["P"][0], info["P"][5], info["P"][2], info["P"][6]

    from raytils.perception.intrinsics import deproject_depth_image

    point_cloud_image = deproject_depth_image(depth, fx, fy, cx, cy)

    z_pos = (depth / 10000.0).flatten()
    xy_pos = np.where(np.ones(depth.shape))

    points = np.ndarray((len(z_pos), 3))
    points[:, 0] = (xy_pos[0] - cx) * z_pos / fx
    points[:, 1] = ((xy_pos[1] - cy) * z_pos / fy) * -1
    points[:, 2] = z_pos * -1
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = np.reshape(rgb, (rgb.shape[0] * rgb.shape[1], 3))
    o3d.visualization.draw_geometries([pcd])
    pass


if __name__ == '__main__':
    __open3d_display_main()
