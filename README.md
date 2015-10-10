# IPOP-server
Server UI for IPOP

## Installation instructions:

### Install Dependencies
Install all the required packages with the following commands
```
sudo apt-get install python-pip
sudo pip install sleekxmpp
sudo pip install pycrypto
```

### Install Web2py
Download and extract web2py from here: [web2py Web Framework](http://www.web2py.com/init/default/download)
```
cd web2py
python web2py
```
Enter some admin password when asked.

### Place IPOP-server code
Open [localhost:8000](http://localhost:8000) and goto `My Sites` tab.

Create a new application with the name `IPOP`

then do the following
```
cd /dir/to/web2py/applications
git clone https://github.com/HotSushi/IPOP-server.git
rm -rf IPOP
mv IPOP-server IPOP
```
This step basically replaces the contents of the dir `/IPOP` with the contents of this repo.

### Done
Open [IPOP](http://localhost:8000/IPOP)

Default login credentials are
```
Name : user
Password : password
```

## Other Installations
### IPOP-ejabberd
IPOP-server can interact with ejabberd server through [IPOP-ejabberd](https://github.com/HotSushi/IPOP-ejabberd), for registering nodes (directly through web interface) and fetching logs. Please follow the instructions for setting up IPOP-ejabberd and avail the functionality of `batchgvpn`.

### Ganglia Integration
IPOP-server can be integrated with Ganglia for viewing monitoring info directly through IPOP-server web interface. Ganglia needs to be installed for both server and client. Client installation instructions can be found [here](https://github.com/HotSushi/IPOP-client/tree/master/ganglia_setup). Refer [this](https://www.digitalocean.com/community/tutorials/introduction-to-ganglia-on-ubuntu-14-04#installation) blog for Server installation (only the server part!)(keep cluster name as `my cluster`). For more information see [here](https://github.com/ipop-project/documentation/wiki/Integrating-Ganglia-monitoring-with-IPOP). 