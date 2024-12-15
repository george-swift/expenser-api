import datetime
import uuid
from decimal import Decimal
from categories import map_category_id_to_name
from db import (
    create_in_dynamodb,
    delete_in_dynamodb,
    get_all_from_dynamodb,
    get_from_dynamodb,
    update_in_dynamodb,
)
from exceptions import handle_errors
from validation import validate_expense_payload, validate_user

CORS_HEADERS = {
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json"
}


@handle_errors
def read_all_expenses(event):
    user_id = validate_user(event)

    expenses = get_all_from_dynamodb(user_id)

    return {
        "statusCode": 200,
        "body": expenses,
        "headers": CORS_HEADERS,
    }


@handle_errors
def create_expense(event):
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
        "amount": Decimal(str(method_payload['amount'])),
        "categoryName": category_name,
        "description": method_payload.get("description", ""),
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    create_in_dynamodb(integration_payload)

    return {
        "statusCode": 201,
        "body": {"id": expense_id},
        "headers": CORS_HEADERS,
    }


@handle_errors
def read_expense(event):
    user_id = validate_user(event)

    expense_id = event.get("pathParameters", {}).get("expenseId")

    expense = get_from_dynamodb(user_id, expense_id)

    if not expense:
        return {
            "statusCode": 404,
            "body": {"message": "Expense not found"},
        }
    return {
        "statusCode": 200,
        "body": expense,
        "headers": CORS_HEADERS,
    }


@handle_errors
def update_expense(event):
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
        "amount": Decimal(str(method_payload['amount'])),
        "categoryName": category_name,
        "description": method_payload.get("description", ""),
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    update_in_dynamodb(integration_payload)

    return {
        "statusCode": 200,
        "body": {"message": "Expense updated successfully"},
        "headers": CORS_HEADERS,
    }


@handle_errors
def delete_expense(event):
    user_id = validate_user(event)

    expense_id = event.get("pathParameters", {}).get("expenseId")

    if not expense_id:
        raise ValueError("Missing expenseId in path")

    delete_in_dynamodb(user_id, expense_id)

    return {"statusCode": 204, "headers": CORS_HEADERS}


def lambda_handler(event, context):
    http_method = event.get("httpMethod", "")
    resource_path = event.get("resource", "")
    path_parameters = event.get("pathParameters", {})

    if resource_path == "/expenses" and http_method == "GET":
        return read_all_expenses(event)
    if resource_path == "/expenses" and http_method == "POST":
        return create_expense(event)
    elif resource_path.startswith("/expenses") and http_method in ["GET", "PUT", "DELETE"]:
        expense_id = path_parameters.get("expenseId")
        if expense_id:
            if http_method == "GET":
                return read_expense(event)
            elif http_method == "PUT":
                return update_expense(event)
            elif http_method == "DELETE":
                return delete_expense(event)
        else:
            return {
                "statusCode": 400,
                "body": {"message": "Missing required expenseId"},
                "headers": CORS_HEADERS,
            }
    else:
        return {
            "statusCode": 404,
            "body": {"message": "Unsupported method or route"},
            "headers": CORS_HEADERS,
        }
