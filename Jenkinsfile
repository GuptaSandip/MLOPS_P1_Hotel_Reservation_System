pipeline {
    agent any 

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "totemic-gravity-463311-h0"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Cloning GitHub repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins......'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/GuptaSandip/MLOPS_P1_Hotel_Reservation_System.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up virtual environment and installing dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment and installing dependencies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and pushing Docker image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'mlops-p1-gcp-key', variable: 'Google_Application_Credentials')]) {
                    script {
                        echo 'Building and pushing Docker image to GCR.....'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${Google_Application_Credentials}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/mlops-p1:latest .
                        docker push gcr.io/${GCP_PROJECT}/mlops-p1:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to google cloud run') {
            steps {
                withCredentials([file(credentialsId: 'mlops-p1-gcp-key', variable: 'Google_Application_Credentials')]) {
                    script {
                        echo 'Deploy to google cloud run.......'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${Google_Application_Credentials}
                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy mlops-p1 \
                            --image=gcr.io/${GCP_PROJECT}/mlops-p1:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                        '''
                    }
                }
            }
        }
    }
}
