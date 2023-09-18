import os
from helpers import helpers
from helpers.slack_client import SlackClient
from helpers.jamf_client import JamfClient


def main():
    # Get our current location
    current_dir = os.path.dirname(__file__)

    # Load our settings
    config = helpers.load_config(f'{current_dir}/config.json')

    # Initialize instances of our helper clients
    jamf_client = JamfClient(config["jamf_user"], config["jamf_pass"],
                             config["jamf_server"])
    slack_client = SlackClient(config["slack_token"])

    jamf_client.authenticate()  # Authenticate to obtain a token

    # Sample Slack data you might receive
    slack_user = "UAO12345"
    slack_timestamp = "1687125073.075118"
    slack_action = "deploy_{APP_NAME_PLACEHOLDER}_{BUNDLE_ID_PLACEHOLDER}_{JAI_ID_PLACEHOLDER}"

    # Parse the Bundle ID, App Name, and App Installer ID from our received action
    jai_info = helpers.parse_jai_from_action(slack_action)
    jai_details = jamf_client.get_app_installer_details(jai_info["jai_id"])

    if slack_action.startswith('deploy_'):
        # Read in our App Installer suggestion template
        with open('./slack_templates/deploy.json') as f:
            template = f.read()

        # Update our template accordingly
        replacements = {
            "{APP_NAME_PLACEHOLDER}": jai_info["app_name"],
            "{USER_PLACEHOLDER}": slack_user,
            "{JAMF_SERVER_PLACEHOLDER}": config["jamf_server"]
        }
        message = helpers.parse_slack_template(template, replacements)

        # Report App Installer suggestion via Slack
        slack_client.update_mesage(config["slack_channel_id"],
                                   timestamp=slack_timestamp,
                                   attachments=message)

        # Check if our Smart Group already exists - Create it if it doesn't
        group_name = f"Patch Mgmt - {jai_info['app_name']}"
        group_response = jamf_client.get_computer_group(name=group_name)

        if 'Error' not in group_response:
            group_id = group_response['computer_group']['id']
        else:
            group_config = helpers.parse_group_xml('./smart_group.xml', group_name,
                                                   jai_info["bundle_id"])

            group_id = jamf_client.create_computer_group(group_config)['id']

        # Configure and deploy our App Installer
        jamf_client.deploy_app_installer(jai_info["app_name"], jai_info["jai_id"],
                                         group_id)

        # Add Patch Title Configuration
        patch_title = jamf_client.add_patch_title(jai_details["titleName"], jai_details["id"])

        # Add Patch Title to Jamf Dashboard
        jamf_client.add_patch_title_dashboard(patch_title["patch_software_title"]["id"])

    elif slack_action.startswith('ignore_'):
        # Read in our App Installer suggestion template
        with open('./slack_templates/ignore.json') as f:
            template = f.read()

        # Update our template accordingly
        replacements = {
            "{APP_NAME_PLACEHOLDER}": jai_info["app_name"],
            "{USER_PLACEHOLDER}": slack_user,
            "{JAMF_SERVER_PLACEHOLDER}": config["jamf_server"]
        }
        message = helpers.parse_slack_template(template, replacements)

        # Report App Installer suggestion via Slack
        slack_client.update_mesage(config["slack_channel_id"],
                                   timestamp=slack_timestamp,
                                   attachments=message)

    elif slack_action.startswith('postpone_'):
        # Read in our App Installer suggestion template
        with open('./slack_templates/postpone.json') as f:
            template = f.read()

        # Update our template accordingly
        replacements = {
            "{APP_NAME_PLACEHOLDER}": jai_info["app_name"],
            "{USER_PLACEHOLDER}": slack_user,
            "{JAMF_SERVER_PLACEHOLDER}": config["jamf_server"]
        }
        message = helpers.parse_slack_template(template, replacements)

        # Report App Installer suggestion via Slack
        slack_client.update_mesage(config["slack_channel_id"],
                                   timestamp=slack_timestamp,
                                   attachments=message)


if __name__ == '__main__':
    main()
