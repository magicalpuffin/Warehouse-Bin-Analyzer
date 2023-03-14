# Connects the AWS RDS instance with psql

# Note
# Login needs to be specified in env.ps1. Can log in as admin or other assigned user

. ps-scripts/env.ps1

cmd /c "psql --host=$($RDS_ENTRYPOINT) --port=$($RDS_PORT) --username=$($RDS_USERNAME) --password --dbname=$($RDS_DATABASE)"