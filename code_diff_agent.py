import os
import subprocess

# --- CONFIG ---
MONITORED_PATHS = ["Dockerfile", "src/", "requirements.txt"]
BASE_COMMIT = os.getenv("BASE_COMMIT", "HEAD~1")  # fallback for GitHub Actions
CURRENT_COMMIT = "HEAD"


def get_changed_files(base_commit, current_commit):
    """Returns a list of changed files between two commits"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", base_commit, current_commit],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().splitlines()
        return files
    except subprocess.CalledProcessError as e:
        print("❌ Error running git diff:", e.stderr)
        return []


def is_relevant_change(files):
    """Check if any changed file is in the monitored paths"""
    for file in files:
        for path in MONITORED_PATHS:
            if file.startswith(path):
                return True
    return False


def main():
    changed_files = get_changed_files(BASE_COMMIT, CURRENT_COMMIT)

    print("📝 Changed Files:")
    for file in changed_files:
        print(f" - {file}")

    should_trigger = is_relevant_change(changed_files)

    with open("build_trigger", "w") as f:
        f.write("trigger=true" if should_trigger else "trigger=false")

    # Print to stdout for GitHub Actions output capture
    print(f"::set-output name=build_required::{str(should_trigger).lower()}")


if __name__ == "__main__":
    main()
