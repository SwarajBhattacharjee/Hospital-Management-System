// ==============================================================================
// Jenkinsfile - Declarative CI/CD Pipeline
// DevOps & Automation Lab Capstone Project (ENSP461)
//
// PREREQUISITES ON JENKINS AGENT:
// 1. Python 3 (python3, python3-venv, pip) installed and on system PATH.
// 2. Docker CLI and Docker daemon access (user in 'docker' group).
//
// SHELL COMPATIBILITY NOTE:
// This pipeline uses 'sh' steps, which is standard for Linux-based Jenkins
// agents (e.g. Ubuntu, Docker-in-Docker). If your Jenkins agent runs directly
// on Windows without WSL/Linux agent, change 'sh' steps to 'bat'.
// ==============================================================================

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'hospital-management-system'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Creating Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated test suite with pytest...'
                sh '''
                    . venv/bin/activate
                    pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    // Archive JUnit test report for visibility in Jenkins UI
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${BUILD_NUMBER}..."
                sh """
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                """
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully: tests passed and Docker image built.'
        }
        failure {
            echo 'CI Pipeline failed: please check test results or build logs.'
        }
        always {
            echo 'Performing workspace housekeeping...'
            cleanWs deleteDirs: true, notFailBuild: true
        }
    }
}
