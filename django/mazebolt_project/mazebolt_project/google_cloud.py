#!/usr/bin/python3

import os

# mb-exam-4
V1_BASE_URL = 'https://www.googleapis.com/compute/v1/projects/mbexam-4'
print('!!!!!!!!!!!!',os.path.dirname(__file__))
#google_key_file = os.path.dirname(__file__) + "/mbexam-4-688583a9e212.p12"
google_key_file = '//mazebolt_project/django/mazebolt_project/mazebolt_project' + "/mbexam-4-688583a9e212.p12" 
client_email = 'mb-exam-4@mbexam-4.iam.gserviceaccount.com'
base_image_name = V1_BASE_URL + '/global/images/attacker'


def get_access_credentials():
    from oauth2client.service_account import ServiceAccountCredentials

    credentials = ServiceAccountCredentials.from_p12_keyfile(client_email, google_key_file,
                                                             scopes=['https://www.googleapis.com/auth/compute'])

    return credentials


def create_instance(instance_name, image_name, size, rc='europe-west1-b'):
    import json
    import requests

    url = V1_BASE_URL + '/zones/%s/instances' % rc
    token = get_access_credentials().get_access_token().access_token
    headers = {'Authorization': 'Bearer %s' % token, 'content-type': "application/json"}
    params = {
        'name': instance_name,
        'machineType': "zones/%s/machineTypes/%s" % (rc, size),
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': image_name,
                }
            },
        ],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        'scheduling': {'preemptible': False},
    }

    r = requests.post(url, data=json.dumps(params), headers=headers)
    if int(r.status_code) != 200:
        raise Exception("Google: Unable to create instance in %s. %s" % (str(rc), str(r.__dict__)))

    res = r.json()
    return res


def list_instances():
    import requests
    url = V1_BASE_URL + '/aggregated/instances'
    token = get_access_credentials().get_access_token().access_token
    headers = {'Authorization': 'Bearer %s' % token, 'content-type': "application/json"}

    r = requests.get(url, headers=headers, params={})
    if int(r.status_code) != 200:
        raise Exception("Google: Unable to list instances. %s" % str(r.__dict__))
    res = r.json()

    instances = []
    for zone, data in res['items'].items():
        if 'instances' in data:
            for i in data['instances']:
                instances.append(i)

    return instances


def delete_instance(instance_name, rc='europe-west1-b'):
    import json
    import requests
    url = V1_BASE_URL + '/zones/%s/instances/%s' % (rc, instance_name)
    token = get_access_credentials().get_access_token().access_token
    headers = {'Authorization': 'Bearer %s' % token, 'content-type': "application/json"}

    r = requests.delete(url, headers=headers)
    if int(r.status_code) != 200:
        raise Exception("Google: Unable to delete instance in %s. %s" % (str(rc), str(r.__dict__)))

    res = r.json()
    return res


if __name__ == "__main__":
    import argparse
    arg_parser = argparse.ArgumentParser(description="Minimal Google Compute CLI")
    arg_parser.add_argument('command', help='Command: list|create|delete.')
    arg_parser.add_argument('-i', '--instance-name', help='Instance name for delete command.', default=None)
    args = arg_parser.parse_args()

    if args.command == 'list':
        print("List:")
        for instance in list_instances():
            print("")
            print(instance)
            print("")

    elif args.command == 'create':
        import uuid
        instance_name = 'mbexam-' + str(uuid.uuid4())

        print("Creating", instance_name)
        res = create_instance(instance_name=instance_name, image_name=base_image_name, size='n1-highcpu-2')
        print("Operation Result:", res)

    elif args.command == 'delete':
        print("Deleting %s:" % str(args.instance_name))
        res = delete_instance(args.instance_name)
        print("Operation Result:", res)

    else:
        raise Exception("Illegal Command '%s'" % args.command)

