#!/usr/bin/env python

from __future__ import print_function
import sys
import yaml
import pprint

class IpFinder:

    def __init__(self, config):
        self.config = config

    def get_ec2_info(self, ec2):
        instances = ec2.describe_instances(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['running', 'stopped', 'stopping'],
            }]
        )
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                finder_info.append(
                    { 'service': "ec2", 'public_ip': instance["PublicIpAddress"], 'resource_id': instance["InstanceId"] }
                )

    def get_natgateway_info(self, ec2):
        instances = ec2.describe_nat_gateways(
            Filters=[{
                'Name': 'state',
                'Values': ['available', 'pending'],
            }]
        )
        for reservation in instances["NatGateways"]:
            for instance in reservation["NatGatewayAddresses"]:
                finder_info.append(
                    { 'service': "natgateway", 'public_ip': instance["PublicIp"], 'resource_id': reservation["NatGatewayId"] }
                )

def _get_config_from_file(filename):
    config = {}
    with open(filename, "r") as stream:
        config = yaml.load(stream)
    return config

def get_boto_session(profile_name, aws_region):
    import boto3
    return boto3.Session(profile_name=profile_name, region_name=aws_region)

def is_service_enabled(service_name):
    if service_name in aws_services_list:
        return True
    return False

# main
if __name__ == "__main__":
    finder_info = []
    default_aws_region = "us-east-1"
    config = _get_config_from_file(sys.argv[1])
    ipfinder = IpFinder(config)
    # print("Current configuration:\n", yaml.dump(config, default_flow_style=False))
    aws_regions_list = config.get("assertions").get("regions", [])
    aws_services_list = config.get("assertions").get("services", [])
    boto_session = get_boto_session(config["profile_name"], default_aws_region)

    # execute for each AWS region
    for aws_region in aws_regions_list:
        # print("== Working region: " + aws_region)
        boto_session = get_boto_session(config["profile_name"], aws_region)
        # EC2
        if is_service_enabled("ec2"):
            ec2 = boto_session.client("ec2", region_name=aws_region)
            ipfinder.get_ec2_info(ec2)
        # NAT Gateway
        if is_service_enabled("natgateway"):
            ec2 = boto_session.client("ec2", region_name=aws_region)
            ipfinder.get_natgateway_info(ec2)
    for x in finder_info:
        print(x)

# End;
