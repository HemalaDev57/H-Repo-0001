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

        stage('Generate large SARIF report') {
            steps {
                sh '''
                    mkdir -p test
                    python3 -c "
import json, os

target_size = 50 * 1024 * 1024  # 50MB raw file
report = {
    'version': '2.1.0',
    'runs': [{
        'tool': {'driver': {'name': 'test-scanner'}},
        'results': [{'ruleId': 'test-rule', 'message': {'text': ''}}]
    }]
}
base_len = len(json.dumps(report))
report['runs'][0]['results'][0]['message']['text'] = 'a' * (target_size - base_len)
with open('test/bigscan.sarif', 'w') as f:
    json.dump(report, f)
print('wrote', os.path.getsize('test/bigscan.sarif'), 'bytes')
"
                '''
            }
        }

        stage('Register large security scan') {
            steps {
                registerSecurityScan(artifacts: 'test/bigscan.sarif')
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
