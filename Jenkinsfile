pipeline {
    agent any 

    environment {
        VENV_DIR = 'venv'
    }

    stages{
        stage('cloning github repo to Jenkins'){
            steps{
                script{
                    echo 'cloning github repo to Jenkins......'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/GuptaSandip/MLOPS_P1_Hotel_Reservation_System.git']])
                }
            }
        }


        stage('setting up our virtual environment and installing dependencies'){
            steps{
                script{
                    echo 'setting up our virtual environment and installing dependencies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                     '''
                    
                }
            }
        }
    }
}