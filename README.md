# api_server
Local Development Environment for C# API server</br>
This was my second attempt at using C# as part of an educational side project coming from a very Python centric development background.</br>
Many thanks to https://github.com/MattWood21 for providing feedback and help when required!</br>

## Roadmap
For future updates on this side project please see https://github.com/kmoorfield/Obsidian_Notes </br>

## Disclaimer
Feel free for anyone to copy / use this in any way as part of educational learning only!</br>

## Getting Started
### Run the code
You can start the application by cloning the repo and executing the rebuild_containers.sh script in Git Bash.</br>

## Web API
The web api Swagger examiner is available, when running, at http://localhost:5000/swagger/index.html

## Load testing
Load testing via Locust is available, when running, at http://localhost:8089/

## Locust Load Testing Configuration
### Main and Worker Configuration
In this configuration the load testing code is in the locust folder.</br>

There are two Dockerfile's in use:

- Dockerfile_Main
	This Dockerfile builds an image to act as the main locust container that will be used to access the web app at http://localhost:8089 when running. It also coordinates the workers.</br>
	The entrypoint by default runs with an UI however locust can be set to run automatically without an UI by adding the following commands onto the entrypoint ["--run-time", "5m", "--headless"].</br>
	The output is then logged within the docker container logs instead of within the UI.</br>
- Dockerfile_Worker
	This Dockerfile builds an image to act as the worker. It is pointed to the main image via the argument --master-host, whose value must match the hostname in application_stack.yaml for the load_main container.</br>
	
## Scaling Workers
You can pick the number of workers by defining the "--scale load_worker=X" value in the rebuild_containers.sh and then re-executing the script again to relaunch the stack.</br>

## Test Definitions
The tests are defined in the locust/tests folder and its sub-folders.</br>