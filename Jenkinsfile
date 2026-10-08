pipeline {
    agent any

    stages {
        stage('Build') {
            stages {
                stage('Compile') {
                    steps {
                        echo 'Compiling...'
                        sleep 5
                    }
                }
                stage('Package') {
                    steps {
                        echo 'Packaging...'
                        sleep 5
                    }
                }
            }
        }

        stage('Registering build artifact') {
            steps {
                echo 'Registering the metadata'
                script {
                        registerBuildArtifactMetadata(
                            name: "my-test-artifact",
                            version: "1.0.0",
                            type: "docker",
                            url: "http://localhost:1111",
                            digest: "6f637064707039346163663237383938",
                            label: "prod"
                        )
                }
            }
        }

        stage('Register sample security scan') {
            steps {
                registerSecurityScan(artifacts: 'testdata/trivy.sarif')
            }
        }

        stage('Generate large SARIF scan report') {
            steps {
                sh 'python3 scripts/generate_large_sarif.py test/large-scan.sarif'
            }
        }

        stage('Register large security scan') {
            steps {
                registerSecurityScan(artifacts: 'test/large-scan.sarif')
            }
        }

        stage('Test') {
            steps {
                echo 'Running Unit Tests...'
                sleep 5
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sleep 5
            }
        }
    }
}
