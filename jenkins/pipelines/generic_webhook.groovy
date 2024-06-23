//http://localhost:8080/generic-webhook-trigger/invoke?token=abc123


PROP = [:]

PROP['git_cred'] = 'github_ssh_key'
PROP['branch'] = 'triggers'


pipeline {
    agent any
        triggers {
        GenericTrigger(
                genericVariables: [
                        [key: 'refsb', value: '$.ref'],
                        [key: 'pusher', value: '$.pusher.name'],
                        [key: 'change_files', value: '$.commits[0].modified[0]'],
                        // [key: 'type', value: '$.changes[0].type'],
                ],
                token: "123456",
                tokenCredentialId: '',
                printContributedVariables: true,
                printPostContent: false,
                silentResponse: false,
                regexpFilterText: '$refsb $change_files',
                regexpFilterExpression: '^(refs/heads/triggers|refs/remotes/origin/triggers) .*pipelines/+?.*'
                
        )
    }
//  triggers {
//         GenericTrigger(
//                 genericVariables: [
//                         [key: 'ref', value: '$.ref'],
//                         [key: 'changed_files', value: '$.commits[*].[\'modified\',\'added\',\'removed\'][*]']
//                 ],

//                 token: 'bot_dev',
//                 tokenCredentialId: '',

//                 printContributedVariables: true,
//                 printPostContent: true,

//                 silentResponse: false,

//                 shouldNotFlattern: false,

//                 regexpFilterText: '$ref $changed_files',
//                 regexpFilterExpression: '^(refs/heads/dev|refs/remotes/origin/dev) .*common/+?.*|.*services/bot/+?.*'
//         )
//     }

    stages {
        stage('Git clone') {
            steps {
                script{
                    println("=====================================${STAGE_NAME}=====================================")
                    println("Cloning from branch ${PROP.branch} and using credentials ${PROP.git_cred}")
                    git branch: PROP.branch, credentialsId: PROP.git_cred, url: 'git@github.com:AlexeyMihaylovDev/atech-devops-nov-2023.git'
                }
            }
        }
        stage('Print params') {
            steps {
                 script {
                 println("=====================================${STAGE_NAME}=====================================")

                 println("+++++++++++++++++++++++++++++++++++++++++++++++++BRANCHE: ${refsb}")
                 println("+++++++++++++++++++++++++++++++++++++++++++++++++PUSHER: ${pusher}")
                    println("+++++++++++++++++++++++++++++++++++++++++++++++++CHANGE FILES: ${change_files}")

                 }

            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
    post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}
