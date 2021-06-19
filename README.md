# Django Rest Full Api


## Technologies used in this project:
  - python
  - django
  - django rest framework
  - web scraping 
  - rabbitmq 
  - redis
  - celery 
  - celery beat
  - docker 
  - nginx
  - postgres
  
   ------------------------------------
   
## Installation:
   ### Prerequisites
   - docker
      for download docker in [link](https://docs.docker.com/engine/install/)

   - docker-compose
      for download docker in [link](https://docs.docker.com/compose/install/)

   - STOP redis server in local
   - STOP rabbitmq server in local
  
   ### create volume

    docker volume create postgres_data
    
    docker volume create static_file
    
    docker volume create media_file
   
   ### create network
   
    docker network create main
    
    docker network create nginx_network
   
   ### run service 
 
    docker-compose up -d
    
   ### cd **nginx/**

    docker-compose up -d
