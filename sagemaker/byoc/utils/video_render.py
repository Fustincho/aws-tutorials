import cv2
import numpy as np
import gymnasium as gym

def render(action_fn, file_path):
    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter(file_path, fourcc, 30.0, (600, 400))

    env = gym.make("LunarLander-v2", render_mode='rgb_array')
    obs, state = env.reset()

    done = False
    while not done:
        action = action_fn(env)
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