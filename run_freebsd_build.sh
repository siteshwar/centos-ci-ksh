set -ex

yum -y install gcc dkms make libgomp
yum -y install kernel-headers kernel-devel glibc-headers glibc-devel
curl -o /etc/yum.repos.d/virtualbox.repo http://download.virtualbox.org/virtualbox/rpm/rhel/virtualbox.repo
yum install -y VirtualBox-5.2
/sbin/rcvboxdrv setup
yum -y install https://releases.hashicorp.com/vagrant/2.1.5/vagrant_2.1.5_x86_64.rpm

state="pending"
description="Build is running"
curl -s --user $GITHUB_USER:$GITHUB_API_KEY -X POST --data "{\"state\": \"$state\", \"description\": \"$description\", \"context\": \"FreeBSD\" }" "$statuses_url"

set -o pipefail
ix_url=$(vagrant up | curl -F 'f:1=<-' ix.io)

if [[ $? -eq 0 ]]; then
    state="success"
    description="Build passed"
else
    state="failure"
    description="Build failed"
fi

curl -s --user $GITHUB_USER:$GITHUB_API_KEY -X POST --data "{\"state\": \"$state\", \"description\": \"$description\", \"context\": \"FreeBSD\", \"target_url\": \"$ix_url\" }" "$statuses_url"

echo $ix_url

vagrant destroy -f
