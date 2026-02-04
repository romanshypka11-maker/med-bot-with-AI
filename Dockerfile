
FROM python:3.11-slim
LABEL authors="Roman Shypka"

#Set the working directory insade the container
WORKDIR /app

#copy librars for project
COPY requirements.txt .

# install all a librars
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Document that the application listens on port 8000
EXPOSE 8000