# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME SignLanguageApp

# Run app.py when the container launches
CMD ["python", "main.py"]