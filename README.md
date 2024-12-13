# Expenser Backend

The backend service for Expenser, a serverless expense management application built using AWS Lambda, DynamoDB, Boto3 (AWS SDK) and Python. This project handles user operations in the frontend app such as creating, reading, updating, and deleting expenses while ensuring secure and efficient functionality.

---

## Features

- **Serverless Architecture**: Deployed on AWS Lambda for scalability and cost-effectiveness.
- **Data Storage**: Uses DynamoDB with a composite key (`userId` as the partition key, `expenseId` as the sort key).
- **Authentication**: Integrates with AWS Cognito for user authentication and management.
- **API Gateway**: Provides RESTful endpoints for accessing expense-related functionalities.
- **CORS Support**: Ensures cross-origin requests are handled securely.
- **Unit Tests**: Ensures code reliability using `pytest`.
- **CI/CD Workflow**: Automates deployments via GitHub Actions.

---

## Prerequisites

- **AWS Account** with the following services configured:
  - AWS Lambda
  - DynamoDB
  - API Gateway
  - Cognito
- **Python 3.12+**
- **Boto 3** (AWS SDK for Python)
- **Poetry** (for dependency management)
- **AWS CLI** (configured with the required permissions)
- **Github Secrets** (configured with the required secrets)

---

## Setup Instructions

### 1. Clone the Repository

```bash
$ git clone https://github.com/george-swift/expenser-backend.git
$ cd expenser-backend
```

### 2. Install Dependencies

Use Poetry to install the required dependencies:

```bash
$ poetry install
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
EXPENSER_DYNAMODB_EXPENSES=<your-dynamodb-table-name>
```

### 4. Run Locally

Start a local serverless environment using AWS SAM CLI

---

## Deployment

This project includes a GitHub Actions workflow for CI/CD. Follow these steps for deployment:

1. **Push to Main Branch**: Any changes pushed to the `main` branch will trigger the workflow.
2. **Workflow Execution**: The workflow will:
   - Install dependencies.
   - Package the application code and dependencies into a ZIP file.
   - Deploy the ZIP file to the specified AWS Lambda function.

### Manual Deployment

Alternatively, deploy manually using the AWS CLI:

```bash
$ poetry export -f requirements.txt --output requirements.txt
$ mkdir build && cp -r src build/
$ pip install -r requirements.txt -t build/
$ cd build && zip -r function.zip .
$ aws lambda update-function-code --function-name <lambda-function-name> --zip-file fileb://function.zip
```

---

## Directory Structure

```
.
├── .github/
│   ├── workflows/
│   │   └── upload_lambda.yml    # CI/CD workflows for uploading zip folder to AWS Lambda
├── src/
│   ├── utils/
│   │   ├── categories.py        # Utilities for expected categories of expenses in app
│   │   ├── db.py                # DynamoDB interaction logic with Boto3
│   │   ├── exceptions.py        # Utilities to handle exceptions
│   │   └── validation.py        # Utilities to handle validations
|   ├── lambda_function.py       # Lambda entry point to lambda_handler
├── tests/                       # Unit tests
├── .editorconfig                # For consistent coding styles between different IDEs
├── .env.example                 # Example environment variables
├── .flake8                      # Checks Python code against coding style
├── .gitignore                   # Specifies intentionally untracked files that Git should ignore.
├── .pre-commit-config.yaml      # For managing pre-commit hooks.
├── MAKEFILE                     # Defines set of tasks to be executed
├── README.md                    # Project documentation
├── poetry.lock                  # Poetry file to maintain same versions of dependencies
└── pyproject.toml               # Poetry configuration and dependencies are managed here
```

---

## API Endpoints

### 1. **Create Expense**

- **Method**: `POST`
- **Path**: `/expenses`
- **Request Body**:

```json
{
  "userId": "<user-id>",
  "expenseId": "<expense-id>",
  "amount": 100.0,
  "categoryId": 5,
  "description": "Dinner at a restaurant",
  "date": "2024-12-10"
}
```

- **Response**:

```json
{
  "id": "Expense ID"
}
```

### 2. **List Expenses**

- **Method**: `GET`
- **Path**: `/expenses`
- **Response**:

```json
[
  {
    "expenseId": "<expense-id>",
    "amount": 100.0,
    "categoryId": 5,
    "description": "Dinner at a restaurant",
    "date": "2024-12-10"
  }
]
```

### 3. **Get Expense**

- **Method**: `GET`
- **Path**: `/expenses/{expenseId}`
- **Response**:

```json
{
  "expenseId": "<expense-id>",
  "amount": 100.0,
  "categoryId": 5,
  "description": "Dinner at a restaurant",
  "date": "2024-12-10"
}
```

### 4. **Update Expense**

- **Method**: `PUT`
- **Path**: `/expenses/{expenseId}`
- **Request Body**:

```json
{
  "amount": 120.0,
  "categoryId": 5
}
```

- **Response**:

```json
{
  "message": "Expense updated successfully"
}
```

### 5. **Delete Expense**

- **Method**: `DELETE`
- **Path**: `/expenses/{expenseId}`

---

## Testing

Run unit tests with config in Makefile:

```bash
$ poetry run make unit-tests
```

---

## Contributing

Contributions are absolutely welcome! Kindly fork the repository and create a pull request with your changes.

---

## Show your support

Leave a ⭐️ if you like this project!

---

## License

This project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
