
def message = 'Hello, Jenkins!'

pipeline {
    agent any

    stages {
        stage('Get IP Configuration') {
            steps {
                // For Windows, use ipconfig command, for Unix-like systems, use ifconfig
                bat 'ipconfig' // Replace 'ipconfig' with 'ifconfig' for Unix-like systems
            }
        }
        stage('Get Hostname') {
            steps {
                bat 'hostname'
            }
        }
        stage('Get linux IP Configuration') {
            steps {
                sh 'ifconfig'
                printls({})
            }
        }
    }
}
