# Streamlit app Docker Image
## 1. Login with your AWS console and launch an EC2 instance
## 2. Run the following commands

Note: Do the port mapping to this port:- 8501


Installing Docker on Amazon Linux 2023 server system will allow users a seamless and efficient way to deploy and manage applications within isolated containers.

Docker doesn’t need an introduction because it has already been used by hundreds of administrators for deploying multiple applications on single hardware using virtualization. It also has simplified the process of packaging software packages and their dependencies into standardized units which ensures the consistency of them across different environments.

In this article, we will guide you through the steps to install Docker in Amazon Linux, so that you will be able to create light, portable, and self-contained containers.

On the Page  hide 
Requirements
Step 1: Update AL2023 Packages
Step 2. Installing Docker on Amazon Linux 2023
Step 3: Start and Enable its Service
Step 4: Allow docker to run without sudo
Step 5: Create a Container – Example
Step 6: Docker Uninstallation (optional)
Requirements
Nothing much just you need a working Amazon Linux 2023 with sudo rights to install packages and a working internet connection.

Step 1: Update AL2023 Packages
Once you have your Amazon Linux terminal access either directly or using SSH for the remote server, run the system update command. This will ensure all the installed packages on our system are up to date and also if there are some security updates available they will be downloaded as well. Besides all this, the DNF package manager will also rebuild its package index cache.
```bash
sudo dnf update
```
Step 2. Installing Docker on Amazon Linux 2023
The next step is to use the default Amazon repository to download and install the Docker. Although, the version of the Docker available through the system repo will not be the latest one but the most stable. Therefore, we go for that.
```bash
sudo dnf install docker
```
Installing Docker on Amazon Linux 2023
Step 3: Start and Enable its Service
Docker service will not be started and enabled by default after you complete its installation. We have to do that manually, here is the command to start the Docker.
```bash
sudo systemctl start docker
```
Now, if you also want Docker to start automatically with system boot then use this command:
```bash
sudo systemctl enable docker
```
To check and confirm the service is running absolutely fine, use:
```bash
sudo systemctl status docker
```
Step 4: Allow docker to run without sudo
The installation is completed but to run the commands of Docker every time you have to use sudo which can be annoying. So, to solve this, we have to add our current user to the Docker group. Use the given command to do that.
```bash
sudo usermod -aG docker $USER
```
Apply the changes we have done to Docker Group:
```bash
newgrp docker
```

```bash
git clone "your-project"
```

```bash
docker build -t entbappy/stapp:latest . 
```

```bash
docker images -a  
```

```bash
docker run -d -p 8501:8501 entbappy/stapp 
```

```bash
docker ps  
```

```bash
docker stop container_id
```

```bash
docker rm $(docker ps -a -q)
```

```bash
docker login 
```

```bash
docker push entbappy/stapp:latest 
```

```bash
docker rmi entbappy/stapp:latest
```

```bash
docker pull entbappy/stapp
```
