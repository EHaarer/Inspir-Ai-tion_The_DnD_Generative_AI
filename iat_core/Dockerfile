# Use the official Python base image
FROM python:3.11-slim

# Install poe
RUN pip install poetry

# Set the working directory inside the container
WORKDIR /app

# Copy the poetry files to the working directory
COPY poetry.lock pyproject.toml ./

# Install the Python dependencies
RUN poetry install 

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8080

# Run the FastAPI application using uvicorn server
CMD  ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
