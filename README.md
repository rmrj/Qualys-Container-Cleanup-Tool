# Qualys Container Cleanup Tool

## Overview
This script automates the process of deleting stale data (DELETED and STOPPED containers) in the Qualys portal using the Delete Container Security API. 

## Features
- Utilizes the Qualys API to remove stale container data.
- Supports deletion of both DELETED and STOPPED container states.

## Requirements
- Python 3.x
- `requests` library
- `yaml` library

## Setup
1. Install required Python libraries:
   ```bash
   pip install requests pyyaml
## Set up the required environment variables:
export QUALYS_API_USERNAME='your_username'

export QUALYS_API_PASSWORD='your_password'
