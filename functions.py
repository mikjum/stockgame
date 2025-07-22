import json
import subprocess

def load_data(DATA_FILE):
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"cash": 10000, "portfolio": {}}

def save_data(data, DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def git_commit_and_push(commit_message="Päivitetty käyttäjätieto"):
    subprocess.run(["git", "config", "--global", "user.email", "sinun@email.com"])
    subprocess.run(["git", "config", "--global", "user.name", "SinunGitHubNimi"])
    subprocess.run(["git", "add", str(DATA_FILE)])
    subprocess.run(["git", "commit", "-m", commit_message])
    
    github_token = os.getenv("GITHUB_TOKEN")
    repo_url = os.getenv("GITHUB_REPO_URL")
    if github_token and repo_url:
        push_url = repo_url.replace("https://", f"https://{github_token}@")
        subprocess.run(["git", "push", push_url])
    else:
        st.warning("GITHUB_TOKEN tai GITHUB_REPO_URL puuttuu!")

