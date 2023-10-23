# Recurso de Autorizador en API Gateway
# Crear una API Gateway
resource "aws_api_gateway_rest_api" "mi_api" {
  name        = "Simple ABC (Terraform)"
  description = "Mi API Gateway"
}

# Recurso de Rol IAM para el autorizador de Cognito
resource "aws_iam_role" "mi_iam_role" {
  name = "mi-iam-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Federated = "cognito-identity.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_api_gateway_authorizer" "mi_authorizer" {
  name            = "mi-authorizer"
  rest_api_id      = aws_api_gateway_rest_api.mi_api.id
  type            = "COGNITO_USER_POOLS"
  identity_source = "method.request.header.Authorization"
  provider_arns   = [aws_cognito_user_pool.mi_user_pool.arn]
  authorizer_credentials = aws_iam_role.mi_iam_role.arn
}


# Configurar Companies resource
resource "aws_api_gateway_resource" "mi_recurso" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  parent_id   = aws_api_gateway_rest_api.mi_api.root_resource_id
  path_part   = "companies"
}
resource "aws_api_gateway_resource" "mi_parametro_recurso" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  parent_id   = aws_api_gateway_resource.mi_recurso.id
  path_part   = "{companyId}"
}
resource "aws_api_gateway_method" "get_method" {
  rest_api_id   = aws_api_gateway_rest_api.mi_api.id
  resource_id   = aws_api_gateway_resource.mi_recurso.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.mi_authorizer.id
}
resource "aws_api_gateway_method" "post_method" {
  rest_api_id   = aws_api_gateway_rest_api.mi_api.id
  resource_id   = aws_api_gateway_resource.mi_recurso.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.mi_authorizer.id
}
resource "aws_api_gateway_integration" "get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.mi_api.id
  resource_id             = aws_api_gateway_resource.mi_recurso.id
  http_method             = aws_api_gateway_method.get_method.http_method
  type                    = "HTTP_PROXY"
  integration_http_method = "GET"
  uri                     = "http://35.172.225.133/companies"
}
resource "aws_api_gateway_integration" "post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.mi_api.id
  resource_id             = aws_api_gateway_resource.mi_recurso.id
  http_method             = aws_api_gateway_method.post_method.http_method
  type                    = "HTTP_PROXY"
  integration_http_method = "POST"
  uri                     = "http://35.172.225.133/companies"
}


# Configurar Congito resources
resource "aws_api_gateway_resource" "mi_recurso_signup" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  parent_id   = aws_api_gateway_rest_api.mi_api.root_resource_id
  path_part   = "signin"
}
resource "aws_api_gateway_resource" "mi_recurso_token" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  parent_id   = aws_api_gateway_rest_api.mi_api.root_resource_id
  path_part   = "token"
}
resource "aws_api_gateway_method" "post_signup" {
  rest_api_id   = aws_api_gateway_rest_api.mi_api.id
  resource_id   = aws_api_gateway_resource.mi_recurso_signup.id
  http_method   = "POST"
  authorization = "NONE"
}
resource "aws_api_gateway_method" "get_token" {
  rest_api_id   = aws_api_gateway_rest_api.mi_api.id
  resource_id   = aws_api_gateway_resource.mi_recurso_token.id
  http_method   = "POST"
  authorization = "NONE"
}
resource "aws_api_gateway_integration" "signup_integration" {
  rest_api_id             = aws_api_gateway_rest_api.mi_api.id
  resource_id             = aws_api_gateway_resource.mi_recurso_signup.id
  http_method             = aws_api_gateway_method.post_signup.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.cognito_signup_lambda.invoke_arn
  passthrough_behavior    = "WHEN_NO_TEMPLATES"
}
resource "aws_api_gateway_integration" "login_integration" {
  rest_api_id             = aws_api_gateway_rest_api.mi_api.id
  resource_id             = aws_api_gateway_resource.mi_recurso_token.id
  http_method             = aws_api_gateway_method.get_token.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.cognito_login_lambda.invoke_arn
  passthrough_behavior    = "WHEN_NO_TEMPLATES"
}
resource "aws_api_gateway_method_response" "singup_response_200" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  resource_id = aws_api_gateway_resource.mi_recurso_signup.id
  http_method = aws_api_gateway_method.post_signup.http_method
  status_code = "200"
}
resource "aws_api_gateway_method_response" "login_response_200" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  resource_id = aws_api_gateway_resource.mi_recurso_token.id
  http_method = aws_api_gateway_method.get_token.http_method
  status_code = "200"
}
resource "aws_api_gateway_method_response" "singup_response_500" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  resource_id = aws_api_gateway_resource.mi_recurso_signup.id
  http_method = aws_api_gateway_method.post_signup.http_method
  status_code = "500"
}
resource "aws_api_gateway_method_response" "login_response_500" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  resource_id = aws_api_gateway_resource.mi_recurso_token.id
  http_method = aws_api_gateway_method.get_token.http_method
  status_code = "500"
}
resource "aws_api_gateway_integration_response" "singup_i_response_500" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  resource_id = aws_api_gateway_resource.mi_recurso_signup.id
  http_method = aws_api_gateway_method.post_signup.http_method
  status_code = aws_api_gateway_method_response.singup_response_500.status_code
  depends_on = [
    aws_api_gateway_integration.signup_integration
  ]
}
resource "aws_api_gateway_integration_response" "login_i_response_500" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  resource_id = aws_api_gateway_resource.mi_recurso_token.id
  http_method = aws_api_gateway_method.get_token.http_method
  status_code = aws_api_gateway_method_response.login_response_500.status_code
  depends_on = [
    aws_api_gateway_integration.login_integration
  ]
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cognito_signup_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.mi_api.id}/*/${aws_api_gateway_method.post_signup.http_method}${aws_api_gateway_resource.mi_recurso_signup.path}"
}
resource "aws_lambda_permission" "apigw_lambda_2" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cognito_login_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.mi_api.id}/*/${aws_api_gateway_method.get_token.http_method}${aws_api_gateway_resource.mi_recurso_token.path}"
}


# Crear un despliegue
resource "aws_api_gateway_deployment" "mi_deployment" {
  rest_api_id = aws_api_gateway_rest_api.mi_api.id
  depends_on = [
    "aws_api_gateway_integration.signup_integration",
    "aws_api_gateway_integration.login_integration",
    "aws_api_gateway_integration.get_integration",
    "aws_api_gateway_integration.post_integration",
  ]

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.mi_api.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.mi_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.mi_api.id
  stage_name    = "test"
}

