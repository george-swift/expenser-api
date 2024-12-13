import json
import uuid
from datetime import datetime

from src.utils.categories import map_category_id_to_name
from src.utils.db import (
    create_in_dynamodb,
    delete_in_dynamodb,
    get_all_from_dynamodb,
    get_from_dynamodb,
    update_in_dynamodb,
)
from src.utils.exceptions import handle_errors
from src.utils.validation import (
    validate_expense_payload,
    validate_user,
)

CORS_HEADERS = {
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
    "Access-Control-Allow-Origin": "*",
}


@handle_errors
def read_all_expenses(event):
    user_id = validate_user(event)

    expenses = get_all_from_dynamodb(user_id)

    return {
        "statusCode": 200,
        "body": json.dumps(expenses),
        "headers": CORS_HEADERS,
    }


@handle_errors
def create_expense(event, context):
    user_id = validate_user(event)

    method_payload = event.get("body", {})

    validate_expense_payload(method_payload)

    expense_id = str(uuid.uuid4())
    category_name = map_category_id_to_name(
        method_payload.get("categoryId", 0)
    )

    integration_payload = {
        **method_payload,
        "userId": user_id,
        "expenseId": expense_id,
        "categoryName": category_name,
        "description": method_payload.get("description", ""),
        "createdAt": datetime.now(datetime.timezone.utc).isoformat(),
    }

    create_in_dynamodb(integration_payload)

    return {
        "statusCode": 201,
        "body": json.dumps({"id": expense_id}),
        "headers": CORS_HEADERS,
    }


@handle_errors
def read_expense(event, context):
    user_id = validate_user(event)

    expense_id = event.get("pathParameters", {}).get("expenseId")

    expense = get_from_dynamodb(user_id, expense_id)

    if not expense:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Expense not found"}),
        }
    return {
        "statusCode": 200,
        "body": json.dumps(expense),
        "headers": CORS_HEADERS,
    }


@handle_errors
def update_expense(event, context):
    user_id = validate_user(event)

    expense_id = event.get("pathParameters", {}).get("expenseId")

    if not expense_id:
        raise ValueError("Missing expenseId in payload")

    method_payload = event.get("body", {})

    validate_expense_payload(method_payload)

    category_name = map_category_id_to_name(method_payload["categoryId"])

    integration_payload = {
        **method_payload,
        "userId": user_id,
        "expenseId": expense_id,
        "categoryName": category_name,
        "description": method_payload.get("description", ""),
        "updatedAt": datetime.now(datetime.timezone.utc).isoformat(),
    }

    update_in_dynamodb(integration_payload)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Expense updated successfully"}),
        "headers": CORS_HEADERS,
    }


@handle_errors
def delete_expense(event, context):
    user_id = validate_user(event)

    expense_id = event.get("pathParameters", {}).get("expenseId")

    if not expense_id:
        raise ValueError("Missing expenseId in path")

    delete_in_dynamodb(user_id, expense_id)

    return {"statusCode": 204, "headers": CORS_HEADERS}


def lambda_handler(event, context):
    http_method = event.get("httpMethod", "")
    resource_path = event.get("resource", "")

    if resource_path == "/expenses" and http_method == "GET":
        return read_all_expenses(event, context)
    if resource_path == "/expenses" and http_method == "POST":
        return create_expense(event)
    elif resource_path == "/expenses/{expenseId}" and http_method == "GET":
        return read_expense(event)
    elif resource_path == "/expenses/{expenseId}" and http_method == "PUT":
        return update_expense(event)
    elif resource_path == "/expenses/{expenseId}" and http_method == "DELETE":
        return delete_expense(event)
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Unsupported method or route"}),
            "headers": CORS_HEADERS,
        }
