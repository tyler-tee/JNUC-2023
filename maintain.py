import os
from helpers import helpers
from helpers.jamf_client import JamfClient


def main():
    # Get our current location
    current_dir = os.path.dirname(__file__)

    # Load our settings
    config = helpers.load_config(f'{current_dir}/config.json')

    # Initialize instance of JamfClient
    jamf_client = JamfClient(config["jamf_user"], config["jamf_pass"],
                             config["jamf_server"])

    jamf_client.authenticate()  # Authenticate to obtain a token

    # Retrieve all deployed App Installers and parse their bundle ID's
    deployed_jais = jamf_client.get_deployed_app_installers()

    # Iterate over deployed App Installers
    for deployment in deployed_jais:
        deployment_details = jamf_client.get_deployment_details(deployment['id'])

    # If failures are noted in a deployment, send a 'Retry All' command
        if deployment_details['failed'] != 0:
            jamf_client.retry_failed_deployment(deployment['id'])


if __name__ == '__main__':
    main()
