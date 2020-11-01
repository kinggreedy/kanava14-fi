

# Welcome to Kanava14.fi 
This project kicks start the revolution for social platform 4.0      
or so....  
  
Preview https://kanava14.kinggreedy.com/    
  
# Quick start

- `cd scripts/vagrant`
- `vagrant up`
- Start development from app/blog-platform
- Visit http://localhost:8080

# Architecture story  
  
Although the test only requires us to develop a platform, I would like to put the context of starting a brand new website for a new client that does not have a website before, providing a small CD/CI solution without any previous tools for DevOps.  
This approach cause a small problem with the architecture and repository management, because this repository actually host 3 components at once (which should have their own repo): application, devbox, deployment scripts. I tried to not over engineering while keeping everything clean and robust.   
  
There are some assumption to be made:  
- Production server could be a virtual private server (not having Kubernetes capability), like using DigitalOcean, Upcloud, Linode, or any VPS similar providers
- There is no information if production server can install docker or not  
- The production server is newly installed and is dedicated to only this project  
- For shared environment, system administrator can use the scripts in scripts/deploy and the description below as assistance  
  - 2-*-.sh scripts: Dependencies installation commands  
  - 3-*-.sh scripts: Project setup commands  
  - 4-*-.sh scripts: Project deploy commands  

# Branching model

- Trunk based
- Production server will use latest commit from branch `releases/x.x`
- Pull request to `master` branch will be tested for code styling and unit test

# Instruction on starting the project  
  
### 1. Development - Devbox/Vagrant  

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
- Follow setup commands in scripts/devbox/3-0-*.sh to  
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
- Add secrets to the github secret configuration  (Please check customization below)
- Run action release, or make a new release by pushing to `release/*` branch  

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

### 6. Production - Scripted deploy

- Edit password & ssh key and run `scripts/deploy/0-init.sh` to create new deploy account and folders
- Copy project to `/opt/kanava14fi/app`
- Run `scripts/deploy/1-master-run.sh` on every new deployment
- Add language detector api key to `production.ini`

### 7. Production - Deploy manually

- Follow scripts/deploy/2-* to install python, postgres and nginx  
- Follow scripts/deploy/3-1-setup-deployment.sh to install the project  
- Upload the directory `app/blog-development` to correct location on server
- `cp production.ini.sample production.ini`  
- Config `production.ini` as you see fit  
- Set api key for language detector in `production.ini`
- Follow `scripts/deploy/3-2-setup-postdeployment.sh` and `scripts/deploy/3-3-setup-postdeployment.sh` 
  to finish installing and config the project  
- Follow `scripts/deploy/4-1-run-predeploy.sh` and `4-2-run-postdeploy.sh`
  each time you deploy a new change  

### 8. Customization  
  
#### app/blog-platform/development.ini or app/blog-platform/production.ini
  
|Key             |Description                    |Default value                |  
|----------------|-------------------------------|-----------------------------|  
| `project.name` | Project name (title, logo) | `Kanava14.fi` |  
| `userauthentication.secret` | Secret for user session and cookie | Randomized upon setup |  
| `sqlalchemy.url` | URL for DB connection | Randomized upon setup (For Docker - set from `scripts/docker/.env` upon setup) |  
| `listen` | Handle host:port request | For development: `*:8080`, For production: take from supervisord, default values are `5000` & `5001` |  

#### app/blog-platform/nginx.conf - Configuration for nginx
*Note: Symlinked to site-available & site-enabled upon deployment*
#### app/blog-platform/supervisord.conf - Configuration for supervisord

Change `command` under `[program:myapp]` to have different backend port than 5000 & 5001

#### scripts/docker/.env - Configuration for docker development

|Key             |Description                    |Default value                |  
|----------------|-------------------------------|-----------------------------|  
| `DB_USER` | Database username | |  
| `DB_PASS` | Database password | |  

#### scripts/vagrant/Vagrantfile - Configuration for vagrant development

|Key             |Description                    |Default value                |  
|----------------|-------------------------------|-----------------------------|  
| `config.vm.network "forwarded_port"` | Forwarding port from guest to host | port `8080` (http) and `22` (ssh) |  
| `config.vm.synced_folder` | Shared folders between host and guest <br> Remove this value if planning to use unison | `"."` => `"/vagrant"` <br> `"../.."` => `"/opt/kanava14fi/app"` <br> `"../../app/blog-platform"` => `"/opt/kanava14fi/blog-platform"` | 
| `config.vm.provision "shell"` | Vagrant provision script, scripts with format under `scripts/devbox/*-0-*` are optional | | 
| `echo "vagrant:vagrant" \| chpasswd` | Default password for vagrant if using unison, change to a more challenging password before exposing ssh to public | | 

#### scripts/vagrant/sync-app.ps1 or scripts/vagrant/sync-project.ps1 - Configuration for unison sync with Vagrant development

|Key             |Description                    |Default value                |  
|----------------|-------------------------------|-----------------------------|  
| `$project` | Project folder | `blog-platform` |  
| `$server` | Vagrant devbox ip | |  
| `$username` | Vagrant login username | `vagrant` |  
| `$password` | Vagrant login password | `vagrant` |  
| `$port` | Vagrant devbox port | `22` | 
| `$project_host_dir` | Project location on host | `../../app/$project` | 
| `$project_guest_dir` | Project location on guest| `ssh://$server//opt/kanva14fi/$project` | 

#### Github Secrets or scripts/deploy/.secrets - Configuration for using Github Secrets or command line act to build and deploy

|Key             |Description                    |Default value                |  
|----------------|-------------------------------|-----------------------------|  
| `PRODUCTION_HOST` | Production server ip | |  
| `PRODUCTION_PORT` | Production server ssh port | |  
| `PRODUCTION_SSH_USER` | Deploy username | |  
| `PRODUCTION_SSH_KEY` | Deploy ssh private key in base64 format `base64 -w 0 <privatekey>` |  |  
| `PRODUCTION_SSH_PASSWORD` | Deploy ssh password | |
| `PRODUCTION_LANGUAGE_DETECTOR_API_KEY` | https://detectlanguage.com/ API KEY | |  
    
# Roadmap  
  
- More unit test  
- RestAPI
- Deployment with docker and kubernetes
- Load balancing with multiple server and database nodes
