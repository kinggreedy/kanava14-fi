
# Welcome to Kanava14.fi  
This project kicks start the revolution for social platform 4.0      
or so....  
  
# Architecture story  
  
Although the test only requires us to develop a platform, I would like to put the context of starting a brand new website, from a new IT company, for a new client that does not have a website before, while providing a small CD/CI solution.  
This approach cause a small problem with the architecture and repository management, because this repository actually host 3 components at once (which should have their own repo): application, devbox, deployment scripts. This approach also requires me to not over engineering while keeping everything clean and robust.   
  
There are some assumption to be made:  
- Production server is a virtual private server (not having Kubernetes capability), like using DigitalOcean, Upcloud, Linode, or any VPS similar providers  
- The production server is newly installed and is dedicated to only this project  
- For shared environment, system administrator can use the scripts in scripts/deploy and the description below as assistance  
  - 2-*-.sh scripts: Dependencies installation commands  
  - 3-*-.sh scripts: Project setup commands  
  - 4-*-.sh scripts: Project deploy commands  
  
## Instruction on starting the project  
  
### 1. Development - Devbox/Vagrant  
  
- `cd scripts/vagrant`  
- Modify Vagrantfile  
  - Remove the addon-script that you don't want to install.  
      You can also run them manually later  
  - In case you are installing unison,  
      Please change the vagrant password to be more secured  
  - Modify the port and shared folder (check config table below at section 6)  
- `vagrant up`  
- You can now develop the app and access to the ports you configured  
- If you have installed unison, you can use example code `sync-app.ps1` and `sync-project.ps1`  
  to make unison sync with your vagrant project between Windows and Linux environment  
  
### 2. Development - Only the app  
  
- Copy blog-platform into the destination folder  
- Follow setup commands in scripts/deploy/3-1-setup-deployment.sh to  
  setup virtual environment and project folder  
- `cp -r app/blog-platform /opt/kanava14fi/`  
  (you can change the directory if you see fit)  
- Follow setup commands in scripts/devbox/3-0-2-setup-devbox-postdeploy.sh to  
  install the tools for the development such as flask8 and pytest  
- Config development.ini  
- `pserve development.ini --reload`  
- run `./scripts/linting.sh` for linting and `./scripts/testing.sh` for testing
- If you want to use nginx in development, follow `scripts/devbox/2-0-4-setup-nginx.sh`

### 3. Production - Using github action as build server to deploy  
  
- Add secrets to the github secret configuration  
- To make a new release, make a new commit in /release branch  
  
### 4. Production - Using devbox as build server  
  
Dependencies:
- Make sure 2-0-3-setup-acl.sh scripts ran successfully  
- Having at least 20GB HDD space  
- Warning, this option will also require 16GB download   
  
Run:  
- sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 -j <event>  
  
Example:  
- sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 -j build  
- sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 -j pull_request  
- sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 -j deploy  
  
#TODO: secret  
  
### 5. Production - Manually deploy  
  
- Follow scripts/deploy/2-* to install python, postgres and nginx  
- Follow scripts/deploy/3-1-setup-deployment.sh to install the project  
- Upload the directory `app/blog-development` to correct location on server  
- Config production.ini as you see fit  
- Follow scripts/deploy/3-2-setup-postdeployment.sh to finish installing and  
  config the project  
- Follow scripts/deploy/4-1-run-predeploy.sh and 4-2-run-postdeploy.sh each time  
  you deploy a new change  
  
### 6. Customization  
  
#TODO  
  
|                |ASCII                          |HTML                         |  
|----------------|-------------------------------|-----------------------------|  
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |  
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |  
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|  
  
# Roadmap (or - what should I do if I can spent more time)  
  
- More testing, at least 80% test coverage  
- More unit test  
- RestAPI with swagger  
- Docker, to enable the project can be deployed to kubernetes cluster more efficient  
- Load balancing with multiple server and database nodes
