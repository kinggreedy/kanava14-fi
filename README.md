
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

Branching model

- Trunk based
- Production deploy will use latest commit from branch releases/x.x

## Instruction on starting the project  
  
### 1. Development - Devbox/Vagrant  

#### Quick start
- `cd scripts/vagrant`
- `vagrant up`
- Start development from app/blog-platform
- Visit http://localhost:8080

#### Customization
- Modify Vagrantfile  
  - Remove the addon-script that you don't want to install.  
      You can also run them manually later  
  - In case you are installing unison,  
      Please change the vagrant password to be more secured  
  - Modify the port and shared folder (check config table below at section 6)  
- You can now develop the app and access to the ports you configured  
- If you have installed unison, you can use example code `sync-app.ps1` and `sync-project.ps1`  
  to make unison sync with your vagrant project between Windows and Linux environment  

### 2. Development - Docker

Requires docker-compose

- `cd scripts/docker`
- Customize .env file
- `sudo docker-compose build`
- `sudo docker-compose up -d`
- Start development from app/blog-platform
- Visit http://localhost:8080

Note: Act tool (https://github.com/nektos/act) won't be available inside this docker development 

### 3. Development - Only the app  

#### Requisites
Assuming that you have already installed required environments
 - Python 3.7
 - Postgres 11
You can follow the scripts in scripts/deploy/2-* to setup them

#### Deploy
- Follow setup commands in scripts/deploy/3-1-setup-deployment.sh to  
  setup virtual environment and project folder
    - ```
      cd ..  
      virtualenv venv
      virtualenv -p /usr/bin/python3.7 venv
      source venv/bin/activate
      cd -
      pip install --upgrade pip setuptools
      ```
- Copy blog-platform into the destination folder  
- Follow setup commands in scripts/devbox/3-0-2-setup-devbox-postdeploy.sh to  
  install the tools for the development such as flask8 and pytest  
  - ```
    pip install .
    pip install -e ".[develop]"
    ```
    `cp development.ini.sample development.ini` and Config development.ini
    ```
    alembic -c development.ini upgrade head
    initialize_blog_platform_db development.ini
    ```
- `pserve development.ini --reload` or `./scripts/devbox/start-pserve.sh`  
- For linting, run `./scripts/linting.sh`  
  For testing, run `./scripts/testing.sh`

### 4. Production - Using github action as build server to deploy  
  
- Edit password & ssh key and run `scripts/deploy/0-init.sh` to create new deploy account and folders
- Add secrets to the github secret configuration  
- Run action release, or make a new release by pushing to release/* branch  

### 5. Production - Using devbox as build server  
  
Requisites:
- Make sure 2-0-3-setup-acl.sh scripts ran successfully  
- Having at least 20GB HDD space  
  By default, vagrant disk capacity are 10GB, you need to increase the disk size to 30GB at least
  https://askubuntu.com/questions/317338/how-can-i-increase-disk-size-on-a-vagrant-vm
- Warning, this option will also require 16GB download   
- Edit secrets configuration in `scripts/deploy/.secrets`

Run:  
- `sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 --secret-file scripts/deploy/.secrets -j <event>` 
  
Example:  
- `sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 --secret-file scripts/deploy/.secrets -j build`  
- `sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 --secret-file scripts/deploy/.secrets -j pull_request`
- `sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 --secret-file scripts/deploy/.secrets -j release`  
- `sudo act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 --secret-file scripts/deploy/.secrets -j deploy`  

### 6. Production - Scripted deploy on traditional server if repo secret / remote ssh script running is not supported

This method expose what command is going to be run on the server.

- Edit password & ssh key and run `scripts/deploy/0-init.sh` to create new deploy account and folders
- Copy project to `/opt/kanava14fi/app`
- Run `scripts/deploy/1-master-run.sh` on every new deployment

### 7. Production - Deploy manually

- Follow scripts/deploy/2-* to install python, postgres and nginx  
- Follow scripts/deploy/3-1-setup-deployment.sh to install the project  
- Upload the directory `app/blog-development` to correct location on server
- `cp production.ini.sample production.ini`  
- Config production.ini as you see fit  
- Follow scripts/deploy/3-2-setup-postdeployment.sh to finish installing and  
  config the project  
- Follow scripts/deploy/4-1-run-predeploy.sh and 4-2-run-postdeploy.sh each time  
  you deploy a new change  

### 8. Customization  
  
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
- Load balancing with multiple server and database nodes
