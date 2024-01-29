# CI/CD with GitHub, Jenkins, Argo CD and Kubernetes Cluster

---

## Jenkins Setup

### Jenkins Installation

```shell
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo dnf upgrade
# Add required dependencies for the jenkins package
sudo dnf install fontconfig java-17-openjdk
sudo dnf install jenkins
sudo systemctl daemon-reload
```

### Start Jenkins

You can enable the Jenkins service to start at boot with the command:

```shell
sudo systemctl enable jenkins
```

You can start the Jenkins service with the command:

```shell
sudo systemctl start jenkins
```

You can check the status of the Jenkins service using the command:

```shell
sudo systemctl status jenkins
```

Browse to http://localhost:8080 (Make sure port 8080 is not used by other processes)

### Post-installation setup wizard

#### 1. Unlocking Jenkins

- When you first access a new Jenkins instance, you are asked to unlock it using an automatically-generated password.

- From the Jenkins console log output, copy the automatically-generated alphanumeric password (between the 2 sets of asterisks) or alternatively use the command to print the password at console: 

```shell
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

- This password also serves as the default administrator account’s password (with username "admin") if you happen to skip the subsequent user-creation step in the setup wizard.

#### 2. Select "Install suggested plugins"

#### 3. Create the first administrator user

Click Save and Finish. When the Jenkins is ready page appears, click Start using Jenkins.

If required, log in to Jenkins with the credentials of the user you just created and you are ready to start using Jenkins!

### Install Docker Pipeline Plugin

To install Docker Pipeline Plugin (enables you to add Docker commands in Jenkinsfile), 
1. click "Manage Jenkins"
2. click Manage Plugins 
3. search for Docker Pipeline under Available plugins
4. Click the Download now and install after restart button


### Add GitHub and Docker Hub Credentials to Jenkins Credentials Manager

1. Go to the Jenkins Dashboard and click Manage Jenkins
2. Click Manage Credentials
3. Click Select System, then Global Credentials (unrestricted) to then Add Credentials
4. Add Docker Hub Username and Password
5. Add ID (should be same as those specified in the Jenkinsfile, in this case: dockerhub_credentials)
6. Click the Create button.
6. Repeat the same for adding GitHub credentials 
- GitHub access token must be used as the GitHub password as Jenkins need to do a GitHub push in this case 
- use ID as github_credentials


---


## Kind cluster setup

```shell
kind create cluster --name=<cluster-name>
```

## Clone Repo

The repository will need to be public for the rest of the tutorial to work properly. You will push your Jenkinsfile, application files, and deployment files to the new GitHub repository. 

## Create Jenkins pipeline

1. Open the Jenkins Dashboard and Click New Item
2. Enter an item name
3. Select Pipeline
4. Check "GitHub hook trigger for GITScm polling" in Build Triggers section
5. Select pipeline script from SCM in pipeline section
6. Select Git as SCM
7. Give the repo URL and credentials
8. Specify the branch and click save
9. click "Build Now" to run pipeline

[Use console output to see the output]

## Installing ArgoCD in Kubernetes Cluster

```shell
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

you can verify the deployment by checking the status of the ArgoCD pods:

```shell
kubectl get pods -n argocd
```

To access the ArgoCD dashboard, use the Port Forwarding to access the ArgoCD.

```shell
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

[use 8081 as Jenkins already running in 8080]

Access ArgoCD Dashboard from your local machine using the following link:
http://127.0.0.1:8081

To get the password you may execute the below command in your Kubernetes cluster. (username is admin):

```shell
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## Create an Application in ArgoCD

1. Application Name
2. Project Name: default
3. Sync Policy: Automatic
4. Check Auto-create Namespace
5. Repo URL: where we have the manifest file (deployment.yaml)
6. Revision: HEAD (branch-name or commit)
7. Path to manifest file : ./
8. Cluster URL: https://kubernetes.default.svc (Application's K8s API server address - as deploying to the same cluster that Argo CD is running in)
9. Namespace: default
10. Click create

As we have defined the nodeport service type in the manifest file, we can access the pod using the node port. <WorkerNodeIP:30001>

By entering the appropriate Worker Node IP address and the designated NodePort in a web browser, we can establish a connection to the Pod running our application.

---
## References

- Jenkins setup on Fedora: https://www.jenkins.io/doc/book/installing/linux/#fedora
- ArgoCD documentation: https://argo-cd.readthedocs.io/en/stable/
- Defining ArgoCD projects: https://argo-cd.readthedocs.io/en/stable/user-guide/projects/
- Managing personal access token in GitHub: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- Connecting private repositories in ArgoCD: https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/
