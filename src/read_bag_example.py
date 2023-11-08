# Source: https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/read_bag_example.py

#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

from tkinter import filedialog as fd

# # Create object for parsing command-line options
# parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
#                                 Remember to change the stream fps and format to match the recorded.")
# # Add argument which takes path to a bag file as an input
# parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
# # Parse the command line arguments to an object
# args = parser.parse_args()
# # Safety if no parameter have been given
# if not args.input:
#     print("No input paramater have been given.")
#     print("For help type --help")
#     exit()
# # Check if the given file have bag extension
# if os.path.splitext(args.input)[1] != ".bag":
#     print("The given file is not of correct file format.")
#     print("Only .bag files are accepted")
#     exit()

path = os.path.dirname(os.path.abspath(__file__))

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    filename = fd.askopenfilename(initialdir=path + "/bags/")

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    # rs.config.enable_device_from_file(config, args.input)
    # rs.config.enable_device_from_file(config, path + "/bags/2023-10-30 20:41:50.807534 - cam0.bag")
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
