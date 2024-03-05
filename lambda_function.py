import boto3

def lambda_handler(event, context):
    event_arn = event["resources"][0]
    
    resource_name = parse_arn(event_arn)
    if resource_name is None:
        return #can't proceed

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
    if user_name is None:
        return #can't proceed
        
    print("user_name= " + user_name)
    #print("time= " + timestamp)
    
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

    event_list=response["Events"]
    if not event_list:
        print("ResourceName " + resourceName + " not in CloudTrail")
        return None
    
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
    #arn:aws:eks:us-west-2:536506487112:addon/testy2/coredns/80c70604-2e61-4b46-45e5-58e39fc72b94
    #arn:aws:autoscaling:us-west-2:536506487112:autoScalingGroup:9796b4f3-a7db-4401-8443-445be4e0da8e:autoScalingGroupName/eks-default-node-pool-82c70605-7b57-3d97-8ea2-1c9b69858b0d
    #arn:aws:ec2:us-west-2:536506487112:instance/i-0d749cf8a07eebe9a
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
    elements = arn.split(':')
    result = {'arn': elements[0],
            'partition': elements[1],
            'service': elements[2],
            'region': elements[3],
            'account': elements[4]
           }
    
    if len(elements) == 8 and '/' in elements[7]:
        elements2 = elements[7].split('/')
        l = len(elements2)
        result['resourcetype'], result['resource'] = elements2[l-2], elements2[l-1]
    elif len(elements) == 7:
        result['resourcetype'], result['resource'] = elements[5:]
    elif '/' not in elements[5]:
        result['resource'] = elements[5]
        result['resourcetype'] = None
    elif '/' in elements[5]:
        elements2 = elements[5].split('/')
        l = len(elements2)
        result['resourcetype'], result['resource'] = elements2[l-2], elements2[l-1]
    else:
        print("Can't parse ARN= " + arn)
        return None
    return result["resource"]