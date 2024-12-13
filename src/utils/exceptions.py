import json

from botocore.exceptions import ClientError


class UnauthorizedError(Exception):
    """
    Exception raised when a request is unauthorized.
    """

    def __init__(self, message="Unauthorized"):
        super().__init__(message)


def handle_errors(handler):
    def wrapper(event, context):
        try:
            return handler(event, context)
        except UnauthorizedError as error:
            return {
                "statusCode": 401,
                "body": json.dumps({"message": str(error)}),
            }
        except ValueError as error:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": str(error)}),
            }
        except ClientError as error:
            return {
                "statusCode": error.response["ResponseMetadata"][
                    "HTTPStatusCode"
                ],
                "body": json.dumps(
                    {
                        "message": "An error occurred while processing your request."
                    }
                ),
            }
        except Exception as error:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"message": "An internal server error occurred."}
                ),
            }

    return wrapper
