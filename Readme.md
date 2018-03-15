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
