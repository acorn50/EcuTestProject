pipeline {
  agent {
    node {
      label 'ECU-TEST'
    }

  }
  stages {
    stage('init') {
      agent {
        node {
          label 'ECU-TEST'
        }

      }
      steps {
        checkETLicense(toolName: 'ECU-TEST', timeout: '120')
      }
    }

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