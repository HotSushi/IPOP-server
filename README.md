# IPOP-server
Server UI for IPOP

###External Dependencies:
- pycrypto
- sleekxmpp

###Installation instructions:

#### Install Dependencies
Install all the required packages with the following commands
```
sudo apt-get install python-pip
sudo pip install sleekxmpp
sudo pip install pycrypto
```

#### Install Web2py
Download and extract web2py from here: [web2py Web Framework](http://www.web2py.com/init/default/download)
```
cd web2py
python web2py
```
Enter some admin password when asked.

#### Place IPOP-server code
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

#### Done
Open [IPOP](http://localhost:8000/IPOP)

Default login credentials are
```
Name : user
Password : password
```
