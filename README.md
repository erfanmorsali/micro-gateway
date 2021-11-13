# How to run projects

## 1 _clone all the projects.

# links:

https://github.com/erfanmorsali/micro-gateway
https://github.com/erfanmorsali/micro-users
https://github.com/erfanmorsali/micro-addresses

## 2 _prepare projects to run
### run this command in java projects root directories:
``
mvn clean package -DskipTests
``
##this command must generate a directory named target for you.


##3 _create networks and volumes :

``
docker network create rabbit-network
``

``
docker network create api-network
``

``
docker network create users-db-network
``

``
docker network create address-db-network
``

``
docker volume create micro-users-volume
``

``
docker volume create micro-address-volume
``

## And simply just run this command in project roots:

``
docker-compose up -d --build
``

## Its better to  first run gateway, then run micro-users and finally micro-addresses.

## You can find swagger documents in :

localhost:8000/docs


