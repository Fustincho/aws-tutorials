FROM python:3.11 as base

# Create virtual environment
RUN pip install --upgrade pip
RUN pip install swig
RUN python3 -m venv /env1

# Environment 1 setup
COPY requirements.txt /
RUN /env1/bin/pip install --no-cache-dir ipykernel
RUN /env1/bin/pip install --no-cache-dir swig
RUN /env1/bin/pip install -r /requirements.txt
RUN /env1/bin/python -m ipykernel install --name=env1 --display-name "py3.11 [RL: Lunar Lander]"
