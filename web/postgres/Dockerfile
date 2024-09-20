FROM postgres:15

RUN useradd -m -s /bin/bash user_bd
RUN echo 'user_bd:user_bd' | chpasswd
RUN apt-get update && apt-get install -y openssh-server