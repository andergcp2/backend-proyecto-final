ERRORS = {
  "CO01": "Required field is missing",
  "CO02": "Field length is not valid",
  "CO03": "Fields with errors",
  "CO04": "Error in cognito client"
}

def customError( statusCode, errorCode, errorDetail = ''):
    return {
        "errorDetail": errorDetail,
        "errorCode": errorCode,
        "errorDescription": ERRORS[errorCode]
    }, statusCode
