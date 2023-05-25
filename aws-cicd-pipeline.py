import boto3

def create_pipeline():
    # Create a CodePipeline client
    codepipeline = boto3.client('codepipeline', region_name='us-east-1')

    # Define the pipeline stages and actions
    pipeline_definition = {
        'name': 'MyPipeline',
        'roleArn': 'arn:aws:iam::016698473537:role/MyCodePipelineRole',
		'artifactStore': {
            'type': 'S3',
            'location': 'pipeline-bucket-sk'
        },
        'stages': [
            {
                'name': 'Source',
                'actions': [
                    {
                        'name': 'SourceAction',
                        'actionTypeId': {
                            'category': 'Source',
                            'owner': 'AWS',
                            'provider': 'CodeCommit',
                            'version': '1'
                        },
                        'configuration': {
                            'RepositoryName': 'my-repo',
                            'BranchName': 'main',
                        },
                        'outputArtifacts': [
                            {
                                'name': 'SourceOutput',
                            },
                        ],
                        'runOrder': 1
                    }
                ]
            },
            {
                'name': 'Build',
                'actions': [
                    {
                        'name': 'BuildAction',
                        'actionTypeId': {
                            'category': 'Build',
                            'owner': 'AWS',
                            'provider': 'CodeBuild',
                            'version': '1'
                        },
                        'configuration': {
                            'ProjectName': 'my-codebuild-project',
                        },
                        'inputArtifacts': [
                            {
                                'name': 'SourceOutput',
                            },
                        ],
                        'outputArtifacts': [
                            {
                                'name': 'BuildOutput',
                            },
                        ],
                        'runOrder': 1
                    }
                ]
            },
            {
                'name': 'Deploy',
                'actions': [
                    {
                        'name': 'DeployAction',
                        'actionTypeId': {
                            'category': 'Deploy',
                            'owner': 'AWS',
                            'provider': 'CloudFormation',
                            'version': '1'
                        },
                        'configuration': {
                            'StackName': 'my-stack',
                            'ActionMode': 'CREATE_UPDATE',
                            'Capabilities': 'CAPABILITY_NAMED_IAM',
                            'TemplatePath': 'BuildOutput::template.yaml',
                            'RoleArn': 'arn:aws:iam::016698473537:role/MyCodePipelineRole',
                        },
                        'inputArtifacts': [
                            {
                                'name': 'BuildOutput',
                            },
                        ],
                        'runOrder': 1
                    }
                ]
            }
        ]
    }

    # Create the pipeline
    response = codepipeline.create_pipeline(
        pipeline=pipeline_definition
    )

    print("Pipeline created successfully!")

# Call the create_pipeline function
create_pipeline()
