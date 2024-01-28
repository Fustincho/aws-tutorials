FROM python:3.11 as base

# Create virtual environments
RUN python3 -m venv /env1
RUN python3 -m venv /env2

# Environment 1 setup
COPY requirements_env1.txt /
RUN /env1/bin/pip install --no-cache-dir ipykernel
RUN /env1/bin/pip install -r /requirements_env1.txt
RUN /env1/bin/python -m ipykernel install --name=env1 --display-name "Python 3.11 [pip env: Faker]"

# Environment 2 setup
COPY requirements_env2.txt /
RUN /env2/bin/pip install --no-cache-dir ipykernel
RUN /env2/bin/pip install -r /requirements_env2.txt
RUN /env2/bin/python -m ipykernel install --name=env2 --display-name "Python 3.11 [pip env: matplotlib]"
