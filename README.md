# Service Request Management System

This project is a Django-based web application for managing service requests. It includes functionalities for user signup, login, service request submission, tracking, and staff management.

## Features

- User authentication (signup, login, logout)
- Service request submission and tracking
- Staff dashboard for managing service requests
- Profile view for logged-in users

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd asn2
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Apply migrations:
    ```sh
    python manage.py migrate
    ```
5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```
6. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`
- Sign up for a new account or log in with an existing account
- Submit and track service requests
- Staff users can log in to access the staff dashboard and manage service requests

## Running Tests

To run the tests, use the following command:
```sh
python manage.py test
```
