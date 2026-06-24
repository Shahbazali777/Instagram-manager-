import os
import time
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

# ⚙️ CONFIGURATION
USERNAME = "YOUR_INSTAGRAM_USERNAME"
PASSWORD = "YOUR_INSTAGRAM_PASSWORD"
SESSION_FILE = "instagram_session.json"

cl = Client()

def login_and_connect():
    print("📡 Initializing Instagram Connection Module...")
    if os.path.exists(SESSION_FILE):
        try:
            print("🔄 Loading existing session...")
            cl.load_settings(SESSION_FILE)
            cl.login(USERNAME, PASSWORD)
            print("✅ Connected successfully via saved session!")
            return True
        except Exception as e:
            print("⚠️ Session expired. Attempting fresh login...")
            
    try:
        print(f"🔐 Logging in as {USERNAME}...")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("✅ Fresh login successful! Session saved.")
        return True
    except Exception as e:
        print(f"❌ Login Failed: {e}")
        return False

def send_self_success_msg():
    try:
        my_id = cl.user_id_from_username(USERNAME)
        success_text = (
            "🎉 *Bot Connect Success!*\n\n"
            "Aapka Instagram bot active ho chuka hai.\n\n"
            "💡 Commands dekhne ke liye DM mein *.allcmd* likhein."
        )
        cl.direct_send(success_text, user_ids=[my_id])
        print("📨 Success notification sent to your DM!")
    except Exception as e:
        print(f"⚠️ Could not send self-message: {e}")

def listen_messages():
    print("🤖 Bot is now listening to DMs & Groups... (Press Ctrl+C to stop)")
    seen_message_ids = set()

    while True:
        try:
            threads = cl.direct_threads(amount=10)
            
            for thread in threads:
                messages = thread.messages
                if not messages:
                    continue
                    
                last_msg = messages[0]
                
                # 👥 FEATURE: WELCOME NEW MEMBER IN GROUP CHAT
                # Agar group chat mein koi naya member join karta hai ya add hota hai
                if thread.is_group and last_msg.item_type == 'action_log':
                    if last_msg.id not in seen_message_ids:
                        seen_message_ids.add(last_msg.id)
                        
                        # Action log check karna ke kya koi add hua hai
                        action_text = getattr(last_msg, 'text', '')
                        if "added" in action_text.lower() or "joined" in action_text.lower():
                            welcome_msg = (
                                "👋 *Welcome to the Group!*\n\n"
                                "Gup-shup mein khushamdeed! Umeed hai aapka waqt accha guzrega.\n"
                                "💡 Is bot ki commands dekhne ke liye chat mein *.allcmd* likhein."
                            )
                            cl.direct_send(welcome_msg, thread_id=thread.id)
                            print(f"✨ Group mein naye member ko welcome kar diya: Thread {thread.id}")
                            continue

                # Normal messages handling
                if last_msg.user_id == cl.user_id or last_msg.id in seen_message_ids:
                    continue
                    
                seen_message_ids.add(last_msg.id)
                body = last_msg.text.lower().strip() if last_msg.text else ""
                thread_id = thread.id

                # 📜 .allcmd COMMAND
                if body == ".allcmd":
                    cmd_list = (
                        "╔════════════════════════╗\n"
                        "║      ⚙️ BOT COMMANDS LIST ⚙️     ║\n"
                        "╚════════════════════════╝\n\n"
                        "📌 1.  .ping\n"
                        "◽ Work: Bot ka active status check karta hai.\n"
                        "◽ Response: Pong!\n\n"
                        "📌 2.  .allcmd\n"
                        "◽ Work: Bot ki tamam available commands ki list detail ke sath show karta hai.\n\n"
                        "📌 3.  Auto Welcome\n"
                        "◽ Work: Group chat mein naye aane wale member ko automatic welcome message bhejta hai.\n\n"
                        "─────────────────────────\n"
                        "🤖 Termux Automated Instagram Bot v1.1"
                    )
                    cl.direct_send(cmd_list, thread_id=thread_id)

                # 👋 .ping COMMAND
                elif body == ".ping":
                    cl.direct_send("🏓 Pong! Instagram bot completely active hai.", thread_id=thread_id)

            time.sleep(5)

        except LoginRequired:
            print("📡 Connection lost. Re-authenticating...")
            if not login_and_connect():
                time.sleep(10)
        except Exception as e:
            print(f"⚠️ Error in loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if USERNAME == "YOUR_INSTAGRAM_USERNAME":
        print("❌ Error: Pehle code ke top par apna Instagram Username aur Password likhein!")
    else:
        if login_and_connect():
            send_self_success_msg()
            listen_messages()
