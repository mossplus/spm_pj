def label = "slave-${UUID.randomUUID().toString()}"
podTemplate(label: label, containers: [
  containerTemplate(name: 'docker', image: 'docker:latest', command: 'cat', ttyEnabled: true),
  containerTemplate(name: 'kubectl', image: 'cnych/kubectl', command: 'cat', ttyEnabled: true),
  containerTemplate(name: 'python', image: 'python:3.9.10', command: 'cat', ttyEnabled: true)
], serviceAccount: 'jenkins', volumes: [
  hostPathVolume(mountPath: '/home/jenkins/.kube', hostPath: '/root/.kube'),
  hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock')
]) {
  node(label) {
    def myRepo = checkout scm
    def gitCommit = myRepo.GIT_COMMIT
    def gitBranch = myRepo.GIT_BRANCH
    // 获取 git commit id 作为镜像标签
    def imageTag = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
    def registryUrl = "10.176.40.151:30005"
    def imageEndpoint = "spm_pj/spm_pj_end"
    // 镜像
    def image = "${registryUrl}/${imageEndpoint}:${imageTag}"
    stage('单元测试') {
        container("python"){
            echo "单元测试阶段"
            sh """
            pip install -r requirement.txt
            python manage.py test
            """
        }
    }
    stage('构建 Docker 镜像') {
        withCredentials([[$class: 'UsernamePasswordMultiBinding',
            credentialsId: 'docker-auth',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASSWORD']]) {
                container('docker') {
                echo "构建 Docker 镜像阶段"
                sh """
                docker login ${registryUrl} -u ${DOCKER_USER} -p ${DOCKER_PASSWORD}
                docker build -t ${image} .
                docker push ${image}
                """
            }
        }
    }
    stage('运行 Kubectl') {
      container('kubectl') {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
            env.BUILD_IMAGE="${image}"
            sh "env"
            sh "mkdir -p ~/.kube && cp ${KUBECONFIG} ~/.kube/config"
            sh "kubectl get pods -n default"
            sh "kubectl apply -f deployment.yaml"
            sh "kubectl get deployment -n default"
            sh "kubectl set image deployment.apps/spm-pj-auto-deployment spm-pj-auto=${image} -n default"
      }
    }
  }
}
}
