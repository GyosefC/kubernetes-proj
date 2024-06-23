
properties([
        parameters([
                string(name: 'IMAGE_NAME', defaultValue: '', description: 'Image name to deploy')
         ])
])

pipeline {
    agent {
        docker {
            label 'linux'
            image 'public.ecr.aws/q1f8b0h6/jenkins_agent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Dowload private key') {
            steps {
                script {
                    println("=====================================${STAGE_NAME}=====================================")
                    global_s3_dowload("aws_cli_cred","eu-central-1","alexey-yolo","alexey_atech.pem","${WORKSPACE}/alexey_atech.pem")
                    }
                }
            }
        stage('Deploy App Image') {
            steps {   
                script {
                    println("=====================================${STAGE_NAME}=====================================")

                    def DOCKER_REGISTRY = "933060838752.dkr.ecr.eu-central-1.amazonaws.com"
                    def EC2_INSTANCES = ["3.123.253.127"]
                    // def IMAGE_NAME = "hello-world-app"
                    def TAG = "latest"
                    def ENVIROMENT = [:] 
                    def PORTS = [
                        8087 : "80"
                    ] 
                    println("Deploying ${IMAGE_NAME}:${TAG} to ${EC2_INSTANCES} ")
                    EC2_INSTANCES.each { server -> 
                    global_docker_run("aws_cli_cred","eu-central-1",DOCKER_REGISTRY,IMAGE_NAME,TAG,PORTS,ENVIROMENT,[:],"ubuntu","${server}","${WORKSPACE}/alexey_atech.pem",true)
                    }
                    }
                }
            }
        }
    
    post {
        always {
            echo 'This will always run'
        }
        
    }
}





// ============================================================================== Function to docker run ========================================================
def global_docker_run(def cred, String regionName = "ca-central-1", def dockerRegistry, def imageName, def tag, Map port = [:], Map enviroment = [:], Map volume = [:], String sshUser = null, String sshHost = null, String sshKey = null, def deleteAll = false, String sshPort = "22") {
    // Forming the SSH command to run on the remote host
    def sshCmd = "ssh -o StrictHostKeyChecking=no -i ${sshKey} -p ${sshPort} ${sshUser}@${sshHost}"
    

if (deleteAll) {
    try {
        println "Stopping and deleting all Containers and Images on the remote host"
        def stopAndDeleteCmd = "docker stop \$(docker ps -a -q) && docker rm \$(docker ps -a -q) && docker rmi \$(docker images -q)"
        println "running command ${sshCmd} '${stopAndDeleteCmd}'"
        sh(script: sshCmd + " '" + stopAndDeleteCmd + "'")    
    } catch (Exception e) {
        println "Error while stopping and deleting all Containers and Images on the remote host"
        e.printStackTrace()
    }
}


  // AWS CLI command to retrieve ECR authorization token
    def awsCliCmd = "aws ecr get-login-password --region ${regionName}"

    // Docker login command using the retrieved authorization token
    def dockerLoginCmd = "${awsCliCmd} | docker login --username AWS --password-stdin ${dockerRegistry}"

    // Forming the docker run command
    def dockerImage = "${dockerRegistry}/${imageName}:${tag}"
    def dockerRunCmd = "docker run -d"

    // Adding ports to the docker run command if they are defined
    if (!port.isEmpty()) {
        def portCmd = port.collect { k, v -> "-p ${k}:${v}" }.join(" ")
        dockerRunCmd += " ${portCmd}"
    }      
    // Adding environment variables to the docker run command if they are defined
    if (!enviroment.isEmpty()) {
        def envCmd = enviroment.collect { k, v -> "-e ${k}=${v}" }.join(" ")
        dockerRunCmd += " ${envCmd}"
    }      
    // Adding volumes to the docker run command if they are defined
    if (!volume.isEmpty()) {
        def volumeCmd = volume.collect { k, v -> "-v ${k}:${v}" }.join(" ")
        dockerRunCmd += " ${volumeCmd}"
    }
        
    dockerRunCmd += " ${dockerImage}"

    // Adding Docker login command and Docker run command
    def combinedCmd = "${dockerLoginCmd} && ${dockerRunCmd}"

    // Running the combined command remotely via SSH
    println "Running the following command remotely via SSH on ${sshHost}: ${combinedCmd}"
    def sshOutput = sh(script: sshCmd + " '" + combinedCmd + "'", returnStdout: true).trim()

    return dockerImage
}

def global_s3_dowload (cred, region, bucketName, fileToDownload, destinationPath) {
  withAWS(credentials: cred, region: region) {
    println "Downloading file ${fileToDownload} from bucket ${bucketName} to ${destinationPath}"
    sh "aws s3 cp s3://${bucketName}/${fileToDownload} ${destinationPath}"
    sh "chmod 600 ${destinationPath}"
  }   
}