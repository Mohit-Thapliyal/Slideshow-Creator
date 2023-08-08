# FROM python:3-alpine3.15
FROM python:3.8-slim
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install gunicorn
EXPOSE 3000
CMD ["gunicorn", "-b", "0.0.0.0:3000", "app.js"]

# # Use the official Python image as the base image
# FROM python:3.8-slim

# # Set environment variables for Flask
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=3000

# # Install libgl1-mesa-glx and libgthread-2.0 library
# RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the requirements file into the container
# COPY requirements.txt requirements.txt

# # Install project dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code into the container
# COPY . .

# # Expose the port on which the Flask app will run
# EXPOSE 3000

# # Start the Flask app
# CMD ["flask", "run"]
