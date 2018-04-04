# Description
This repo shows how to migrate an existing Flask app to one that can use
OpenShift's
[`s2i`](https://github.com/openshift/source-to-image) tool to create
a Docker image of the app.

`s2i` builds Docker images using a common two-stage build pattern: the
source code is piped to a **builder image**, prepared, and then output
into a final image. It's most interesting feature is that it can do all this
*without a Dockerfile*.

NOTE: If starting off fresh without any existing, it may be better to use the
`s2i create <image name> <destination directory>` command from the
[`s2i` CLI](https://github.com/openshift/source-to-image/blob/master/docs/cli.md)

### Building the Docker image: `s2i build` and `docker run`
Assuming the final image name is `hello-world-flask:v0`:
1. In the terminal, change directories to the repo's `flask-app/` folder
2. Run `s2i build . centos/python-36-centos7 hello-world-flask:v0`
3. Run `docker run -p 8888:8080 hello-world-flask:v0`

### Migration Steps
The only required adjustments to the original Flask repo are:
- Moving the Flask app's files into a folder ending in "-app"
- Adding an `.s2i/environment` specifying the app start script
  e.g. the file used to run the app with the command `python <file>`
  - NOTE: if `app.py` is the start script, then no need to add the
    `.s2i/environment` file

# Details

### Builder image + Python version
This Flask app uses the
[`centos/python-36-centos7`](https://hub.docker.com/r/centos/python-36-centos7/)
image as the builder image.

### Flask app file structure
If the original repo looks like this
```
flask-repo
|-- run.py
|-- sampleapp/
    |-- __init__.py
    |-- views.py
```
then the new repo would look like this
```
flask-repo
|-- flask-app               # new contents folder
    |-- run.py
    |-- sampleapp/
        |-- __init__.py
        |-- views.py
    |-- .s2i                # new folder
        |-- environment     # new file
```

# Other notes

### OpenShift
**This repo cannot be directly** deployed as a git repo to OpenShift 3; see
an example
**[HERE](https://github.com/geordgez/flask-openshift-upload-ex)** instead.
This is
because the `.s2i/` folder and app files need to be directly in the repo
folder rather than in any of the repo's child folders. To see the Flask app
adapted for directly deploying a git repo to OpenShift and letting the
OpenShift instance automatically build via `s2i`, again see
[the sister repo mentioned above](https://github.com/geordgez/flask-openshift-upload-ex).

The sister repo can be directly deployed on OpenShift Online / OpenShift
Container Platform via `Add to project > Browse Catalog > Python > 3.5` and
pasting a fork of the git repository. *NOTE: the current app succesfully
runs on both 3.5 (as of 04-03-2018, 3.5 is the current latest version
on OpenShift's online base images) and 3.6 (available via CentOS's
Docker Hub).*
