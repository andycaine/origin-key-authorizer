# origin-key-authorizer

A Lambda authorizer that can be used to ensure that calls are made via CloudFront.

## Description

Putting a CloudFront distribution in front of your app can be a great way to boost security. For example, you can use CloudFront to [absorb distributed denial of service (DDoS) attacks](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ConfiguringCaching.html), [integrate with AWS WAF](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-awswaf.html) to protect against a range of exploits, and [add common security-related HTTP headers to your responses](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-response-headers-policies.html).

Of course, this is only effective if you can prevent users from accessing your origin directly. `origin-key-authorizer` is a simple Lambda authorizer that can be used to validate a custom header passed from CloudFront in order to protect AWS API Gateway HTTP API origins.

## Getting started

`origin-key-authorizer` is available via the AWS Serverless Application Repository. To include it in your CloudFormation template and use it to protect your HTTP API origin:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: 'AWS::Serverless-2016-10-31'
Description: An example stack showing the use of origin-key-authorizer
Resources:

  OriginKey:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: OriginKey
      GenerateSecretString:
        ExcludePunctuation: true
        PasswordLength: 64

  OriginKeyAuthorizer:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: 'arn:aws:serverlessrepo:eu-west-2:211125310871:applications/origin-key-authorizer'
        SemanticVersion: <CURRENT_VERSION>
      Parameters:
        OriginKey: !Sub '{{resolve:secretsmanager:${OriginKey}}}'

  MyApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      Auth:
        Authorizers:
          OriginKeyAuthorizer:
            FunctionArn: !GetAtt OriginKeyAuthorizer.Outputs.OriginKeyAuthorizerArn
            AuthorizerPayloadFormatVersion: 2.0
            EnableSimpleResponses: true
            FunctionInvokeRole: !GetAtt OriginKeyAuthorizer.Outputs.LambdaAuthorizerRoleArn
            Identity:
              ReauthorizeEvery: 300
              Headers:
                - 'X-Custom-Origin-Key'
        DefaultAuthorizer: OriginKeyAuthorizer

```

Now you can deploy your stack. These steps assume you have the [SAM CLI installed and set up for your environment](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html):

```
$ sam build
$ sam deploy \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
    --stack-name example-stack \
    --resolve-s3
```
