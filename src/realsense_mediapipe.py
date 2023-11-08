import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyrealsense2 as rs
import time
import numpy as np
import cv2
import os

path = os.path.dirname(os.path.abspath(__file__))
mp_util_path = os.path.join(path, '..', 'mp_util')

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image

def create_mp_detector():
  # STEP 2: Create an PoseLandmarker object.
  base_options = python.BaseOptions(model_asset_path=mp_util_path+'/pose_landmarker_full.task')
  options = vision.PoseLandmarkerOptions(
      base_options=base_options,
      output_segmentation_masks=True)
  detector = vision.PoseLandmarker.create_from_options(options)
  return detector

def main():
  mp_detector = create_mp_detector()
  
  pipelines = []
  profiles = []
  
  try:
    ctx = rs.context()
    devices = ctx.query_devices()

    # start camera streams
    for i in range(len(devices)):
        pipelines.append(rs.pipeline())
        
        config = rs.config()
        config.enable_device(str(devices[i].get_info(rs.camera_info.serial_number)))   
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        
        profiles.append(pipelines[i].start(config))
    
    # Allow cameras to stabilize
    time.sleep(5)
    
    while True:
      for i, pipeline in enumerate(pipelines):
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # STEP 3: Load the input image.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=color_image)

        # STEP 4: Detect pose landmarks from the input image.
        detection_result = mp_detector.detect(mp_image)

        # STEP 5: Process the detection result. In this case, visualize it.
        annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
        cv2.imshow('Annotated Image - cam' + str(i),cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

        # segmentation_mask = detection_result.segmentation_masks[0].numpy_view()
        # visualized_mask = np.repeat(segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255
        # cv2.imshow('Visualized Mask', visualized_mask)
      
      key = cv2.waitKey(1)
      # if pressed escape exit program
      if key == 27:
          cv2.destroyAllWindows()
          break
          
  except Exception as e:
    print(e)
    pass

  finally:
      pass
      
  pipeline.stop()

    
if __name__ == "__main__":
    main()