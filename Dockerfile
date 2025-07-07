# Use the official lightweight Python image
FROM python:3.12-slim

# Set a working directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr (so logs show up in real time)
ENV PYTHONUNBUFFERED=1

# Streamlit config: run in headless mode and disable CORS so it’s accessible externally
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Launch the app
ENTRYPOINT ["streamlit", "run", "st_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
