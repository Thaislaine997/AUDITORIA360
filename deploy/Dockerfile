FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application (adjust as necessary)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]