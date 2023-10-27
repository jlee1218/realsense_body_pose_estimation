import pyrealsense2 as rs
import time
import os
from datetime import datetime

path = os.path.dirname(os.path.abspath(__file__))

def main():
    try:
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
        # config.enable_record_to_file(path + '/bags/' + datetime.now() + '.bag')

        profile = pipeline.start(config)

        recorder = rs.recorder(path + '/bags/' + str(datetime.now()) + '.bag', profile.get_device())

        time.sleep(10)
        print("exit")


    except Exception as e:
        print(e)
        pass

    finally:
        pipeline.stop()


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