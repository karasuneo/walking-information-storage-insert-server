#!/bin/sh

# Export environment variables
export DB_HOST=${DB_HOST}
export DB_PORT=${DB_PORT}
export DB_NAME=${DB_NAME}
export DB_USER=${DB_USER}
export DB_PASSWORD=${DB_PASSWORD}

# Create schemaspy.properties from template
envsubst </schemaspy.properties.template >/schemaspy.properties

cat /schemaspy.properties

# Run SchemaSpy
java -jar /schemaspy.jar
