import os
import time
from instagrapi import Client

def load_credentials():
    print("--- Instagram Welcome Bot Setup ---")
    # Script start hote hi sabse pehle username aur password mangegi
    username = input("Enter your Instagram Username: ").strip()
    password = input("Enter your Instagram Password: ").strip()
    return username, password

def send_self_dm(cl, username, message):
    """Apne hi account (Self DM) me confirmation message bhejne ke liye"""
    try:
        self_id = cl.user_id_from_username(username)
        cl.direct_send(message, user_ids=[self_id])
        print(f"[✔] Notification sent to self DM: {message}")
    except Exception as e:
        print(f"[-] Could not send self DM: {e}")

def main():
    # Credentials input lena
    username, password = load_credentials()
    cl = Client()
    
    # Session file taake baar baar login credentials send na karne paren (Safety feature)
    session_file = f"{username}_session.json"
    
    processed_followers = set()
    user_id = None
    is_first_run = True

    print("\n[★] Bot Started. Monitoring connection 24/7...")

    # Infinite Loop: Jo script ko kabhi band nahi hone degi (24 Hours Active)
    while True:
        try:
            # 1. Reconnect & Login Check
            if not cl.get_settings() or not user_id:
                print("\n[..] Connecting/Reconnecting to Instagram...")
                
                # Agar pehle se session save hai to us se login karega
                if os.path.exists(session_file):
                    try:
                        cl.load_settings(session_file)
                        cl.login(username, password)
                    except:
                        cl.login(username, password)
                        cl.dump_settings(session_file)
                else:
                    cl.login(username, password)
                    cl.dump_settings(session_file)
                
                user_id = cl.user_id_from_username(username)
                print("[+] Connection Successful!")
                
                # Connection active hote hi aapko apne inbox me msg aayega
                send_self_dm(cl, username, "🤖 [Bot Active OK] Connection restored and bot is working smoothly!")

                # Pehli baar run hone par mojooda followers ko safe list me dalna
                if is_first_run:
                    print("Fetching current followers list...")
                    try:
                        processed_followers = set(cl.user_followers(user_id).keys())
                        is_first_run = False
                        print(f"[+] Loaded {len(processed_followers)} existing followers. Monitoring for new ones...")
                    except Exception as e:
                        print(f"Error fetching followers: {e}")

            # 2. Automatically Welcome New Members
            print("Checking for new followers...")
            current_followers = set(cl.user_followers(user_id).keys())
            new_followers = current_followers - processed_followers

            for follower_id in new_followers:
                # Welcome Message text
                WELCOME_MESSAGE = "Assalam-o-Alaikum! Welcome to our page. Thank you for following us! 😊"
                
                cl.direct_send(WELCOME_MESSAGE, user_ids=[follower_id])
                print(f"[+] Welcome message sent to follower ID: {follower_id}")
                processed_followers.add(follower_id)
                time.sleep(5) # Rate limit / Anti-ban safety gap

            # Har 5 minute (300 seconds) baad dobara check karega
            time.sleep(300)

        except Exception as e:
            # Agar internet down ho ya Instagram temporary logout kare to script crash nahi hogi
            print(f"\n[⚠️] Connection Lost or Error: {e}")
            print("[🔄] Retrying automatically in 1 minute... Please don't close.")
            
            user_id = None 
            time.sleep(60) # 1 minute wait karne ke baad loop dobara check karegi

if __name__ == "__main__":
    main()
