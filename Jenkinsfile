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
        bat 'start "D:\\Program Files\\ECU-TEST 2020.1\\ECU-TEST.exe"'
        startET 'ECU-TEST'
      }
    }

  }
}