# This Dockerfile sets up a Python environment for running an application that parses HTML docuemnt
# and extracts attributes related to e-commerce products and returns the 
# extracted attributes and their selectoes/xpaths in JSON format.

# It uses the official Python 3.9-slim base image.
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the local directory to the /app directory in the container
ADD requirements.txt ./

# Install the Python dependencies specified in the requirements.txt file
RUN pip install -r requirements.txt

# Copy all the files from the local directory to the /app directory in the container
COPY . .

# Expose port 8000 to allow incoming connections
EXPOSE 8000

# Set the command to run when the container starts
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]