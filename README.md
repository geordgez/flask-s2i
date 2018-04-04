# Description
This repo shows how to migrate an existing Flask app to one that can be built
into a Docker image using
[`s2i`](https://github.com/openshift/source-to-image).

`s2i` builds Docker images using a common two-stage build pattern: the
source code is piped to a **builder image**, prepared, and then output
into a final image. It's most interesting feature is that it can do all this
*without a Dockerifle*.

NOTE: If starting off fresh without any existing, it may be better to use the
`s2i create <image name> <destination directory>` command from the
[`s2i CLI`](https://github.com/openshift/source-to-image/blob/master/docs/cli.md)

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
