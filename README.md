# AwsAutoTagger
Auto tag new AWS Resources

*Setup*
1. Navigate to the AWS Config Service in the desired AWS Region (Type "config" into the search bar in the AWS Console)
2. Select "Get Started"
3. Keep the Defaults for "Recording method" and "Data governance"
4. For the S3 Bucket:
    1. You MUST use a bucket with the proper bucket policy and permissions (The Config Service will set this up for you)
    2. You can share the same bucket across Config Services in multiple regions
    3. If this is the first region you are configuring the Config Service in select "Create a bucket" (this should be selected by default)
         1. You can accept the default S3 Bucket name or customize it
    1. If you have already setup Config Service in another region you can reuse the existing bucket by seleting "Choose a bucket from your account" (this should be slected by default)
         1. Select the appropriate bucket in the "S3 Bucket name" field (It should auto populate this by default)
    3. Leave the S3 "Prefix" blank and do not set an "Amazon SNS topic"
4. Click "Next"
5. On the "AWS Managed Rules" page keep the defaults and click "Next"
6. On the "Review" page click "Confirm"

Todo:
- AWS Config Settings (IAM)
- AWS Config Retention (S3) Duration
- Cloud Formation Install

Works with:
- EC2 Instances (and associated ENI, SG, Vol)
- Lambda Functions
- S3 Buckets
- EKS
- ECR
- ECS
- RDS
* give the lambda function more permissions, e.g., All or PowerUser to increse list

Know not to work with:
- AWS::EC2::EC2Fleet (EKS)
- AWS::EC2::NetworkInterface (EKS)
- AWS::AutoScaling::AutoScalingGroup (EKS) - not in cloudtrail, long ARN
- AWS::EKS::Addon (EKS)