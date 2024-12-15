#!/bin/bash

# Start PostgreSQL
service postgresql start

# Wait for PostgreSQL to be ready (optional, for large databases)
sleep 5

# Initialize PostgreSQL database if not already initialized (optional)
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres';" || true
sudo -u postgres psql -c "CREATE DATABASE analytics;" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE analytics TO postgres;" || true

# Start the Flask application
python /run.py
