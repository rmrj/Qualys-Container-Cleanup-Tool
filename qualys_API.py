#!/usr/bin/env python
#
# Author: Rama Raju Konuganti
# Purpose: To delete the stale data(DELETED and STOPPED containers) in Qualys portal using Delete Container Security API.
# version: 1.0
# date: 07.12.2022
from __future__ import print_function
from builtins import str
import sys, requests, os, logging
import yaml
import base64
import logging.config
#import os.path
from os import path
#import snoop

# setup_http_session sets up global http session variable for HTTP connection sharing
def setup_http_session():
    global httpSession

    httpSession = requests.Session()

# setup_credentials builds HTTP auth string and base64 encodes it to minimize recalculation
def setup_credentials(username, password, URL):
    global token

    authURL = URL + "/auth"
    usrPass = str(username)+':'+str(password)
    usrPassBytes = bytes(usrPass, "utf-8")
    httpCredentials = base64.b64encode(usrPassBytes).decode("utf-8")
    authBody = "username="+ str(username) + "&password=" + str(password) + "&token=true&permissions=true"

    authHeader = {"Content-Type": "application/x-www-form-urlencoded"}
    response=httpSession.post(authURL, headers=authHeader, data=authBody, verify=True)
    token = response.text
    #print("Token = {}".format(str(token)))

#logging setup
def setup_logging(default_path='./config/logging.yml',default_level=logging.INFO,env_key='LOG_CFG'):
    """Setup logging configuration"""
    if not os.path.exists("log"):
        os.makedirs("log")
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# Called to read in ./config.yml
#@snoop
def config():
    with open('config.yml', 'r') as config_settings:
        config_info = yaml.load(config_settings, Loader=yaml.SafeLoader)
        try:
            username = os.environ["QUALYS_API_USERNAME"]
            #password = base64.b64decode(os.environ["QUALYS_API_PASSWORD"])
            password = os.environ["QUALYS_API_PASSWORD"]
        except KeyError as e:
            logger.critical("Critical Env Variable Key Error - missing configuration item {0}".format(str(e)))
            logger.critical("Please review README for required configuration to run script")
            sys.exit(1)
        try:
            threadCount = str(config_info['defaults']['threadCount']).rstrip()
            URL = str(config_info['defaults']['apiURL']).rstrip()
            if "pageSize" in config_info['defaults']:
                pageSize = config_info['defaults']['pageSize']
            else:
                pageSize = 50

            if "exitOnError" in config_info['defaults']:
                exitOnError = config_info['defaults']['exitOnError']
            else:
                exitOnError = True
        except KeyError as e:
            logger.critical("Critical ./config.yml Key Error - missing configuration item {0}".format(str(e)))
            logger.critical("Please review README for required configuration to run script")
            sys.exit(1)
        if URL == "<QUALYS_API_URL>":
            logger.critical("Critical ./config.yml Key Error - missing configuration item Qualys API URL")
            logger.critical("Please check for https://www.qualys.com/docs/qualys-container-security-api-guide.pdf for the correct Qualys API URL for your subscription")
            logger.critical("Please review README for required configuration to run script")
            sys.exit(1)
        if username == '' or password == '' or URL == '':
            logger.critical("Config information in ./config.yml not configured correctly. Exiting...")
            sys.exit(1)
    return username, password, URL, pageSize, exitOnError, threadCount

# Delete call to API to execute the delete_containers function and return status code
def Delete_Call(token,URL):

    headers = {
        'Accept': '*/*',
        'content-type': 'application/json',
        'Authorization': "Bearer %s" % token
    }

    r = requests.delete(URL, headers=headers, verify=True)
    logger.debug("Repsonse code for GET to {0} - Response Code {1}".format(str(URL),str(r.status_code)))
    logger.debug("API Data for Response \n {}".format(str(r.text[:10000])))

    return r.status_code


#calling the delete API to remove deleted and stopped containers from Qualya portal 
def delete_containers():
    username, password, URL, pageSize, exitOnError, threadCount = config() 
    setup_credentials(username, password, URL) 
    delete_deleted_containers_URL = URL + "/csapi/v1.3/containers?filter=state%3ADELETED"
    delete_stopped_containers_URL = URL + "/csapi/v1.3/containers?filter=state%3ASTOPPED"
    Delete_Call(token,delete_deleted_containers_URL)
    Delete_Call(token,delete_stopped_containers_URL)

if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)
    setup_http_session()
    delete_containers()
