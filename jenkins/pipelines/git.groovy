properties([
        parameters([
                string(name: 'AWS_CRED', defaultValue: 'aws_cred', description: 'AWS Credentials ID'),
                string(name: 'S3_BUCKET', defaultValue: 'alexey--demo', description: 'S3 Bucket Name'),
                string(name: 'S3_FILE', defaultValue: 'demofile', description: 'S3 File Name'),
                string(name: 'DEST', defaultValue: '${WORKSPACE}', description: 'Destination Folder'),
                string(name: 'REGION', defaultValue: 'us-east-1', description: 'AWS Region'),
                string(name: 'BRANCH', defaultValue: 'main', description: 'branch for git clone'),
                string(name: 'AGENT', defaultValue: 'linux', description: 'Choose Agent'),
                hidden(defaultValue: 'github_ssh_key', name: 'GIT_CRED'),
                booleanParam(name: 'S3', defaultValue: true, description: 'Enable Debugging'),
                choice(name: 'CHOICE', choices: ['main', 'development', 'feature'], description: 'Choose one'),
                [$class: 'CascadeChoiceParameter', choiceType: 'PT_CHECKBOX', filterLength: 1, filterable: false,
                             name: 'MODULES', referencedParameters: 'AWS_CRED',
                             script: [$class: 'GroovyScript', fallbackScript: [classpath: [], oldScript: '', sandbox: true, script: 'return [\'error\']'],
                                      script: [classpath: [], oldScript: '', sandbox: true, script: 
                                      '''
                                      def list_modules = ['polybot', 'yolo5' , 'atechbot']
                                      return list_modules
                                      '''
                                      ]]]   
         ])
])

pipeline {

    agent { label params.AGENT}



    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }

    stages {
        stage('Git clone') {
            steps {
                script{
                    println("=====================================${STAGE_NAME}=====================================")
                    println("Cloning from branch ${params.BRANCH} and using credentials ${params.GIT_CRED}")
                    git branch: params.BRANCH, credentialsId: params.GIT_CRED, url: 'git@github.com:AlexeyMihaylovDev/atech-devops-nov-2023.git'
                }
            }
        }

        stage('Download from S3 Bucket') {
            when {expression { params.S3 == true }}
            steps {
                script{
                    println("=====================================${STAGE_NAME}=====================================")
                    download_from_s3(params.AWS_CRED,params.S3_BUCKET,"${params.S3_FILE}","${params.DEST}","${params.REGION}")  
                }
            }
        }
    }                    // faulure, success, aborted , unstable
    post{
        always{
            echo "This will always run"
        }
        failure{
            echo "This will run only if failed"
        }
        success{
            echo "This will run only if success"
        }
        unstable{
            echo "This will run only if unstable"
        }
    
    }
}


//============================================================FUNC=====================================================


    
def download_from_s3(def cred,def bucket, def file, def dest,def region='us-east-1'){
    withAWS(credentials: cred, region: region ) {
        println("Downloading file name ${file} from bucket ${bucket} to ${dest}")
        sh "aws s3 cp s3://${bucket}/${file} ${dest}"         
    }
}