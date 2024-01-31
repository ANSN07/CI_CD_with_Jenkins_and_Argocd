pipeline {
    environment {
        REGISTRY_CREDENTIAL = 'dockerhub_credentials'
        DOCKERHUB_USERNAME = 'alnx551'
        IMAGE_TAG = "${BUILD_NUMBER}"
        APP_NAME = 'python-app'
        IMAGE_NAME = "${DOCKERHUB_USERNAME}" + '/' + "${APP_NAME}"
    }
    agent any
    stages {
        stage('Checkout Source') {
            steps {
                git 'https://github.com/ANSN07/CI_CD_with_Jenkins_and_Argocd'
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
	stage('Modify') {
            steps {
	        withCredentials([usernamePassword(credentialsId: 'github_credentials', passwordVariable: 'pass', usernameVariable: 'user')]) {
			sh "rm -rf Flask-App-Manifests"	
			sh "git clone https://github.com/ANSN07/Flask-App-Manifests.git" // clone the repo
				sh "cd Flask-App-Manifests"
				dir('Flask-App-Manifests') {
					sh "sed -i 's/${APP_NAME}.*/${APP_NAME}:${IMAGE_TAG}/g' deployment.yaml"
					sh "git config user.email 20100677@mail.wit.ie" // set git config
					sh "git config user.name Alka" // set git config
					sh "git add deployment.yaml" // add the updated manifest to git
					sh "git commit -m 'Updated the deployment file: ${BUILD_NUMBER}'" // commit the changes
					sh "git push https://$user:$pass@github.com/ANSN07/Flask-App-Manifests.git main" // push changes
				}
			}
	    }
	}
    }
}
