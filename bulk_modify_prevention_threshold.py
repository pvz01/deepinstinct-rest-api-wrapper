# Example of how to modify a policy setting or set of setting in bulk, including
# an unlimited quantity of policies on 1 or more managenent servers, in a single
# script. On a multi-tenancy server, the scope of policies modified will depend
# upon the privileges of the API key(s) you provide in the server_list.

server_list = [

    {'fqdn': 'server1.customers.deepinstinctweb.com', 'key': 'alpha'},

    {'fqdn': 'server2.customers.deepinstinctweb.com', 'key': 'beta'},

    {'fqdn': 'server3.customers.deepinstinctweb.com', 'key': 'charlie'}

]


#import required libraries
import requests
import json

for server in servers:

    #define DI server config
    fqdn = server['fqdn']
    key = server['key']

    #get list of policies
    request_url = f'https://{fqdn}/api/v1/policies/'
    headers = {'accept': 'application/json', 'Authorization': key}
    response = requests.get(request_url, headers=headers)
    policies = response.json()

    for policy in policies:
        #for every Windows policy
        if policy['os'] == 'WINDOWS':
            #get policy data from server
            request_url = f'https://{fqdn}/api/v1/policies/{policy["id"]}/data'
            response = requests.get(request_url, headers=headers)
            policy_data = response.json()
            #modify policy data
            if policy_data['data']['prevention_level'] in ['HIGH', 'VERY_HIGH']:
                print(f"Modifying prevention_level setting from '{policy_data['data']['prevention_level']}' to 'MEDIUM' for MSP '{policy['msp_name']}' (ID {policy['msp_id']}) Policy '{policy['name']}' (ID {policy['id']})")
                policy_data['data']['prevention_level'] = 'MEDIUM'
                #save modified policy data to server
                response = requests.put(request_url, json=policy_data, headers=headers)
