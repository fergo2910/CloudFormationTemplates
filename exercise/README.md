## HOW TO RUN
With admin privilege run de following command to docker compose the django enviroment.
```
$ git clone https://github.com/fergo2910/exercise.git
$ cd exercise
$ docker-compose up [-d]
```
And then enter to the landpage `localhost/exercise_redis/home`
If you want to connect into the database, you can run the following command to the redis container
```
docker exec -it <container> redis-cli [-h <hostname>]
```

# CONFIGURATION
For redis persistence storage change the volumne directory to your folder to store the data at the docker-compose.yml file.
```
volumes:
- //c/Users/fjgonzalez/Music/data:/data
```
For Node.js app to recognize redis, Node.js calls redis with the hostname in the  `code_node_api/node_modules/redis/index.js` where is define the port and the host (line 70).

### RUNNING THE APP
Once the environment is working, the following url should be executed: `localhost/exercise_redis/home`.
In the `localhost/exercise_redis/elements` you can add products and search products.

### CLEANING UP
When you want to try new changes into code, you need stop docker-compose with `Ctrl + C` and remove the images that were created with the docker-compose.
Also you can run the commands.
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker images
docker rmi exercise_web_app_01
docker rmi exercise_web_app_02
```
So you can start from scratch.

# ARCHITECTURE
The architecture of this exercise is the following:
![ARCHITECTURE](exercise.png?raw=true "ARCHITECTURE")

Two networks were created to be used within the solution
- back-tier
  Internal network communicating the api of Node.js and Redis
- front-tier
  Internal network communicating the web app, consul and Node.js

It was developed in this way to define the difference between Frontend and Backend (as a concept).  

<details>
  <summary>Redis</summary>
  <p>Images: redis:latest</p>
  <p>Using its default configuration and storing information persistently outside the container.</p>
  <p>Hostname within back-tier network: 'redis'</p>
  <p>Visible port for tests: 6379</p>
</details>

<details>
  <summary>Node api</summary>
  <p>Image: node:latest</p>
  <p>Generator of api as REST server and storage in Redis, self registration of services to consul when the container starts.</p>
  <p>Hostname within back-tier network: 'node_api'</p>
  <p>Visible port for test: 7000</p>
</details>

<details>
  <summary>Consul</summary>
  <p>Image: consul:latest</p>
  <p>Service check and service provider for web app and api communication. Shows and provides the web app with the available node to consume the 'service_api' service self-registered by node_api</p>
  <p>Hostname within front-tier network: 'consul'</p>
  <p>Visible port for test: 8500</p>
</details>

<details>
  <summary>Web app</summary>
  <p>Image: exercise_web_app_0#</p>
  <p>Web application nodes in django framework. Entry, request and sample of information stored in redis. Consume consul service to obtain node, node give the connection of the REST server and then retrive the result. Image generated with Dockerfile when executing the `docker-compose up` command</p>
  <p>Hostname within front-tier network: 'web_app_01' and 'web_app_02'</p>
  <p>Visible port for test: 8000 and 9000</p>
  <p>URL for exercise: localhost:[port]/exercise_redis/home</p>
</details>

<details>
  <summary>Load balancer</summary>
  <p>Image: dockercloud/haproxy:latest</p>
  <p>Load balancer using haproxy, round robin with docker links to web app.</p>
  <p>Hostname within front-tier network: 'lb'</p>
  <p>Visible port for test: 80</p>
  <p>URL for exercise: localhost/exercise_redis/home</p>
</details>

# DEPLOY WITH CFN
If you want the same enviroment in cloud you could run a CFN service with the following steps.
1. Go to your aws console and EC2 service.
2. Generate a` Key-pair` to connect to an EC2 Instance.
3. This will save a `key.pem` file with a rsa key. Save this key into your root project.
4. change the privileges of the `key.pem` with the command `chmod 400 key.pem` so the key wont be modifiable, only readable.
5. Now, you need to create a user in your aws account.
   1. Go to your console
   2. Go to IAM service
   3. Users, and create a user and save the public and secrete keys of the user.
6.  Set up a profile for aws-cli with the command `aws configure --profile exercise`
   1. Enter the public key of the created user
   2. Enter the private key of the created user
   3. Choose your region
   4. You can leave the default format in blank
7.  Now with aws configured run, the following command to create the CloudFormation stack in AWS.
```
aws cloudformation create-stack --stack-name exercise_stack --template-body file://$PWD/aws-stack.yml --profile exercise --region us-west-2
```
8.  When the stack is **CREATE_COMPLETE** you need to go to Resources and click in the Physical ID of the EC2_Deploy and copy the public IP of the instance.
9.  You have to configure a volumne for redis in the aws-docker-compose.yml using:
10. Finally, you can run docker-compose -H tcp://public_ip:2375 up -f aws-docker-compose.yml
11. When everything is up you can access through your browser to the public ip and it will show you the same page that you build with docker compose localy.
