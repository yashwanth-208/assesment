# assesment
Develop a scheduler microservice that allows job scheduling while maintaining  critical job-related information. The service should have API endpoints for job management,  such as listing all jobs, retrieving details of a specific job by ID, and creating new jobs. 


This code implements a simple job scheduler microservice using Flask and SQLAlchemy. Let's break down the key components:

Flask Setup: We start by creating a Flask application and configuring it to use a SQLite database.

Job Model: The Job class defines the structure of our job data, including fields for job name, last run timestamp, next run timestamp, and scheduling interval.

Database Initialization: We create the database and tables using db.create_all().

Job Scheduling Logic: The run_jobs function runs in a separate thread, continuously checking for scheduled jobs to execute.

API Endpoints:

GET /jobs: This endpoint retrieves all jobs from the database and returns them in JSON format.
GET /jobs/<id>: This endpoint retrieves a specific job by its ID, providing detailed information.
POST /jobs: This endpoint allows users to create new jobs. It validates the input data, adds the job to the database, and schedules it based on the specified interval (daily or weekly).
Job Execution: The run_job function updates the job's last run and next run timestamps when the job is executed.

Threading: We use threading to run the job scheduler in the background while the Flask app serves API requests.
