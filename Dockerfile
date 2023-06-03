version: '3.7'
services:
  web:
    build:
      context: ./web
      dockerfile: Dockerfile
    ports:
      - "80:80"
    environment:
      - MYSQL_ROOT_PASSWORD=password
    volumes:
      - ./web:/var/www/html
      - /var/run/docker.sock:/var/run/docker.sock
		security_opt:
      - seccomp:unconfined
  db:
    image: mysql:5.7
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=db
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    volumes:
      - db_data:/var/lib/mysql
		network_mode: host
  compute_script:
    image: python:3.9-alpine
    volumes:
      - ./script.py:/app/script.py
    command: ["python", "/app/script.py"]

volumes:
  db_data:
