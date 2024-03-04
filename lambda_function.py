import boto3

def lambda_handler(event, context):
    event_arn = event["resources"][0]
    
    resource_name = parse_arn(event_arn)
    resource_type = event["detail"]["configurationItem"]["resourceType"]
    timestamp = event["time"]

    print("arn= " + event_arn)
    print("resource_name= " + resource_name)
    print("resource type= " + resource_type)
    
    # Handle Special case of AWS Volume on Create
    if resource_type == "AWS::EC2::Volume":
        resource_name = getInstanceName(event, resource_name)
    
    # Lookup the User Name in CloudTrail
    user_name = lookup_user(resource_name)
        
    print("user_name= " + user_name)
    print("time= " + timestamp)
    
    # Tag the Resource
    tag_resource(event_arn, user_name, timestamp)
    
def tag_resource(arn, user_name, timestamp):
    rt_client = boto3.client('resourcegroupstaggingapi')
    response = rt_client.tag_resources(
        ResourceARNList=[
            arn
        ],
        Tags={
            'user': user_name,
            'created_at': timestamp
        }
    )
    print(response)
    

def lookup_user(resourceName):
    ct_client = boto3.client('cloudtrail')
    response = ct_client.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'ResourceName',
                'AttributeValue': resourceName
            }
        ],
        MaxResults=1
    )

    user_name=response["Events"][0]["Username"]
    return user_name
    
# Volumes created with an EC2 instance are not recorded (user name) in CloudTrail so we need
# to capture the realted EC2 instance name to look up the username
def getInstanceName(event, resource_name):
    relationships = event["detail"]["configurationItem"]["relationships"]
    print("Volume Event Found...")
    
    for val in relationships:
        if val["resourceType"] == "AWS::EC2::Instance":
            print("... is EC2 Create.  New EC2 name for resourceId= " + val["resourceId"])
            return val["resourceId"]
            
    # No EC2 instance found for Volume, keep volume name for lookup
    print("...is direct new volume create; no EC2 instance.  Keeping resourceId the same.")
    return resource_name

def parse_arn(arn):
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
    elements = arn.split(':')
    result = {'arn': elements[0],
            'partition': elements[1],
            'service': elements[2],
            'region': elements[3],
            'account': elements[4]
           }
    if len(elements) == 7:
        result['resourcetype'], result['resource'] = elements[5:]
    elif '/' not in elements[5]:
        result['resource'] = elements[5]
        result['resourcetype'] = None
    else:
        result['resourcetype'], result['resource'] = elements[5].split('/')
    return result["resource"]
