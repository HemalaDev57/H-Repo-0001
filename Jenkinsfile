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

        stage('Generate 5MB SARIF scan report') {
            steps {
                sh 'python3 scripts/generate_large_sarif.py test/5mb-scan.sarif 5242880'
            }
        }

        stage('Register 5MB security scan') {
            steps {
                registerSecurityScan(artifacts: 'test/5mb-scan.sarif')
            }
        }

        stage('Generate 10MB SARIF scan report') {
            steps {
                sh 'python3 scripts/generate_large_sarif.py test/10mb-scan.sarif 10485760'
            }
        }

        stage('Register 10MB security scan') {
            steps {
                registerSecurityScan(artifacts: 'test/10mb-scan.sarif')
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
