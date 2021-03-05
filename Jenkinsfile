pipeline {
  agent none
  stages {
    stage('run') {
      agent {
        node {
          label 'ECU-TEST'
        }

      }
      steps {
        startET(toolName: 'ECU-TEST', keepInstance: true, timeout: '120')
      }
    }

  }
}