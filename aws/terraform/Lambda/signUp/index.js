const AWS = require('aws-sdk');
const cognito = new AWS.CognitoIdentityServiceProvider();

exports.handler = async (event, context) => {
    const { username, password, email, groupName, idDb } = event;

    if (!event || !event.username || !event.password || !event.email || !event.groupName || !event.idDb) {
        console.error('Missing required input parameters');
        throw new Error('Missing required input parameters');
    }

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
            {
                Name: 'custom:Role',
                Value: groupName,
            },
            {
                Name: 'custom:idDb', 
                Value: idDb,
            }
        ],
    };

    try {
        await cognito.signUp(signUpParams).promise();
        console.log('User successfully signed up');
    } catch (error) {
        if (error.code === 'UsernameExistsException') {
            console.error('Username already exists:', error);
            throw new Error('User with this username already exists');
        } else {
            console.error('Error signing up:', error);
            throw new Error('Sign-up failed');
        }
    }
    return {
        statusCode: 200,
        body: JSON.stringify({ message: 'User signed up successfully' }),
    };
};
