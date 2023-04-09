# Use the official Python image as the base image
FROM python:3.10-buster

# Set the working directory
WORKDIR /app

# Copy the Poetry setup files into the container
COPY pyproject.toml .

# Install Poetry
RUN pip install --no-cache-dir poetry==1.4.2

# Install the dependencies
RUN poetry install

# Copy the source code, configuration, and model
COPY src/ src/
COPY config.json .
COPY model/ model/

# Expose the port used by the WebSocket server
EXPOSE 8765

# Start the WebSocket server
ENTRYPOINT ["poetry", "run", "python", "src/main.py"]