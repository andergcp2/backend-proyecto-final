
resource "aws_cognito_user_pool" "mi_user_pool" {
  name = "user-pool"
  
  password_policy {
    minimum_length = 6
  }

  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_subject = "Account Confirmation"
    email_message = "Your confirmation code is {####}"
  }

  schema {
    attribute_data_type      = "String"
    developer_only_attribute = false
    mutable                  = true
    name                     = "email"
    required                 = true

    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
  }

  lambda_config {
    pre_sign_up    = aws_lambda_function.pre_sign_up.arn
  }
}

resource "aws_cognito_user_pool_client" "mi_user_pool_client" {
  name = "cognito-client"

  user_pool_id = aws_cognito_user_pool.mi_user_pool.id
  generate_secret = false
  refresh_token_validity = 90
  prevent_user_existence_errors = "ENABLED"
  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]
  
}

resource "aws_cognito_user_pool_domain" "cognito-domain" {
  domain       = "abc-domain"
  user_pool_id = "${aws_cognito_user_pool.mi_user_pool.id}"
}


# Create an AWS Lambda function
resource "aws_lambda_function" "cognito_signup_lambda" {
  function_name = "cognito-signup-lambda"
  handler = "index.handler"
  runtime = "nodejs14.x"
  memory_size = 256
  timeout = 10
  source_code_hash = filebase64sha256("${path.module}/lambda_function_signup.zip")

  role = aws_iam_role.lambda_execution_role.arn

  filename = "lambda_function_signup.zip"

  environment {
    variables = {
      COGNITO_CLIENT_ID = aws_cognito_user_pool_client.mi_user_pool_client.id, # Replace with your Cognito App Client ID
    }
  }
}

# Create an AWS Lambda function
resource "aws_lambda_function" "cognito_login_lambda" {
  function_name = "cognito-login-lambda"
  handler = "index.handler"
  runtime = "nodejs14.x"
  memory_size = 256
  timeout = 10
  source_code_hash = filebase64sha256("${path.module}/lambda_function_login.zip")

  role = aws_iam_role.lambda_execution_role.arn

  filename = "lambda_function_login.zip"

  environment {
    variables = {
      COGNITO_CLIENT_ID = aws_cognito_user_pool_client.mi_user_pool_client.id, # Replace with your Cognito App Client ID
    }
  }
}

# Create an AWS Lambda function
resource "aws_lambda_function" "pre_sign_up" {
  function_name = "cognito-confirm-lambda"
  handler = "index.handler"
  runtime = "nodejs14.x"
  memory_size = 256
  timeout = 10
  source_code_hash = filebase64sha256("${path.module}/lambda_function_confirm.zip")
  role = aws_iam_role.lambda_execution_role.arn
  filename = "lambda_function_confirm.zip"
}

# IAM role for Lambda execution
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# Attach necessary IAM policies to the Lambda execution role
resource "aws_iam_policy_attachment" "lambda_execution_policy" {
  name = "lambda_execution_policy"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  roles = [aws_iam_role.lambda_execution_role.name]
}