from instagrapi import Client
import openai
import moviepy.editor as mp
from datetime import datetime
from dotenv import load_dotenv
import time, os

# 🔐 Load environment variables
load_dotenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📲 Login to Instagram
cl = Client()
cl.login(USERNAME, PASSWORD)

# 🧠 AI + Video
def generate_roast_video():
    roast = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Give me a short, funny roast"}]
    )["choices"][0]["message"]["content"]

    clip = mp.VideoFileClip("base.mp4")
    txt = mp.TextClip(roast, fontsize=36, color='white', size=clip.size, bg_color='black')
    txt = txt.set_duration(clip.duration).set_position("center")
    final = mp.CompositeVideoClip([clip, txt])
    filename = f"roast_{int(time.time())}.mp4"
    final.write_videofile(filename, fps=24, codec="libx264")
    return filename

# 🔁 Main loop
last_seen = {}

def check_dms():
    threads = cl.direct_threads()
    for thread in threads:
        user = thread.users[0]
        user_id = user.pk
        messages = cl.direct_messages(thread.id)

        for msg in messages[::-1]:  # Oldest first
            if msg.id in last_seen.get(user_id, []):
                continue

            if "roast me" in msg.text.lower():
                cl.direct_send(
                    "🔥 Want a custom roast? Send $3 to PayPal.me/yourlink and DM 'paid' when done.",
                    [user_id]
                )
            elif "paid" in msg.text.lower():
                cl.direct_send("🔥 Generating your roast...", [user_id])
                roast_video = generate_roast_video()
                cl.direct_send_video(roast_video, [user_id])

            last_seen.setdefault(user_id, []).append(msg.id)

# 🏃 Run the bot
while True:
    try:
        check_dms()
        time.sleep(30)
    except Exception as e:
        print("Error:", e)
