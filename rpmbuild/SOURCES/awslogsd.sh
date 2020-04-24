#!/bin/sh
# Version: 1.1.2-rpm
echo -n $$ > /var/run/awslogs.pid
exec 5</var/run/awslogs.pid
[ -f /etc/awslogs/proxy.conf ] && . /etc/awslogs/proxy.conf
exec /usr/bin/env -i HTTPS_PROXY=$HTTPS_PROXY HTTP_PROXY=$HTTP_PROXY NO_PROXY=$NO_PROXY AWS_CONFIG_FILE=/etc/awslogs/awscli.conf HOME=/root /bin/nice -n 4 /usr/bin/aws logs push --config-file /etc/awslogs/awslogs.conf --additional-configs-dir /etc/awslogs/config >> /var/log/awslogs.log 2>&1
