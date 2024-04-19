import cv2
import numpy as np
import gymnasium as gym
import subprocess
import os
from typing import Callable, Tuple

def convert_video(input_path, output_path):
    """
    Convert a video file from MPEG-4 to H.264 format using ffmpeg.

    Parameters:
    input_path (str): The file path of the input video.
    output_path (str): The file path where the converted video will be saved.

    The function executes an ffmpeg command to convert the video and handles the
    process outcome, printing a success message or error details.
    """
    # MPEG-4 to H.264
    command = [
        'ffmpeg', 
        '-hide_banner', 
        '-loglevel', 'error', 
        '-y', 
        '-i', input_path, 
        output_path
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        print(f"Video conversion successful: {output_path}")
    else:
        print("Video conversion failed.")
        print(result.stderr.decode())

def record_simulation(action_fn: Callable[[gym.Env, np.ndarray], int], file_path: str):
    """Renders a video of an agent performing in a Gym environment: LunarLander-v2.
    
    Args:
        action_fn: Function to determine the action to take based on 
                   the environment and observation.
        file_path: The output file path for the final video.
    """
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    mpeg4_path = os.path.dirname(file_path) + "/mpeg4.mp4"
    video = cv2.VideoWriter(mpeg4_path, fourcc, 30.0, (600, 400))

    env = gym.make("LunarLander-v2", render_mode='rgb_array')
    obs, state = env.reset()

    done = False
    while not done:
        action = action_fn(env, obs)
        obs, reward, terminated, truncated , info = env.step(action)
        if terminated:
            break
        frame = env.render()

        # Convert RGB to BGR (OpenCV uses BGR by default)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video.write(frame)

    # Release everything when job is finished
    env.close()
    video.release()
    
    convert_video(mpeg4_path, file_path)
    os.remove(mpeg4_path)

def make_model_action(model):
    def model_action(env: gym.Env, obs: np.ndarray) -> int:
        action, _ = model.predict(obs)
        return action
    return model_action

