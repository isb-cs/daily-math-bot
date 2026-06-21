import datetime
import os
import sys
import requests
import gdown

# 1. Map days of the week to your Google Drive File IDs
PROBLEMS = {
    "Monday": "1nCHma_8bXUj3Fq66uemUXDMjcUdWZF6O",
    "Tuesday": "19Y6PIyZxOjARBrZRZ3jAtoPThgqpKOPW",
    "Wednesday": "1uf0u-tlcl4oVu2dPFKo7enp6WiCygDGm",
    "Thursday": "1q7yPGHXqSbIWJxcuAP3z9Y2VzXcVF-yT",
    "Friday": "12abf69tKCpnIi66oFDJNxOhLLlOCvh2n",
    "Sunday": "1sZXTmCB1jYifPpg1NHtQDj9Nm49lwfPA",
}

SOLUTIONS = {
    "Monday": "190FeDwH1azMLPtvyH4wWLAiDt7v2iGSZ",
    "Tuesday": "1HLYFA9DJeKxOAI1JeaooIJb_c-f_-UPn",
    "Wednesday": "1weQ5R2dZptlXdbiMlYgfnSveQrcnAvzV",
    "Thursday": "1nC1yakba4qy6TAe0t260Rt_7KQ-Ng2wf",
    "Friday": "1jY_te4tGHm-eD39luAzagYqH9_kiceXf",
}
#    "Saturday": "1_YOUR_SAT_SOLUTION_ID_HERE",
#    "Sunday": "1_YOUR_SUN_SOLUTION_ID_HERE",

# 2. Grab the webhook URL from GitHub's secure secret vault
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def post_to_students(post_type):
    today = datetime.datetime.now().strftime("%A")
    
    if post_type == "morning":
        file_id = PROBLEMS.get(today)
        message = f"☀️ **Good morning!** Here is your {today} Math Challenge:"
    elif post_type == "evening":
        file_id = SOLUTIONS.get(today)
        message = f"🌙 **Evening!** Here is the solution for the {today} challenge:"
    else:
        print("Invalid post type specified.")
        return

    if not file_id or "YOUR_" in file_id:
        print(f"Skipping: No valid Google Drive ID configured for {today}.")
        return

    # Download from Google Drive
    drive_url = f"https://google.com{file_id}"
    local_filename = "temp_image.jpg"
    gdown.download(drive_url, local_filename, quiet=True)

    # Post text and image to Discord
    with open(local_filename, "rb") as image_file:
        payload = {"content": message}
        files = {"file": image_file}
        response = requests.post(WEBHOOK_URL, data=payload, files=files)
        
    os.remove(local_filename)
    
    if response.status_code == 200 or response.status_code == 204:
        print(f"Successfully posted {post_type} image for {today}!")
    else:
        print(f"Failed to post to Discord. Status code: {response.status_code}")

if __name__ == "__main__":
    # This reads the argument sent by our timer ('morning' or 'evening')
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        post_to_students(argument)
    else:
        print("Please provide an argument: 'morning' or 'evening'")
