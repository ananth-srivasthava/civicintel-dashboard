# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install the required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run requires port 8080
EXPOSE 8080

# The command to launch your Streamlit app
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8080", "--server.address=0.0.0.0"]