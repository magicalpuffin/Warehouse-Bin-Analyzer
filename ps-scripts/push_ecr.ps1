# Builds container and pushes image to AWS ECR

. ps-scripts/env.ps1

$ecrUri = "$($AWS_ACCOUNT_ID).dkr.ecr.$($AWS_REGION).amazonaws.com/$($ECR_REPO)"

# Build the Docker image
Write-Output "Docker Building: $($ecrUri):$($TAG)"
zappa save-python-settings-file dev
docker build --tag "$($ecrUri):$($TAG)" --label "$($IMAGE_LABEL)" --file docker/Dockerfile_dev .

# Remove previous image
Write-Output "Docker Removing Previous Image: $($ecrUri)"
docker image prune --force --filter "label=$($IMAGE_LABEL)"

# Authenticate to ECR using the AWS CLI
Write-Output "Authenticating Docker: $($ecrUri)"
aws ecr get-login-password | docker login --username AWS --password-stdin "$($ecrUri)"

# Push the Docker image to ECR
Write-Output "Docker Pushing: $($ecrUri):$($TAG)"
docker push "$($ecrUri):$($TAG)"