## Murmur-rest API v1

### Overview

Murmur-REST is a RESTful web application wrapper over the Murmur SLICE API to administer virtual Mumble servers. The API allows you to develop your own application using the feature set and endpoints provided. This project was built to administer Mumble servers for [Guildbit.com](http://guildbit.com).

Murmur-REST is still in early development. If you find any issues or would like to help contribute to the project, please report them via Github issues or send a pull request.

**Check out my Mumble-Widget project! https://github.com/alfg/mumble-widget**

### Endpoints

#### Servers

| Endpoint | Description |
| ---- | --------------- |
| GET /servers/ | Get server list |
| POST /servers/ | Create a new server, starts it, and returns details |
| GET /servers/:serverid | Get server details |
| POST /servers/:serverid/start | Start server |
| POST /servers/:serverid/stop | Stop server |
| DELETE /servers/:serverid | Delete server |
| DELETE /servers/delete?id=1,2,3 | Delete multiple servers |
| GET /servers/:serverid/logs | Get server logs |
| GET /servers/:serverid/bans | Get list of banned users |
| GET /servers/:serverid/conf | Get server configuration for specified id |
| POST /servers/:serverid/conf?key=users&value=100 | Set configuration variable 'users' to 100 |
| POST /servers/:serverid/sendmessage | Send a message to all channels in a server. formdata: message |
| POST /servers/:serverid/setsuperuserpw | Sets SuperUser password. formdata: password |

#### Stats

| Endpoint | Description |
| ---- | --------------- |
| GET /stats/ | Get all statistics |

#### Users

| Endpoint | Description |
| ---- | --------------- |
| GET /servers/:serverid/user | Get all users in a server |
| GET /servers/:serverid/user/:userid | Get User |
| POST /servers/:serverid/user | Create User, formdata:  username&password |
| DELETE /servers/:serverid/user/:userid | Delete User |
| POST /servers/:serverid/kickuser?usersession=1 | Kick user with session #1 |
| POST /servers/:serverid/user/:userid/mute | Mute User |
| POST /servers/:serverid/user/:userid/unmute | Unmute User |
| POST /servers/:serverid/user/:userid/update | Update registered username. formdata: username

#### Channels

| Endpoint | Description |
| ---- | --------------- |
| GET /servers/:serverid/channels | Get all channels in a server |
| GET /servers/:serverid/channels/:channelid | Get a channel from a server by ID |
| POST /servers/:serverid/channels | Create Channel, formdata:  name&parent |
| GET /servers/:serverid/channels/:channelid/acl | Get ACL list for channel ID |
| DELETE /servers/:serverid/channels/:channelid | Delete Channel |


### Development Setup

Assuming you already have Murmur running and set up, follow the instructions below to run murmur-rest
for development. Tested on Ubuntu 13.10, but should be to run wherever Murmur and Zero Ice are supported.

Runserver.py uses Flask's development server. This should be used for development only. See
Deployment for Production for running in production mode. Python virtualenv is highly recommended as well.

1) Install required Zero Ice library

`sudo apt-get install python-zeroc-ice`

2) Clone and install murmur-rest

```
git clone git@github.com:alfg/murmur-rest.git
cd /directory/to/murmur-rest
pip install -r requirements.txt
```

*Note*: If running in virtualenv, use the `--system-site-packages` flag in order to import the Ice library.

3) Run and test application

```
$ cp settings.py.example settings.py
$ python runserver.py
 * Running on http://0.0.0.0:5000/
 * Restarting with reloader

$ curl http://127.0.0.1:5000/servers/
[
    {
        "address": ":::64739",
        "channels": 1,
        "humanize_uptime": "0:00:02",
        "id": 2,
        "log_length": 35,
        "maxusers": "10",
        "name": "",
        "running": true,
        "uptime": 2,
        "users": 0
    }
]
```


### Docker Setup

A Dockerfile is provided to easily setup a local development setup. Install [Docker](https://docs.docker.com/engine/installation/) and run the following commands:

* Pull docker image and run:
```
docker pull alfg/murmur-rest
docker run -it -p 5000:5000 --rm murmur-rest
```

or

* Build and run container from source:
```
git clone https://github.com/alfg/murmur-rest
docker build -t murmur-rest .
docker run -it -p 5000:5000 --rm murmur-rest
```

* Load `http://{VM IP}:5000/servers/` into the browser to test.
If you're unsure what your Docker VM's host is, just run `docker-machine ls` to check.



###  Deployment for Production

Following the same steps for Deployment for Development, just use a Python WSGI application server
such as [Gunicorn](http://gunicorn.org/) instead of the built-in Flask server. The provided `wsgi.py`
file is provided for this.

For example, if using Gunicorn and virtualenv:

```
/path/to/murmur-rest/env/bin/gunicorn -b 127.0.0.1:5000 wsgi:app
```

### TODO

- Complete support for full Murmur SLICE API
- API Documentation
- Error Handling
- Tests

### Resources
- [Murmur SLICE API](http://mumble.sourceforge.net/slice/Murmur.html)

### License

The MIT License (MIT)

Copyright (c) 2016 github.com/alfg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
