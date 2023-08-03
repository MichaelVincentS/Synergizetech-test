pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('2f4dd153-425d-4486-a113-b72e0967597b')
  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t michaelvs2000/synergize-test:latest .'
      }
    }
    stage('Login') {
      steps {
        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
      }
    }
    stage('Push') {
      steps {
        sh 'docker push michaelvs2000/synergize-test:latest'
      }
    }
  }
  post {
    always {
      sh 'docker logout'
    }
  }
}