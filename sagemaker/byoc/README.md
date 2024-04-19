# Bring Your Own Container (BYOC) to SageMaker

Welcome to an exciting journey where you won't just be learning about AWS SageMaker's capabilities but will also be taking a small detour to the moon! Well, not literally, but close enough. In this session, we dive into the concept of **Bring Your Own Container (BYOC)** to SageMaker, empowering you to deploy custom training and inference containers. As a fun twist, we will train a Reinforcement Learning (RL) model in the [LunarLander-v2](https://www.gymlibrary.dev/environments/box2d/lunar_lander/) environment from Gymnasium to master a lunar landing!

Fear not if you're not a Reinforcement Learning guru! The primary goal here isn't to deep dive into the complexities of RL algorithms. Instead, we focus on the practical steps to **BYOC in SageMaker**. This tutorial is designed to be accessible, providing you with the knowledge to leverage SageMaker's powerful features using containers you configure.

## Part 1: Building and Training Your Container

### Overview

In the first part of our mission, we'll focus on the initial stages of using your own container with SageMaker:

1. **Build Your Training Container:** First, we'll cover the essentials of crafting your very own Docker container suitable for training models. This includes setting up the necessary dependencies and environment configurations.
2. **Create and Run a Training Job:** Once our container is ready, you'll learn how to launch a training job in SageMaker using this custom setup. We'll guide you through configuring the SageMaker training job to use your container, so our virtual lander learns how to touch down smoothly on the moon.

### Getting Started

Let’s prepare our tools and get ready to build a container that’s not just a module, but a moon module!

## Part 2: Inference and Deployment

### Overview

The second part of our tutorial will take you through the steps needed to see your training come to life in a real-world application:

1. **Develop an Inference Container:** After training, the next step is to create an inference container. This part of the tutorial will show you how to prepare your container for making predictions.
2. **Deploy Your Model as a SageMaker Endpoint:** We will walk you through deploying your trained RL model as a SageMaker Endpoint, ready to make predictions—or in our case, successful lunar landings.

### Launching Your Model

Now that our training is complete, let’s deploy it to see how well our virtual lunar lander can perform in the real (simulated) world!

---

Let's get started, and prepare for a smooth landing in the fascinating world of SageMaker!
