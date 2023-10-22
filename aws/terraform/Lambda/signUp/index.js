const AWS = require('aws-sdk');
const cognito = new AWS.CognitoIdentityServiceProvider();

exports.handler = async (event, context) => {
    const { username, password, email } = event;

    const cognitoClientId = process.env.COGNITO_CLIENT_ID; // Retrieve Cognito Client ID from environment variable

    // Sign up the user in Cognito
    const signUpParams = {
        ClientId: cognitoClientId,
        Username: username,
        Password: password,
        UserAttributes: [
            {
                Name: 'email',
                Value: email,
            },
        ],
    };

    try {
        await cognito.signUp(signUpParams).promise();
        console.log('User successfully signed up');
    } catch (error) {
        console.error('Error signing up:', error);
        throw new Error('Sign-up failed');
    }

    // You can also send a confirmation code to the user's email and confirm it here.

    // Return a response
    return {
        statusCode: 200,
        body: JSON.stringify({ message: 'User signed up successfully' }),
    };
};
