# Use the official lightweight Python image
FROM python:3.12-slim

# Set a working directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr (so logs show up in real time)
ENV PYTHONUNBUFFERED=1

# Streamlit config: run in headless mode and disable CORS so it's accessible externally
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Install system dependencies for geospatial libraries
RUN apt-get update && apt-get install -y \
    libexpat1 \
    libexpat1-dev \
    libgdal-dev \
    gdal-bin \
    libgeos-dev \
    libproj-dev \
    libspatialite-dev \
    libsqlite3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Launch the app
ENTRYPOINT ["streamlit", "run", "st_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.baseUrlPath=/dynamic-bharat"]