# How to run projects

## First of all clone all the projects.

# links:

https://github.com/erfanmorsali/micro-gateway
https://github.com/erfanmorsali/micro-users
https://github.com/erfanmorsali/micro-addresses

## create networks and volumes :

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

## first run gateway,then run micro-users and finally micro-addresses

## you can find swagger documents in :

localhost:8000/docs


