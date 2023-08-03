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
    BUILD_ID_IMAGE = "${BUILD_ID}"
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
            sh '''#!/bin/bash
                 sed -i 's/SHORT_SHA/${env.BUILD_ID_IMAGE}/g' ./kubernetes-manifest/application/application.yaml
            '''
            step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: './kubernetes-manifest/application/application.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
            step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: './kubernetes-manifest/application/configmap.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
        }
    }
  }
  post {
    always {
      sh 'docker logout'
    }
  }
}