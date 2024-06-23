

pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
                
                println('Hello World')
                
                sh "echo 'Hello World'" 
                
                sh 'ifconfig'
                
                sh 'apt update -y '
                
            }
        }
    }
}


