import json
from typing import List, Dict


def load_config(config_json: str) -> Dict:
    with open(config_json) as f:
        config = json.load(f)

    return config


def load_applications(apps_json):
    with open(apps_json) as f:
        app_installs = json.load(f)

    return app_installs


def parse_jamf_apps(installed_apps: List) -> Dict:
    bundle_dict = {}

    for record in installed_apps:
        for app in record['applications']:
            if app['bundleId'] in bundle_dict.keys():
                bundle_dict[app['bundleId']]['count'] += 1
            else:
                bundle_dict[app['bundleId']] = {"count": 1, "app_name": app['name']}

    installed_app_lst = [{"app.bundleId": key,
                          "app.name": bundle_dict[key]['app_name'],
                          "count": bundle_dict[key]['count']} for key in bundle_dict.keys()]

    return installed_app_lst


def parse_group_xml(xml_file: str, smart_group_name: str, bundle_id: str) -> str:
    with open(xml_file) as f:
        smart_group_config_template = f.read()

    smart_group_config = smart_group_config_template.replace('{NAME_PLACEHOLDER}', smart_group_name)
    smart_group_config = smart_group_config.replace('{BUNDLE_ID_PLACEHOLDER}', bundle_id)

    return smart_group_config


def parse_slack_template(template: str, replacement_dict: Dict) -> List:
    for key, value in replacement_dict.items():
        template = template.replace(key, str(value))

    template_parsed = json.loads(template)

    return template_parsed


def parse_jai_from_action(slack_action: str) -> Dict:
    raw_info = slack_action.split("_")

    jai_summary = {
        "app_name": raw_info[1],
        "bundle_id": raw_info[2],
        "jai_id": raw_info[3]
    }

    return jai_summary
