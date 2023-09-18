import os
from helpers import helpers
from helpers.jamf_client import JamfClient
from helpers.slack_client import SlackClient


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

    # Get total systems registered with our Jamf instance
    system_count = len(jamf_client.get_jamf_systems()["computers"])

    # Retrieve all available App Installers and parse their bundle ID's
    all_jais = jamf_client.get_all_app_installers()
    all_bundle_ids = [jai["bundleId"] for jai in all_jais["results"]]

    # Retrieve all deployed App Installers and parse their bundle ID's
    deployed_jais = jamf_client.get_deployed_app_installers()
    deployed_jai_deets = [jamf_client.get_app_installer_details(jai["appTitleId"]) for jai in deployed_jais["results"]]
    deployed_bundle_ids = [jai["bundleId"] for jai in deployed_jai_deets]

    # Get rid of bundle ID's associated with deployed App Installers
    available_bundle_ids = [jai_id for jai_id in all_bundle_ids if jai_id not in deployed_bundle_ids]

    # Load a list of the installed applications in our environment
    app_installs_raw = jamf_client.get_computer_inventory(sections=['APPLICATIONS'])
    app_installs = helpers.parse_jamf_apps(app_installs_raw)

    # Get rid of any bundle ID's in our app inventory without an available App Installer
    eligible_installs = [jai_id for jai_id in app_installs if jai_id["app.bundleId"] in available_bundle_ids]

    # Find the installation prevalence of discovered applications
    for install in eligible_installs:
        install["install_prev"] = (install["count"]/system_count)

    # Filter out any install with an install prevalence less than our threshold
    applicable_jais = [install for install in eligible_installs
                       if install["install_prev"] >= config["install_threshold"]]
    print(applicable_jais)

    if applicable_jais:
        # Read in our App Installer suggestion template
        with open(f'{current_dir}/slack_templates/suggestion.json') as f:
            template = f.read()

        # Iterate over applicable App Installers and replace strings in our template as necessary
        for app in applicable_jais:
            replacements = {
                "{APP_NAME_PLACEHOLDER}": app["app.name"],
                "{BUNDLE_ID_PLACEHOLDER}": app["app.bundleId"],
                "{TOTAL_INSTALLS_PLACEHOLDER}": app["count"]
            }
            message = helpers.parse_slack_template(template, replacements)

            # Report App Installer suggestion via Slack
            slack_client.send_message(config["slack_channel_id"], attachments=message)

    return applicable_jais


if __name__ == '__main__':
    main()
