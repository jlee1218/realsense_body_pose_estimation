# Modified from: https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/read_bag_example.py

import pyrealsense2 as rs
import numpy as np
import cv2
import os.path
from tkinter import filedialog as fd

path = os.path.dirname(os.path.abspath(__file__))

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    filename = fd.askopenfilename(initialdir=path + "/bags/")

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, filename)


    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    config.enable_stream(rs.stream.depth, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, rs.format.bgr8, 30)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    
    # Create colorizer object
    colorizer = rs.colorizer()

    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get depth frame
        depth_frame = frames.get_depth_frame()
        
        # Colorize depth frame to jet colormap
        depth_color_frame = colorizer.colorize(depth_frame)

        # Convert depth_frame to numpy array to render image in opencv
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        
        # Get color frame
        color_frame = frames.get_color_frame()
        
        color_image = np.asanyarray(color_frame.get_data())

        # images = np.hstack((color_image, depth_color_image)) # both streams need to have the same resolution

        cv2.imshow("Color Stream", color_image)
        
        # Render image in opencv window
        cv2.imshow("Depth Stream", depth_color_image)
        
        # cv2.imshow("Color and Depth Stream", images) 
        
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            break

finally:
    pass
