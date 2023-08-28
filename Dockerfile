# Use the official Alpine image as the base image
FROM python:3.9-alpine

# Set environment variables for Python and output buffering
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# RUN apk update && apk add --no-cache pkgconfig mariadb-dev

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache pkgconfig mariadb-dev


# Set the working directory in the container
WORKDIR /LessonPlan/backend

# Copy the requirements file into the container at /backend
COPY requirements.txt /LessonPlan/backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend/backendlication code into the container at /backend
COPY . /LessonPlan/backend/

# Expose the port that the Django development server will run on
EXPOSE 7070

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:7070"]

# ENTRYPOINT [ "sh" , "./entrypoint.sh" ]


