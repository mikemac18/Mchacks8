# import the random library to help us generate the random numbers
import random

# Create the CoinBot Class
class ManagerBot:

    # Create a constant that contains the default text for the message
    ADD_ME = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Sure! Let me add that real quick....\n\n"
            ),
        },
    }

    # The constructor for the class. It takes the channel name as the a
    # parameter and then sets it as an instance variable
    def __init__(self, channel):
        self.channel = channel

    # Generate a random number to simulate flipping a coin. Then return the
    # crafted slack payload with the coin flip message.
    def _add_nums(self):
        results = "1 + 1 = 2"

        text = f"The result is {results}"

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self):
        return {
            "channel": self.channel,
            "blocks": [
                self.ADD_ME,
                *self._add_nums(),
            ],
        }