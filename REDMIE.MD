exam_ict

## swagger-ui doc
- api.dxcode.ir/api/schema/swagger-ui

## requirements
- python:3.11 higher
- django 5.2 higher

## install
- pip install -r requirements/development.txt (for development)
- pip install -r requirements/production.txt (for production)

## build on vps
- cd folder base image
- gunzip ict_1.0.0.tar.gz
- docker load -i ict_1.0.0.tar
- docker-compose up --build

# relation schema
![ict_exam.drawio.png](ict_exam.drawio.png)