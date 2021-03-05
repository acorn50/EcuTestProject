pipeline {
  agent {
    label 'ECU-TEST'
  }
  stages {
    stage('init') {
      agent {
        node {
          label 'ECU-TEST'
        }

      }
      steps {
        checkETLicense 'ECU-TEST'
      }
    }

    stage('run') {
      agent {
        node {
          label 'ECU-TEST'
        }

      }
      steps {
        startET 'ECU-TEST'
      }
    }

  }
}