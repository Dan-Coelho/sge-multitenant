# Project Overview: SGE Multitenant 
# Based on the SGE Project developed in the Django Master course by PycodeBR

This document provides a comprehensive overview of the SGE Multitenant project, a multi-tenant inventory and sales management system built with Django.

## Project Purpose and Architecture

SGE Multitenant is a web-based application designed to allow multiple companies to manage their products, brands, inflows, and outflows in a segregated environment. Each company has its own set of users and data, ensuring privacy and security.

The project follows a standard Django architecture, with a central `app` for project-level configurations and several dedicated apps for different functionalities:

*   **`companies`**: Manages company information.
*   **`companyusers`**: Associates users with specific companies, forming the core of the multi-tenant system.
*   **`brands`**: Manages product brands.
*   **`products`**: Manages products, including their cost, selling price, and quantity.
*   **`inflows`**: Tracks product inflows (purchases).
*   **`outflows`**: Tracks product outflows (sales).

The multi-tenancy is implemented by associating each piece of data (like products, brands, etc.) with a `CompanyUser`, which in turn is linked to a specific `Company`.

## Technologies Used

*   **Backend**: Django
*   **Database**: PostgreSQL
*   **Frontend**: Django Templates
*   **Containerization**: Docker (optional, based on `docker-compose.yml` and `Dockerfile`)

## Building and Running the Project

To build and run the project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd sge_multitenant
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up the database:**
    *   Make sure you have a PostgreSQL server running.
    *   Create a database named `sge_multitenant` with a user `postgres` and password `postgres`.
    *   Alternatively, you can use the provided `docker-compose.yml` to spin up a PostgreSQL container:
        ```bash
        docker-compose up -d
        ```

4.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000`.

## Development Conventions

*   **Coding Style**: The project uses `flake8` for linting. Adhere to PEP 8 standards.
*   **Multi-tenancy**: All new models that should be company-specific must have a `ForeignKey` to the `CompanyUser` model.
*   **Admin Panels**: The project has two admin panels:
    *   `/admin/`: For superusers to manage all data.
    *   `/portal/`: A company-specific admin panel for managing company data.
*   **Templates**: Templates are organized within each app's `templates` directory. Global templates are located in the `app/templates` directory.
