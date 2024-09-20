#!/bin/bash
#ssh-keygen -t rsa -q -N '' -f /etc/ssh/ssh_host_key
ssh-keygen -t rsa -q -N '' -f /etc/ssh/ssh_host_rsa_key
ssh-keygen -t dsa -q -N '' -f /etc/ssh/ssh_host_dsa_key
/usr/sbin/sshd -D