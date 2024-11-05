# API Execution Guide

## Introduction

This document provides step-by-step instructions for setting up and running the API for the healthy nutrition information system. The API is implemented in Python using the FastAPI framework and connects to a MongoDB database.

## Prerequisites

Before starting the API, ensure you have the following components installed:

- Python 3.7 or higher
- pip (Python package manager)
- MongoDB
- uvicorn

## Installation

1. **Clone the repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your_username/foodDB.git
   cd foodDB/db-api
   ```
   
2. **Create a virtual environment**

   It is recommended to create a virtual environment to manage dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   Install the required dependencies to run the API:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set up MongoDB connection**

   Due to copyright reasons, the necessary data for the MONGODB_URL environment variable is not included in the repository. Although you can run the Docker container with the MongoDB image, the database accessible from the provided URL will not contain the required information. You will need to obtain the data locally and set up your own MongoDB instance with this data.

   Export the MongoDB connection URL in your environment:

   ```bash
   export MONGODB_URL=mongodb://mongoadmin:4qJp8wDxA7@localhost:27022/
   ```

   **Note:** You must set up and load the data into your local MongoDB instance according to the instructions from your institution or data provider.

## Running the API

To start the API, run the following command in your terminal:

```bash
uvicorn app:app --reload
```

This command will start the FastAPI development server with automatic reload enabled. The API will be available at  `http://127.0.0.1:8000`.

## Verification

To verify that the API is working correctly, you can access the automatically generated interactive documentation by FastAPI at:

- Swagger Documentation: `http://127.0.0.1:8000/docs`
- Redoc Documentation: `http://127.0.0.1:8000/redoc`

## Additional Notes

- Ensure that the `27022` port, where MongoDB is running, is not blocked by a firewall or another service.
- You can modify the MongoDB connection URL and other configuration parameters as needed in your development environment.

## Conclusion

By following these steps, you should have the healthy nutrition information system's API running in your local environment. For any issues or questions, please check the project documentation or contact the system developer.
