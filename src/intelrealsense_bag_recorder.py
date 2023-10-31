import pyrealsense2 as rs
import time
import os
import numpy as np
import cv2
from datetime import datetime

path = os.path.dirname(os.path.abspath(__file__))

def main():
    pipelines = []
    profiles = []
    recorders = []
    try:
        
        ctx = rs.context()
        devices = ctx.query_devices()
        
        # print(len(devices))
        
        # device_1 = devices[0]
        
        # print(devices[0].get_info(rs.camera_info.serial_number))
        # print(devices[1])

        # start camera streams
        for i in range(len(devices)):
            pipelines.append(rs.pipeline())
            
            config = rs.config()
            
            config.enable_device(str(devices[i].get_info(rs.camera_info.serial_number)))   
            config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
            
            profiles.append(pipelines[i].start(config))
            
            
        # pipeline = rs.pipeline()
        # config = rs.config()
        # config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        
        # profile = pipeline.start(config)

        
        # Allow cameras to stabilize
        time.sleep(5)
        
        # Start recording
        print("Recording Start")
        for i in range(len(devices)): 
            recorders.append(rs.recorder(path + '/bags/' + str(datetime.now()) + ' - cam'+str(i) +'.bag', profiles[i].get_device()))

        # time.sleep(5)
        # print("exit")
        
        # Create colorizer object
        colorizer = rs.colorizer()
        
        
        
        # Streaming loop
        while True:                    
            # Camera 1
            # Wait for a coherent pair of frames: depth and color
            frames_1 = pipelines[0].wait_for_frames()
            depth_frame_1 = frames_1.get_depth_frame()
            color_frame_1 = frames_1.get_color_frame()
            if not depth_frame_1 or not color_frame_1:
                continue
            # Convert images to numpy arrays
            color_image_1 = np.asanyarray(color_frame_1.get_data())
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap_1 = colorizer.colorize(depth_frame_1)
            depth_image_1 = np.asanyarray(depth_colormap_1.get_data())

            # Camera 2
            # Wait for a coherent pair of frames: depth and color
            frames_2 = pipelines[1].wait_for_frames()
            depth_frame_2 = frames_2.get_depth_frame()
            color_frame_2 = frames_2.get_color_frame()
            if not depth_frame_2 or not color_frame_2:
                continue
            # Convert images to numpy arrays
            color_image_2 = np.asanyarray(color_frame_2.get_data())
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap_2 = colorizer.colorize(depth_frame_2)
            depth_image_2 = np.asanyarray(depth_colormap_2.get_data())

            # Stack all images horizontally
            images1 = np.hstack((color_image_1, depth_image_1))
            images2 = np.hstack((color_image_2, depth_image_2))

            images = np.vstack((images1,images2))

            # Show images from both cameras
            cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
            cv2.imshow('RealSense', images)

            # depth_images = np.zeros((2, 720, 1280, 3))
            # color_images = np.zeros((2, 720, 1280, 3))
        
            # for i in range(len(devices)):
            #     frames = pipelines[i].wait_for_frames()

            #     # Get depth frame
            #     depth_frame = frames.get_depth_frame()
                
            #     # Colorize depth frame to jet colormap
            #     depth_color_frame = colorizer.colorize(depth_frame)

            #     # Convert depth_frame to numpy array to render image in opencv
            #     depth_images[i] = np.asanyarray(depth_color_frame.get_data())
                
            #     # Get color frame
            #     color_frame = frames.get_color_frame()
                
            #     color_images[i] = np.asanyarray(color_frame.get_data())

                

            # images2 = np.vstack((depth_images, color_images))
            
            # cv2.imshow("Color and Depth Stream", images2) 
            
            key = cv2.waitKey(1)
            # if pressed escape exit program
            if key == 27:
                cv2.destroyAllWindows()
                break

        
        
        
        for pipeline in pipelines: 
            pipeline.stop()


    except Exception as e:
        print(e)
        pass

    finally:
        pass


if __name__ == "__main__":
    main()


# dev = pipe.start(config).get_device()

# # Skip first 10 seconds to allow depth to stabilize
# dev.pause()
# time.sleep(10000) 
# dev.resume()

# # only record a frame every 5 seconds
# while (auto fs = pipe.wait_for_frames())
#     {
#         dev.pause();
#         time.sleep(5000);
#         dev.resume();
#     }