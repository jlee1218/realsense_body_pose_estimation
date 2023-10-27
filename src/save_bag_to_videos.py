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

from datetime import datetime

path = os.path.dirname(os.path.abspath(__file__))

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    # rs.config.enable_device_from_file(config, args.input)
    rs.config.enable_device_from_file(config, path + "/bags/test4.bag", False)

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    config.enable_stream(rs.stream.depth, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, rs.format.bgr8, 30)

    # Start streaming from file
    pipeline.start(config)
    
    # Create colorizer object
    colorizer = rs.colorizer()
    
    # Use first frame to get dimensions
    frame = pipeline.wait_for_frames()
    depth_frame_width = frame.get_depth_frame().width
    depth_frame_height = frame.get_depth_frame().height
    color_frame_width = frame.get_color_frame().width
    color_frame_height = frame.get_color_frame().height
    
    
    # MP4 Format
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    color_out = cv2.VideoWriter(path + '/videos/' + str(datetime.now()) + ' - rgb.mp4', fourcc, 30.0, (color_frame_width, color_frame_height))
    depth_out = cv2.VideoWriter(path + '/videos/' + str(datetime.now()) + ' - depth.mp4', fourcc, 30.0, (depth_frame_width, depth_frame_height))
    
    try: 
    
        # Streaming loop
        while True:
            # 
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
            
            color_out.write(color_image)
            depth_out.write(depth_color_image)
            
    except:
        # When all frames are read, pipepline will be empty and an exception will be thrown
        color_out.release()
        depth_out.release()
        
finally:
    pass
