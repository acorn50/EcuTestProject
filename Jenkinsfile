pipeline {
  agent {label 'EcuTest'}
  stages {
    stage('init') {
      steps {
        sh 'python /var/lib/jenkins/workspace/develop_main/algorithm.py'
      }
    }
  }
}
