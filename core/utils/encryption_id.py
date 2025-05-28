import base64


class PollLinkGenerator:
    def __init__(self, bot_name):
        self.bot_name = bot_name
    def _encrypt_id(self, user_id):

        user_id_bytes = str(user_id).encode('utf-8')
        encrypted_bytes = base64.urlsafe_b64encode(user_id_bytes)
        return encrypted_bytes.decode('utf-8')

    def generate_link(self, user_id):

        encrypted_id = self._encrypt_id(user_id)
        poll_link = f"https://t.me/{self.bot_name}?start={encrypted_id}"
        return poll_link