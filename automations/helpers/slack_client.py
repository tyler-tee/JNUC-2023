import requests
from typing import List


class SlackClient:

    def __init__(self, token: str,
                 verify_cert: bool = True):

        self.base_url = "https://slack.com/api"
        self.session = requests.session()
        self.session.headers = {"Authorization": f"Bearer {token}",
                                "Content-Type": "application/json"}
        self.session.verify = verify_cert

    def send_message(self, channel_id: str,
                     attachments: List = None, text: str = None) -> bool:
        """
        Post a message to a Slack channel of your choosing.
        """

        payload = {"channel": channel_id}

        if attachments or text:
            payload["attachments"] = attachments if attachments else None
            payload["text"] = text if text else None
        else:
            print("Slack Error: Must provide text or attachments to send message.")
            return False

        response = self.session.post(f"{self.base_url}/chat.postMessage", json=payload)

        if response.status_code == 200 and response.json()['ok'] is True:
            return True
        else:
            print("Slack Error: ", response.status_code, response.json())
            return False

    def update_mesage(self, channel_id: str, timestamp: str,
                      attachments: List = None, text: str = None) -> bool:
        """
        Update a message posted to Slack.
        """

        payload = {"channel": channel_id,
                   "ts": timestamp}

        if attachments or text:
            payload["attachments"] = attachments if attachments else None
            payload["text"] = text if text else None
        else:
            print("Slack Error: Must provide text or attachments to update message.")
            return False

        response = self.session.post(f"{self.base_url}/chat.update", json=payload)

        if response.status_code == 200 and response.json()['ok'] is True:
            return True
        else:
            print("Slack Error: ", response.status_code, response.json())
            return False
