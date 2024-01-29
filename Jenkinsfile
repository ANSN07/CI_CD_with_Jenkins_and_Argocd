pipeline {
    environment {
        REGISTRY_CREDENTIAL = 'dockerhub_credentials'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_USERNAME = 'alnx551'
        APP_NAME = 'python-app'
        IMAGE_NAME = "${DOCKERHUB_USERNAME}" + '/' + "${APP_NAME}"
    }
    agent any
    stages {
        stage('Checkout Source') {
            steps {
                git 'https://github.com/ANSN07/python.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build IMAGE_NAME
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', REGISTRY_CREDENTIAL) {
                        dockerImage.push("${BUILD_NUMBER}")
                    }
                }
            }
        }
        stage('Modify the image in Kubernetes deployment file') {
            steps {
                sh 'cat deployment.yaml'
                sh "sed -i 's/${APP_NAME}.*/${APP_NAME}:${IMAGE_TAG}/g' deployment.yaml"
                sh 'cat deployment.yaml'
            }
        }
        stage('Push the changed deployment file to Git') {
            steps {
                script {
                    sh """
                    git config --global user.name "Alka"
                    git config --global user.email "20100677@mail.wit.ie"
                    git add deployment.yaml
                    git commit -m 'Updated the deployment file: ${BUILD_NUMBER}' """
                    withCredentials([usernamePassword(credentialsId: 'github_credentials', passwordVariable: 'pass', usernameVariable: 'user')]) {
                        sh "git push https://$user:$pass@github.com/ANSN07/python.git master"
                    }
                }
            }
        }
    }
}
