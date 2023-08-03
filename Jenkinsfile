pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('2f4dd153-425d-4486-a113-b72e0967597b')
    PROJECT_ID = 'synergize-test'
    CLUSTER_NAME = 'synergize-test-gke'
    LOCATION = 'asia-southeast2'
    CREDENTIALS_ID = 'synergize-test'
  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t michaelvs2000/synergize-test:${BUILD_ID} .'
      }
    }
    stage('Login') {
      steps {
        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
      }
    }
    stage('Push') {
      steps {
        sh 'docker push michaelvs2000/synergize-test:${BUILD_ID}'
      }
    }
    stage('Deploy to GKE') {
        steps{
            sh "sed -i 's/hello:latest/hello:${env.BUILD_ID}/g' deployment.yaml"
            step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'kubernetes-manifest/deployment.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
        }
    }
  }
  post {
    always {
      sh 'docker logout'
    }
  }
}