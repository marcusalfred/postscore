FROM python:3.10

WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install uvicorn
RUN pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# Copy the app directory into the container
COPY app/ /app/

# Set the working directory to where the main.py is located
WORKDIR /app

# Set the Python path to include the app directory
ENV PYTHONPATH=/app

EXPOSE 5555

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]