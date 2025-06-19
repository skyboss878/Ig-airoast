from instagrapi import Client

USERNAME = "your_username"
PASSWORD = "your_password"

cl = Client()
cl.login(USERNAME, PASSWORD)

def send_roast(username, message):
    user_id = cl.user_id_from_username(username)
    cl.direct_send(message, [user_id])

# Example
send_roast("friend_username", "You have something on your chin... no, the third one down.")
