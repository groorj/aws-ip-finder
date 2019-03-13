# aws-ip-finder
Ever needed to find a public IP in your AWS accounts ? It might be "easy" when you have 1 account but what if you have 20, 50, 100+ accounts ?

This script gather Public IP information for AWS services and returns a list of the findings.

### How to install
```
git clone https://github.com/groorj/aws-ip-finder.git
cd aws-ip-finder
pip install -r requirements.txt
```

### Requirements
- Python3
- PyYAML
- Boto3

### Configuration
Edit the file config.yml in order to configure your parameters.

```
profile_name: my-profile-name
assertions:
  regions:
    - sa-east-1
    - us-east-1
    services:
      - ec2
      - natgateway
  output_format: "csv"
```
- **profile_name**: `This is the AWS profile name that you use with your account located at ~/.aws/credentials`
- **regions**: `A list of regions that you want this script to craw and get data for`
- **services**: `A list of services to query for Public IPs`. Current options are: `ec2`, `natgateway`
- **output format**: `This is the format that the output will be presented`. Current options are: `csv`, `json`

### Running
`python3 -tt aws-ip-finder.py config.yml`

### Notes
You can create as many configuration files as you want and provide it as an argument to the aws-ip-finder.py script.
