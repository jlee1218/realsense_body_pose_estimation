import pyrealsense2 as rs
import numpy as np
import cv2
import os.path
from tkinter import filedialog as fd
from pathlib import Path

path = os.path.dirname(os.path.abspath(__file__))

def save_to_video(file_path):
    try:
        file_name = Path(file_path).stem
        
        print("Converting " + file_name + " to video")
        
        # Create pipeline
        pipeline = rs.pipeline()
    
        # Create a config object
        config = rs.config()
    
        rs.config.enable_device_from_file(config, file_path, False)
    
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
        color_out = cv2.VideoWriter(path + '/videos/' + file_name + ' - rgb.mp4', fourcc, 30.0, (color_frame_width, color_frame_height))
        depth_out = cv2.VideoWriter(path + '/videos/' + file_name + ' - depth.mp4', fourcc, 30.0, (depth_frame_width, depth_frame_height))
        
        try: 
            # Streaming loop
            while True:
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                depth_color_frame = colorizer.colorize(depth_frame)
                depth_color_image = np.asanyarray(depth_color_frame.get_data())
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


def main():
    file_paths = fd.askopenfilenames(initialdir = path + "/bags/")
    
    for file_path in file_paths:
        save_to_video(file_path)
    

if __name__ == "__main__":
    main()