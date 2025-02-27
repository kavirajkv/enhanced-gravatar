# Enhanced Gravatar Application

This is a Flask-based application that allows users to retrieve and store their profile information, including Gravatar details. The application uses Redis for data storage.

## Prerequisites

- Docker and Docker Compose (for running with Docker)
- Python 3.x (for running locally)
- Redis (for running locally)

## Getting Started

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/kavirajkv/enhanced-gravatar.git
cd enhanced-gravatar
```

### 2. Use docker compose to run 

At project root folder / where docker compose file exist

```bash
docker compose up
```

### 3. To run the application locally

Make sure your redis server running 

```bash
redis-server
```

Then at project root folder run the below command

```bash
make run
```


