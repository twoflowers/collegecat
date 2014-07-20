# -*- mode: ruby -*-
# vi: set ft=ruby :

$bash_provision = <<EOF
echo "BLAARG!"
yum -y install http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-11.ius.centos6.noarch.rpm http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/epel-release-6-5.noarch.rpm
yum -y install mysql-server python27 python27-pip python27-tools python27-devel vim-enhanced mysql-devel
pip2.7 install -r /var/www/collegecat/requirements.txt
chkconfig mysqld on
service mysqld start
mysql -uroot -e 'GRANT ALL PRIVILEGES ON *.* TO "collegecat"@"localhost" IDENTIFIED BY "UrNotAG04t"; FLUSH PRIVILEGES';
mysql -uroot -e 'CREATE DATABASE collegecat;'
echo "Populating random data"
cd /var/www/collegecat/app/
/usr/bin/python2.7 /var/www/collegecat/app/generate_data.py | tail
#rm -fv /etc/nginx/conf.d/default.conf
#cp -v /var/www/collegecat/nginx.conf /etc/nginx/conf.d/collegecat.conf
#mkdir -pv /var/log/uwsgi/ /etc/supervisord.d
#cp -v /var/www/collegecat/etc_supervisord.conf /etc/supervisord.conf
#cp -v /var/www/collegecat/supervisord.conf /etc/supervisord.d/collegecat.conf
cp -fv /var/www/collegecat/upstart.conf /etc/init/collegecat.conf
service iptables stop;chkconfig iptables off
start collegecat
EOF

Vagrant.configure("2") do |config|
    config.vm.box_url = ""
    config.vm.define :cat do |cat|
        cat.vm.box = "centos-64-x64"
        cat.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-x86_64-v20131103.box"
        cat.vm.network :private_network, ip: "192.168.200.18"
        cat.vm.hostname = "dev.college.cat"
        cat.vm.synced_folder ".", "/var/www/collegecat"
        config.vm.network "forwarded_port", guest: 80, host: 8080
        cat.vm.provision :shell, inline: $bash_provision
    end
end
