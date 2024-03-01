import boto3

def lambda_handler(event, context):
    event_arn = event["resources"][0]
    
    resource_name = parse_arn(event_arn)

    print("arn= " + event_arn)
    print("resource_name= " + resource_name)
    
    
    user_name = lookup_user(resource_name)
    timestamp = event["time"]
    
    print("user_name= " + user_name)
    print("time= " + timestamp)
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
