# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port that the app will run on
EXPOSE 8080

# Set the command to run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]

