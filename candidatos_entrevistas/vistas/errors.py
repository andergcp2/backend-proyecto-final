ERRORS = {
  "CO01": "Required field is missing",
  "CO02": "Field length is not valid",
  "CO03": "Fields with errors",
  "CO04": "Error in cognito client",
  "CO05": "Duplicate registration error",
  "CO06": "Date is not valid"
}

def customError( statusCode, errorCode, errorDetail = ''):
    return {
        "errorDetail": errorDetail,
        "errorCode": errorCode,
        "errorDescription": ERRORS[errorCode]
    }, statusCode
