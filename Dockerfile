FROM ubuntu:latest

RUN apt update && apt install  openssh-server -y

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN echo 'root:password' | chpasswd

RUN service ssh restart

RUN service ssh start
CMD ["/usr/sbin/sshd","-D"] 
