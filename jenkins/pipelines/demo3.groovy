

//================================================================ PARAMETRS ======================================================



def message = "Hello, Jenkins!"

def JOB = [:]

//================================================================ PARAMETRS ======================================================



pipeline {
    agent any

    stages {
        stage('Get params') {
            steps {
                echo 'Get parametrs'
                
            }
        }
        stage('Git clone') {
            steps {
                echo 'Git clone'
            }
        }
        stage('Build project') {
            steps {
              script{
                echo 'Build project'
                
                println("${message}")
                
                JOB.msg = "${message}"
                
                println(" The my JOB : ${JOB.msg} ")
                

                }
            }
        }
    }
}


//================================================================ FUNCTIONS ======================================================


