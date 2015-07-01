# IPOP-server
Server UI for IPOP

###External Dependencies:
- pycrypto
- sleekxmpp

###Functionality:
- create a new gvpn
- establish secure connection with client
- send encrypted config files

###Installation instructions:
Install all the required packages with the following command

```
sudo apt-get install python-pip
sudo pip install sleekxmpp
```

Download and extract web2py from here: [web2py Web Framework](http://www.web2py.com/init/default/download)

```
cd web2py
python web2py
```

Enter some admin password when asked.

Open [localhost:8000](http://localhost:8000) and goto `My Sites` tab.

Download [web2py.app.IPOP.w2p](http://www.fileconvoy.com/dfl.php?id=g80c4c172b0cc730899968591481edfb31577a778b) which is a packaged version of this server.

open this file in web2py interface under the section `Upload and install packed application` in `My Sites` tab.

once done click on the server and you are done!


