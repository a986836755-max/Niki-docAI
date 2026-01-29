# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies and the package itself
RUN pip install --no-cache-dir .

# Set the entrypoint to the ndoc CLI
ENTRYPOINT ["ndoc"]

# Default argument
CMD ["--help"]
