pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "totemic-gravity-463311-h0"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repository...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/GuptaSandip/MLOPS_P1_Hotel_Reservation_System.git'
                        ]]
                    )
                }
            }
        }

        stage('Set up virtualenv and install dependencies') {
            steps {
                script {
                    echo 'Creating virtual environment and installing dependencies...'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Train Model') {
            steps {
                script {
                    echo 'Running training pipeline...'
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        python pipeline/training_pipeline.py
                    '''
                }
            }
        }

        stage('Build and Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'mlops-p1-gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and pushing Docker image to GCR...'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/mlops-p1:latest .
                            docker push gcr.io/${GCP_PROJECT}/mlops-p1:latest
                        '''
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed!"
        }
        success {
            echo "Pipeline completed successfully."
        }
    }
}
