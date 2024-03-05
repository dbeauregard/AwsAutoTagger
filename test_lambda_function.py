import unittest
import lambda_function

class TestLambdaFunction(unittest.TestCase):

    def test_arn_g1(self):
        result = lambda_function.parse_arn("arn:partition:service:region:account-id:resource-id")
        self.assertEqual(result, "resource-id")

    def test_arn_g2(self):
        result = lambda_function.parse_arn("arn:partition:service:region:account-id:resource-type/resource-id")
        self.assertEqual(result, "resource-id")

    def test_arn_g3(self):
        result = lambda_function.parse_arn("arn:partition:service:region:account-id:resource-type:resource-id")
        self.assertEqual(result, "resource-id")

    def test_arn_instance(self):
        result = lambda_function.parse_arn("arn:aws:ec2:us-west-2:536506487112:instance/i-0d749cf8a07eebe9a")
        self.assertEqual(result, "i-0d749cf8a07eebe9a")
    
    def test_arn_s3(self):
        result = lambda_function.parse_arn("arn:aws:s3:::config-bucket-536506487112")
        self.assertEqual(result, "config-bucket-536506487112")

    @unittest.skip("S3 Paths not yet supported")
    def test_arn_s3_path(self):
        result = lambda_function.parse_arn("arn:aws:s3:::config-bucket-536506487112/AWSLogs/536506487112/")
        self.assertEqual(result, "config-bucket-536506487112")

    def test_arn_asg(self):
        result = lambda_function.parse_arn("arn:aws:autoscaling:us-west-2:536506487112:autoScalingGroup:9796b4f3-a7db-4401-8443-445be4e0da8e:autoScalingGroupName/eks-default-node-pool-82c70605-7b57-3d97-8ea2-1c9b69858b0d")
        self.assertEqual(result, "eks-default-node-pool-82c70605-7b57-3d97-8ea2-1c9b69858b0d")

    @unittest.skip("EKS Addons not yet supported")
    def test_arn_eksaddon(self):
        result = lambda_function.parse_arn("arn:aws:eks:us-west-2:536506487112:addon/testy2/coredns/80c70604-2e61-4b46-45e5-58e39fc72b94")
        self.assertEqual(result, "corednsd")

    def test_arn_rdsinstance(self):
        result = lambda_function.parse_arn("arn:aws:rds:us-west-2:536506487112:db:database-1-instance-2")
        self.assertEqual(result, "database-1-instance-2")
    
    def test_arn_rdscluster(self):
        result = lambda_function.parse_arn("arn:aws:rds:us-west-2:536506487112:cluster:database-1")
        self.assertEqual(result, "database-1")

    def test_arn_eni(self):
        result = lambda_function.parse_arn("arn:aws:ec2:us-west-2:536506487112:network-interface/eni-042a010ea81e05538")
        self.assertEqual(result, "eni-042a010ea81e05538")

    def test_arn_fleet(self):
        result = lambda_function.parse_arn("arn:aws:ec2:us-west-2:536506487112:fleet/fleet-869634b7-c68d-6c2d-041a-a300675a4d5f")
        self.assertEqual(result, "fleet-869634b7-c68d-6c2d-041a-a300675a4d5f")

    def test_arn_launchtemplate(self):
        result = lambda_function.parse_arn("arn:aws:ec2:us-west-2:536506487112:launch-template/lt-0bc883ce91e0e4f87")
        self.assertEqual(result, "lt-0bc883ce91e0e4f87")

    def test_arn_labmda(self):
        result = lambda_function.parse_arn("arn:aws:lambda:us-west-2:536506487112:function:AwsAutoTagger")
        self.assertEqual(result, "AwsAutoTagger")

    def test_arn_sg(self):
        result = lambda_function.parse_arn("arn:aws:ec2:us-west-2:536506487112:security-group/sg-0c4414f68b93d8f46")
        self.assertEqual(result, "sg-0c4414f68b93d8f46")

    def test_arn_volume(self):
        result = lambda_function.parse_arn("arn:aws:ec2:us-west-2:536506487112:volume/vol-05f578aef770b61b7")
        self.assertEqual(result, "vol-05f578aef770b61b7")    
        
if __name__ == '__main__':
    unittest.main()