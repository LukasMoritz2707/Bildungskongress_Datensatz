import os

FOLDER_NAME = "Google"

os.mkdir(f"{FOLDER_NAME}")

for folders in ["Gemini", "ChatGPT", "DeepSeek"]:
    folder = f"{FOLDER_NAME}/{folders}"
    os.mkdir(folder)
    for i in range(0,20):
        with open(f"{folder}/{i}.json", "w") as f:
            pass