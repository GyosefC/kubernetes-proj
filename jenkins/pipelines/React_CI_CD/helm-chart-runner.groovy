import groovy.json.JsonBuilder
import groovy.json.JsonSlurper
import groovy.json.JsonSlurperClassic
import groovy.transform.Field

@Field JOB = [:]

JOB.trigg_by = currentBuild.getBuildCauses('hudson.model.Cause$UserIdCause').userName

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
                regexpFilterExpression: '^(refs/heads/main)'        
        )
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }

    stages{
        stage('Git clone'){
            steps{
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: 'https://github.com/AlexeyMihaylovDev/atech-devops-nov-2023']]])    
            }
        }
        stage('Read helm chart values'){
            steps{
                script{  
                    
                     dir("${WORKSPACE}/k8s/helm/react_site")  {
                     sh 'ls -l'    
                    def chartValues = readFile (file: 'values.yaml')  
                    JOB.buildChartValues = chartValues
                     }
                    println(JOB.buildChartValues)
                                
                }
                
            }
         }
        stage('Input params '){
            when{
                expression { !JOB.trigg_by.isEmpty()}
            }
            steps{
                script{
                    def userInput = input (id: 'userInput', message: 'Please provide the following parameters', parameters: [
                        [$class: 'WHideParameterDefinition', defaultValue: JOB.buildChartValues, description: '', name: 'chartValues'],
                        choice(name: 'CHOICE_HELM', choices: ['install','upgrade','uninstall'], description: 'Choose one'),
                        [$class: 'DynamicReferenceParameter', choiceType: 'ET_FORMATTED_HTML', description: "",
                             name: 'ChartValues', omitValueField: true, referencedParameters: 'chartValues',
                             script: [$class: 'GroovyScript', fallbackScript: [classpath: [], sandbox: true,
                                                                               script: 'return [\'error\']'], script: [classpath: [], sandbox: true, script: '''
                                def jsonValue = "${chartValues}".replaceAll('"', '\\\\"') 
                                return "<textarea name=\\"value\\" rows='27' cols='100'>${jsonValue}</textarea>"
                            ''']]],

                    ])
                    JOB.params = userInput['ChartValues']
                    sh 'rm -f values.yaml' //delete old values.yaml

                }
            }
        }
        stage('Helm update values by user input'){
            when{
                expression { !JOB.trigg_by.isEmpty()}
            }
            steps{
                script{
                     dir("${WORKSPACE}/k8s/helm/react_site")  {
                        writeFile file: 'values.yaml', text: JOB.params
                    }
                }
            }
        }
        stage('Run is Job with Auto Trigger'){
            when{
                expression { JOB.trigg_by.isEmpty()
                }
            }
            steps{
                script{
                    println("=====================================${STAGE_NAME}=====================================")
                }
            }
        }
        
        // stage('Login to EKS'){
        //     steps{
        //         script{
        //             withCredentials([string(credentialsId: 'aws-eks-creds', variable: 'AWS_CREDENTIALS')]) {
        //                 sh 'aws eks --region us-west-2 update-kubeconfig --name alexey'
        //             }
        //         }
        //     }
        // }

        stage('Helm install'){
            steps{
                script{
                     dir("${WORKSPACE}/k8s/helm/react_site")  {
                        sh 'helm install react-site . -f values.yaml -n alexey'
                    }
                }
            }
        }
        }
    }
