#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import base64
from AnsiblePlaybook import RunPlaybook


def gen_ssh_key(ssh_key_file):
    ansible_ssh_key_raw = os.environ["ANSIBLE_SSH_KEY"]
    ansible_ssh_key = base64.b64decode(ansible_ssh_key_raw)
    with open(ssh_key_file, 'w') as f:
        f.write(ansible_ssh_key)
    return ssh_key_file

def machine_init(machine, fleet_id):
    if type(machine) is str:
        inventory = machine + ","
    if type(machine) is list:
        inventory = ",".join(machine) + ","

    ansible = RunPlaybook(private_key_file=gen_ssh_key("ssh_key.pem"))
    ansible.run(
        inventory=inventory,
        playbook_path=["playbooks/server_init.yml",],)
    return result

def main_handler(event, content):
    print('Event Content {}'.format(json.dumps(event)))

    # Check where the request came from
    if "requestContext" not in event.keys():
        return {"errorCode": 410, "errorMsg":"event is not come from api gateway"}

    # Check if the request is valid
    if event["requestContext"]["path"] != "/gameserver"
        return {"errorCode": 411, "errorMsg":"request is not from setting api path"}

        try:
            body = json.loads(event["body"])
            machine = body["machine"]
            fleet_id = body["fleet_id"]
        except Exception as e:
            print("Failed to parse the body: {}".format(event["body"]))
            return {"errorCode": 413, "errorMsg":"request is not correctly execute"}
        machine_init_result = machine_init(machine=machine, fleet_id=fleet_id)

    return {"errorCode": 413, "errorMsg":"request is not correctly execute"}
