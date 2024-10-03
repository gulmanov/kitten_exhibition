# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Copy the pre-downloaded packages
COPY ./vendor /app/vendor/

# Install any necessary dependencies from the pre-downloaded files
RUN pip install --no-index --find-links=/app/vendor -r requirements.txt


# Copy the wait-for-it.sh script into the Docker image
COPY wait-for-it.sh /wait-for-it.sh

# Give the wait-for-it.sh script executable permissions
RUN chmod +x /wait-for-it.sh

# Copy the current directory contents into the container at /app
COPY . /app/

# Set environment variables to disable buffering and allow easier log management
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the port that the application runs on
EXPOSE 8000

# Run the Django development server
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
