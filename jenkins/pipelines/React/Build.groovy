
PROP = [:]

PROP['git_cred'] = 'github_ssh_key'
PROP['branch'] = 'main'
PROP['docker_tag'] = 'latest'
PROP['docker_file_path'] = 'Dockerfile.prod'
PROP['ecr_registry'] = '933060838752.dkr.ecr.eu-central-1.amazonaws.com'
PROP['aws_region'] = 'eu-central-1'
PROP['aws_cli_cred'] = 'aws_cli_cred'
PROP['image_name'] = 'hello-world-app'
PROP['email_recepients'] = "alexeymihaylovdev@gmail.com"

pipeline {
    agent {
        docker {
            label 'linux'
            image 'public.ecr.aws/q1f8b0h6/jenkins_agent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
        triggers {
        GenericTrigger(
                genericVariables: [
                        [key: 'refsb', value: '$.ref'],
                        [key: 'pusher', value: '$.pusher.name'],
                        [key: 'change_files', value: '$.commits[0].modified[0]']
                ],
                token: "react_app",
                tokenCredentialId: '',
                printContributedVariables: true,
                printPostContent: false,
                silentResponse: false,
                regexpFilterText: '$refsb',
                regexpFilterExpression: '^(refs/heads/main|refs/remotes/origin/main)'
                
        )
    }
    stages {
        stage('Git clone') {
            steps {
                script{
                    println("=====================================${STAGE_NAME}=====================================")
                    println("Cloning from branch ${PROP.branch} and using credentials ${PROP.git_cred}")
                    git branch: PROP.branch, credentialsId: PROP.git_cred, url: 'git@github.com:AlexeyMihaylovDev/hello-world-app.git'
                }
            }
        }
        stage('Create Docker Image') {
            steps {
                 script {
                 println("=====================================${STAGE_NAME}=====================================")
                  sh "docker build -t ${PROP.ecr_registry}/${PROP.image_name}:${PROP.docker_tag} -f  ${PROP.docker_file_path} ."
                 }

            }
        }
        stage('Upload to ECR AWS') {
            steps {
                script {
                println("=====================================${STAGE_NAME}=====================================")
                    withAWS(credentials: 'aws_cli_cred', region: 'eu-central-1') { 
                    def login = ecrLogin()
                    sh "${login}"
                    sh "docker push ${PROP.ecr_registry}/${PROP.image_name}:${PROP.docker_tag}"
                    }
                }
            }
        }
       // if you want to trigger deploy job
        stage('Trigger Deploy Job') {
            steps {
                build job: 'React/Deploy', parameters: [string(name: 'IMAGE_NAME', value: "${PROP.image_name}")]
            }
        }
    }
    
    post {
        always {
            script {
                currentBuild.description = ("Branch : ${PROP.branch}\n Image Name : ${PROP.image_name}\n Docker Tag : ${PROP.docker_tag}\n ECR Registry : ${PROP.ecr_registry}")
                EMAIL_MAP = [
                        "Job Name"      : JOB_NAME,
                        "Build Number"  : BUILD_NUMBER,
                        "Branch"        : "${PROP.branch}",
                        "More Info At"  : "<a href=${BUILD_URL}console> Click here to view build console on Jenkins. </a>",
                        "painted"       : "false"
                ]
                sendByMapFormat(PROP.email_recepients, currentBuild.result, EMAIL_MAP,
                        "Jenkins Report", "Build Notification - Jenkins Report", "Hello World App build")

            }
        }
        
    }
}


def sendByMapFormat (toUser, type, map, subject = "Jenkins Report", headLine = "Jenkins Report", message = "", attachmentFile = "", attachmentLogFile = false) {
  
  	/*
    	toUser            : Put email address here if it is for their attention and action.
        type              : Status of deploy job (*** SUCCESS\FAILURE or 0\1 ***).
        map               : All parameters to be shown on email's table. 'painted' boolean key inside map determines whether the table inside the email will be colored or not (true: green[SUCCESS], red[FAILURE] \ false: white).
        subject           : Subject of email.
        headLine          : HeadLine of email.
        message           : The message that is added to the bottom of the email.
        attachmentFile    : Path of the Attachment file (*** Must be relative to Workspace ***).
        attachmentLogFile : Attachment Jenkins log file (true \ false). 
    */
  
    script {
      
      	key = "painted"
      	if (map[key]){ // if 'key' exists inside map.
          
        	isPainted = map.find{ it.key == key }.value
          
          	if (!isPainted.toString().trim().toLowerCase().equals("true") && !isPainted.toString().trim().toLowerCase().equals("false")){
                echo "\"isPainted\" value must be a boolean parameter. Please fix it to the next time. Default value: isPainted = true."
              	isPainted = true
            }
          
          	map.remove(key)  
          
        } else {
        	isPainted = true
        }

      	ALL_USERS = toUser.split(";")
      
      	toEmail = ""
      	for (String USER : ALL_USERS) {
          toEmail += USER.contains("@")? "${USER};" : "${USER}@gmail.com;"
        }

        switch (type.toString().toUpperCase()) {

            case ["1", "FAILURE"] :
          		COLOR = isPainted.toBoolean() ? "salmon" : "white"
                TYPE  = "FAILURE"
          		ICON  = "&#128542;" 
                break

            case ["0", "SUCCESS"] :
          		COLOR = isPainted.toBoolean() ? "lightgreen" : "white"
                TYPE  = "SUCCESS"
          		ICON  = "&#128522;"
                break

            default:
              	COLOR = isPainted.toBoolean() ? "BurlyWood" : "white"
                TYPE = "MESSAGE"
          		ICON  = "&#128529;" 
        }

        MESSAGE      = message.replaceAll("\n", "<br>")
        HTML_MESSAGE = (MESSAGE.equals("")) ? "" :   "<tr><td colspan=\"2\">${MESSAGE}</td></tr>"
      
      	if (!attachmentFile.equals("")) {
      		try{
	    		readFile(attachmentFile)
			} catch(e) {
        	  	echo "\nFailed to find \"${attachmentFile}\". Will not be attached as a file to email.\n"
			}
        }
      
      	HEAD_LINE = "${ICON} ${headLine} - ${TYPE}"
      
      	TABLE_PROPERTIES = ""
      	map.each{ key, value -> 
        	TABLE_PROPERTIES += "<tr><td>${key}</td><td>${value}</td></tr>"
        }
      	
        String body = 
        
        """
			<html>
				<head>
					<style>
						table {
  							font-family: arial, sans-serif;
  							border-collapse: collapse;
  							width: 100%;
						}
                        
						td {
  							border: 1px solid black;
  							text-align: left;
  							padding: 10px;
						}
                        
						tr {
						  background-color: ${COLOR};
						}

					</style>
				</head>
                
				<body>
					<h2>
                    	${HEAD_LINE}
                    </h2>
                    
					<table>
                        
                        ${TABLE_PROPERTIES}

						${HTML_MESSAGE}

					</table>                  
				</body>
			</html>

        """

        emailext(
        	to:                 "${toEmail}",
            subject:            "${subject}",
            body:               "${body}",
            attachmentsPattern: "${attachmentFile}",
          	attachLog:          "${attachmentLogFile}",
          	mimeType:           "text/html"
        )
    }  
}
