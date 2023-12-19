#!/bin/sh

vault_path="/opt/vault"
if ! [ -d "$vault_path" ]; then
#installing vault for Ubuntu
    curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
    sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
    sudo apt-get update && sudo apt-get install vault
fi


export VAULT_ADDR='https://vault.<domain>.com'
export QUALYS_API_USERNAME="$(vault kv get -field=QUALYS_API_USERNAME secret/to/path/qualys)"
export QUALYS_API_PASSWORD="$(vault kv get -field=QUALYS_API_PASSWORD secret/to/path/qualys)"

python3 qualys_API.py
