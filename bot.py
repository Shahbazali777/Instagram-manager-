import os
import time
from instagrapi import Client

def load_credentials():
    print("--- Instagram Welcome Bot Setup ---")
    # Agar user ne pehle se username setup nahi kiya to script input mangegi
    username = input("Enter your Instagram Username: ").strip()
    password = input("Enter your Instagram Password: ").strip()
    return username, password

def main():
    # 1. Setup Phase
    username, password = load_credentials()
    
    cl = Client()
    print("\nLoggin in... Please wait...")
    
    try:
        cl.login(username, password)
        print("\n[+] BOT ACTIVE OK! Chat script is running successfully.")
    except Exception as e:
        print(f"\n[-] Login Failed: {e}")
        return

    # Welcome Message Configuration
    WELCOME_MESSAGE = "Assalam-o-Alaikum! Welcome to our page. Thank you for following us! 😊"
    
    # Pehle se majood followers ki list le rahe hain taake unhe dobara msg na jaye
    print("Fetching current followers...")
    try:
        user_id = cl.user_id_from_username(username)
        processed_followers = set(cl.user_followers(user_id).keys())
    except Exception as e:
        print(f"Error fetching followers: {e}")
        processed_followers = set()

    print("\n[✔] Monitoring new followers 24/7...")
    
    # 2. 24 Hours Active Loop
    while True:
        try:
            # New followers check karein
            current_followers = set(cl.user_followers(user_id).keys())
            new_followers = current_followers - processed_followers

            for follower_id in new_followers:
                # New follower ko message bhejein
                cl.direct_send(WELCOME_MESSAGE, user_ids=[follower_id])
                print(f"[+] Welcome message sent to user ID: {follower_id}")
                processed_followers.add(follower_id)
                time.sleep(5) # Rate limit se bachne ke liye gap
                
        except Exception as e:
            print(f"Error in loop: {e}")
            # Agar Instagram temporary block kare to login refresh karne ki koshish karein
            try:
                cl.login(username, password)
            except:
                pass
        
        # Har 5 minute baad check karega (Instagram safety ke liye)
        time.sleep(300) 

if __name__ == "__main__":
    main()
