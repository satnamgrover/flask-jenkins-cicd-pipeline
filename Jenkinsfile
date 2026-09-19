pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = "$DOCKERHUB_CREDENTIALS_USR/cicd-pipeline-project"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                }
        }
        stage('lint'){
            steps{
                sh ''' 
                python3 -m venv venv
                . venv/bin/activate
                pip install flake8
                flake8 app/ tests/ --max-line-length=100
                '''
            }
        }
        stage('test'){
            steps{
                sh '''
                . venv/bin/activate
                pip install -r requirements-dev.txt
                pytest tests/ -v
                '''
            }
        }
        
        stage('build'){
            steps{
                sh ''' docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'''
            }
        }
        stage('Push To DockerHub'){
            steps{
                sh'''
                echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                docker push ${IMAGE_NAME}:${IMAGE_TAG}
                docker push ${IMAGE_NAME}:latest
                '''
            }
        }
        stage('Deploy'){
            steps{
                sh "docker run -d -p 5000:5000 --name flask-app ${IMAGE_NAME}:latest"
            }
        }
    }
     post {
        // Runs regardless of success/failure - good place for cleanup and notifications
        always {
            sh 'docker logout || true'
            cleanWs()
        }
        success {
            echo "Pipeline succeeded: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline failed - check the stage logs above.'
        }
    }
}

