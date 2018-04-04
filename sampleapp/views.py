from sampleapp import myapp

@myapp.route('/')
def helloworld():
    return 'Hello World!'
