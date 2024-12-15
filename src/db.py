import logging
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

logger = logging.getLogger()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("EXPENSER_DYNAMODB_EXPENSES"))

def get_all_from_dynamodb(user_id: str) -> list[dict]:
    """
    Retrieves all expenses for a user from the DynamoDB table.

    Args:
        user_id (str): The user ID (partition key).

    Returns:
        list[dict]: A list of expense items belonging to the user.

    Raises:
        ClientError: If the query operation fails.
    """
    try:
        response = table.query(
            KeyConditionExpression=Key("userId").eq(user_id),
            ProjectionExpression="expenseId, amount, categoryName, description, #dt",
            ExpressionAttributeNames={"#dt": "date"}
        )
        items = response.get("Items", [])
        if items:
            logger.info(
                f"Retrieved {len(items)} expenses for userId: {user_id}"
            )
        else:
            logger.info(f"No expenses found for userId: {user_id}")
        return items
    except ClientError as error:
        logger.error(
            f"Error retrieving expenses for userId {user_id}: {error}",
            exc_info=True,
        )
        raise


def get_from_dynamodb(user_id: str, expense_id: str) -> dict | None:
    """
    Retrieves an expense from the DynamoDB table.

    Args:
        user_id (str): The user ID (partition key).
        expense_id (str): The expense ID (sort key).

    Returns:
        dict: The expense item if found, None if not found.

    Raises:
        ClientError: If the query operation fails.
    """
    try:
        response = table.get_item(
            Key={"userId": user_id, "expenseId": expense_id},
            ProjectionExpression="expenseId, amount, categoryName, description, #dt",
            ExpressionAttributeNames={"#dt": "date"}
        )
        item = response.get("Item")
        if item:
            logger.info(f"Expense retrieved: {expense_id}")
            return item
        else:
            logger.info(
                f"Expense not found for userId: {user_id}, expenseId: {expense_id}"
            )
            return None
    except ClientError as error:
        logger.error(f"Error retrieving data: {error}", exc_info=True)
        raise error


def create_in_dynamodb(data: dict) -> None:
    """
    Saves an expense to the DynamoDB table.

    Args:
        data (dict): The expense to save.

    Raises:
        ClientError: If the create operation fails.
    """
    try:
        table.put_item(Item=data)
        logger.info(f"Expense created: {data}")
    except ClientError as error:
        logger.error(f"Error deleting expense: {error}", exc_info=True)
        raise


def update_in_dynamodb(data: dict) -> None:
    """
    Updates an expense in the DynamoDB table.

    Args:
        data (dict): The fields to update.

    Raises:
        ClientError: If the update operation fails.
    """
    try:
        update_data = {key: value for key, value in data.items() if key not in ["userId", "expenseId"]}
        
        update_expression = "SET " + ", ".join(
            f"#{key} = :{key}" for key in update_data.keys()
        )
        expression_attribute_values = {
            f":{key}": value for key, value in update_data.items()
        }
        expression_attribute_names = {f"#{key}": key for key in update_data.keys()}
        
        table.update_item(
            Key={"userId": data["userId"], "expenseId": data["expenseId"]},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ConditionExpression=Attr("userId").eq(data["userId"])
        )
        logger.info(f"Expense updated: {data}")
    except ClientError as error:
        logger.error(f"Error updating expense: {error}", exc_info=True)
        raise


def delete_in_dynamodb(user_id: str, expense_id: str) -> None:
    """
    Deletes an expense from the DynamoDB table.

    Args:
        user_id (str): The user ID of the expense owner (partition key).
        expense_id (str): The expense ID of the expense to be deleted (sort key).

    Raises:
        ClientError: If the delete operation fails.
    """
    try:
        response = table.delete_item(
            Key={"userId": user_id, "expenseId": expense_id},
            ReturnValues="ALL_OLD",
        )

        if response.get("Attributes", {}).get("expenseId") == expense_id:
            logger.info(f"Expense deleted: {expense_id}")
        else:
            logger.info(
                f"Expense {expense_id} not found for user {user_id} or deletion failed"
            )

    except ClientError as error:
        logger.error(f"Error deleting expense: {error}", exc_info=True)
        raise
