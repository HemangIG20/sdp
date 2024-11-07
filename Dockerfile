# Step 1: Use the official Python base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file to the container
COPY requirements.txt /app/

# Step 4: Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the entire app into the container
COPY . /app/

# Step 6: Expose port 5000 (default Flask port)
EXPOSE 5000

# Step 7: Set the environment variable to tell Flask to run in production
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Step 8: Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
