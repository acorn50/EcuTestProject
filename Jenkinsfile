pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh 'python /var/lib/jenkins/workspace/develop_main/algorithm.py'
      }
    }

    stage('test') {
      steps {
        sh 'python /var/lib/jenkins/workspace/testPython/hello.py'
      }
    }

    stage('notify') {
      steps {
        emailext(body: '$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS:  Check console output at $BUILD_URL to view the results.', subject: '$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!', to: 'jiangcw@dfmc.com.cn', mimeType: 'text/html', attachLog: true, compressLog: true)
      }
    }

  }
}
