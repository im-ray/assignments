# Use the official Ubuntu base image
FROM ubuntu:24.04

# Set environment variables for non-interactive apt-get and locale
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG en_US.utf8

# Install necessary dependencies, including the deadsnakes PPA for Python 3.9
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    locales \
    libpq-dev \
    python3-dev \
    postgresql \
    postgresql-contrib \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Add deadsnakes repository to install Python 3.9
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update

# Install Python 3.9 and other necessary packages
RUN apt-get install -y \
    python3.9 \
    python3.9-distutils \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install pip version 21.2.4
# RUN python3.9 -m pip install --upgrade pip==21.2.4

# Install pip version 21.2.4 without uninstalling the current version
# RUN python3.9 -m pip install --ignore-installed --upgrade pip==21.2.4

# Copy the requirements file into the container at root (/)
COPY flask_req.txt /

# Install dependencies including python3-venv
RUN apt-get update && apt-get install -y python3.9-venv python3.9-distutils python3-pip

# Create a virtual environment
RUN python3.9 -m venv /venv

# Install the dependencies in the virtual environment
# libpq-dev, python3-dev
RUN /venv/bin/pip install --no-cache-dir -r /flask_req.txt

# Set the virtual environment to be used by default
ENV PATH="/venv/bin:$PATH"


# Install the Python dependencies from flask_req.txt
# RUN pip3 install --no-cache-dir -r /flask_req.txt

# Copy the 'app' directory into the container at /app
COPY app /app

# Copy 'run.py' and 'config.py' into the root of the container
COPY run.py /
COPY config.py /

# Expose the ports for both the Flask app (5000) and PostgreSQL (5432)
EXPOSE 5000 5432

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Give execute permissions to the entrypoint script
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["python3", "run.py"]
