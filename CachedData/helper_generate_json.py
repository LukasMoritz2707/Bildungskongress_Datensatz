FOLDER_NAME = "Sex_ZeroShot"

for folders in ["Gemini", "ChatGPT", "Grok", "DeepSeek"]:
    folder = f"{FOLDER_NAME}/{folders}"
    for i in range(0,20):
        with open(f"{folder}/{i}.json", "w") as f:
            pass