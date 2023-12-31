from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/hi')
def xxx():
    abc="""
#version=RHEL8
ignoredisk --only-use=sda
autopart --type=lvm
# Partition clearing information
#clearpart --none --initlabel
zerombr
clearpart --all --initlabel
# Use graphical install
#graphical
text
# Use CDROM installation media
cdrom
# Keyboard layouts
keyboard --vckeymap=us --xlayouts='us'
# System language
lang en_US.UTF-8

# Network information
network  --bootproto=static --device=ens32 --gateway=10.1.1.1 --ip=10.1.23.101 --nameserver=8.8.8.8 --netmask=255.255.0.0 --ipv6=auto --activate
network  --hostname=mytest.local
# Root password
rootpw --iscrypted $6$jMMs4Nv.1BA8D74c$jHOC.koxhNO1VAIMbwm/QAd/iNSKwxKeetFgBDzPd42p2bcRknqD8O/0awUmnmBN2PMxyu3.eGF9WLsn3oSTx0
# Run the Setup Agent on first boot
firstboot --enable
# Do not configure the X Window System
skipx
# System services
services --enabled="chronyd"
# System timezone
timezone Asia/Hong_Kong --isUtc
reboot

%packages
@^minimal-environment
kexec-tools
curl
vim
git
telnet

%end

%addon com_redhat_kdump --enable --reserve-mb='auto'

%end

%anaconda
pwpolicy root --minlen=6 --minquality=1 --notstrict --nochanges --notempty
pwpolicy user --minlen=6 --minquality=1 --notstrict --nochanges --emptyok
pwpolicy luks --minlen=6 --minquality=1 --notstrict --nochanges --notempty
%end
    """
    return abc
