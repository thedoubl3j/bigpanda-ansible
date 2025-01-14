#!/usr/bin/env python3

import requests
from requests import HTTPError

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            environment_id=dict(type='str', required=True),
            incident_id=dict(type='str', required=True),
            api_token=dict(type='str', required=True),
            source_incidents=dict(type='list', required=True),
            comment=dict(type='str', required=False)
        ),
        supports_check_mode=True
    )

    environment_id = module.params['environment_id']
    incident_id = module.params['incident_id']
    api_token = module.params['api_token']
    source_incidents = module.params['source_incidents']
    comment = module.params['comment']

    # Set the request headers
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }

    json_data = {
        'source_incidents': source_incidents,
        'comment': comment
    }

    try:
        response = requests.post(
            f'https://api.bigpanda.io/resources/v2.0/environments/{environment_id}/incidents/{incident_id}/merge',
            headers=headers,
            json=json_data
        )

        response.raise_for_status()
        module.exit_json(changed=True, result=response.text)
    except HTTPError as e:
        # Log any HTTP errors
        module.fail_json(msg=f"An HTTP error occurred: {str(e)}")


if __name__ == '__main__':
    main()
