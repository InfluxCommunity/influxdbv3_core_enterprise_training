# Start with the InfluxDB v3 core image
FROM quay.io/influxdb/influxdb3-core:latest
# Install system dependencies
USER root
# Create app directory and set it as working directory early
RUN mkdir -p /app
WORKDIR /app
# Install system packages
RUN apt-get update && apt-get install -y     python3     python3-pip     python3-venv     wget     gnupg     && rm -rf /var/lib/apt/lists/*
# Install Telegraf
RUN curl -s https://repos.influxdata.com/influxdata-archive.key | gpg --dearmor > /etc/apt/trusted.gpg.d/influxdata-archive.gpg     && echo "deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive.gpg] https://repos.influxdata.com/debian stable main" > /etc/apt/sources.list.d/influxdata.list     && apt-get update     && apt-get install -y telegraf
# Create necessary directories inside /app
RUN mkdir -p /app/data     && mkdir -p /app/plugins
# Create and configure virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/venv"
# Install Python packages in virtual environment
RUN pip3 install --no-cache-dir     pandas     numpy     influxdb3-python
# Add plugins directory to Python path
ENV PYTHONPATH="/app/plugins:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1
# Expose ports
EXPOSE 8181