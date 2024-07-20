# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy crontab file to the cron.d directory
COPY crontab.txt /etc/cron.d/daily_email

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/daily_email

# Apply the cron job
RUN crontab /etc/cron.d/daily_email

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && python app.py
