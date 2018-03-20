#  Generalized Templates

## Parameters:

### General
-   CertificateARN
    - If you want to set a HTTPS protocol, you can add this Certificate and change the `elb` and the `master` template.
-   StackEnv
    - Environment name you are going to deploy (if needed)
        - *qa*
        - *prod*
- ImageTag
    - With this parameter we will look for the image in the task definition

### Cluster configuration
- InstanceType
    - Instance type ECS cluster w    ill build on.
- MinSize    
    - Minimum number of EC
- DesiredSize
    - Number of instance EC2 on the auto scaling group and can't be less than min size
- MinSize
    - Minimum number of EC2 instances on the auto scaling group
- MaxSize
    - Maximum number of EC2 instance on the auto scaling group
- KeyPair
    - Key for EC2 instances.

### Database configuration
- DBMasterUsername
    - Name of the master user in the new database that will be created
- DBMasterUserPassword
    - Password of the master user in the database
- DBInstanceClass
    - Type of the compute an capacity classes of the database, usually _db.t2.micro_
- DBEngine
    - Database engine that the database instance will use
        - MySQL (*default*)
        - Postgress
- DBName
    - Name of the database instance provided at the time of the creation
- DBInstanceIdentifier
    - Name of the database
- DBAllocatedStorage
    - Allocated storage size for the data base instance in GB
        - Default: 100Gb

### Cache configuration
- CacheNodeType
    - The compute and memory capacity of nodes in the cache cluster
- CacheEngine
    - The engine of the elastic cache instance
- CacheClusterName
    - Name for the cluster cache
- CacheNumCacheNodes
    - Size of the cache nodes in the cluster.

# Generalized Stacks

1. [VPC Template](https://s3.amazonaws.com/ferdinand-bucket/infrastructure/vpc.yaml)
    - This template creates a VPC with four subnets:
        - 2 public and 2 private.
2. [Security Group Template](https://s3.amazonaws.com/ferdinand-bucket/infrastructure/vpc-sg.yaml)
    - Creates two Security groups, one accepts public network traffic and the other accepts only the public security group traffic
3. [Elastic LoadBalancer V2 Template](https://s3.amazonaws.com/ferdinand-bucket/infrastructure/elb.yaml)
    - This template creates and Elastic Load Balancing Applicaion with a listener and a default target group to set up later
4. [ECS Cluster Template](https://s3.amazonaws.com/ferdinand-bucket/infrastructure/ecs.yaml)
    - This template creates:
        - ECS Cluster
        - Auto Scaling group
        - Sacle Up policy
        - Scale Down policy
        - CloudWatch Memory Alarm Up/Down
        - CloudWatch CPU Alarm Up/Down
        - Launch Configuration
        - Role for ECS
        - Instance profile
5. [RDS instance  Template](https://s3.amazonaws.com/ferdinand-bucket/infrastructure/databases/rds.yaml)
    - This template creates a subnet group and a database instance.
6. [Elastic Cache Cluster Template](https://s3.amazonaws.com/ferdinand-bucket/generalized_templates/ec-redis.yaml)
    - This template creates a subnet group and a cluster of cache.
7. [Client Service Template](https://s3.amazonaws.com/ferdinand-bucket/generalized_templates/client.yaml)
    - This templates creates :
        - Auto scaling for the ECS service
        - Scaling policy for the ECS service
        - CloudWatch Alarm of HTTP errors 500
        - ECS Service
        - Task Definition using a ECR images
        - CloudWatch Log group
        - Target group
        - Rule for the listener in the ELB V2
        - Role for service instance
        - Role for auto scaling
