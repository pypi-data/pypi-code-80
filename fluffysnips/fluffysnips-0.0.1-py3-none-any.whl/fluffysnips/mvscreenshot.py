from pathlib import Path
from datetime import datetime, timedelta
import sys


def pretty_delta(delta: timedelta):
    if delta.seconds < 0:
        return "in the future"
    elif delta.seconds < 120:
        return f"{delta.seconds} seconds ago"
    elif delta.seconds < 60 * 120:
        return f"{delta.seconds // 60} minutes ago"
    else:
        return f"{delta.seconds // (60 * 60)} hours ago"


def main():
    if len(sys.argv) < 2:
        print("Usage: mvscreenshot destination_name")
    destination = Path(sys.argv[1]).resolve()
    pictures_path = Path.home() / "Pictures"
    screenshots = list(pictures_path.glob("Screenshot from *.png"))
    screenshots.sort()
    last_screenshot = screenshots[-1]
    last_date = datetime.strptime(
        last_screenshot.name, "Screenshot from %Y-%m-%d %H-%M-%S.png"
    )
    now = datetime.now()
    delta = now - last_date
    delta_text = pretty_delta(delta)
    if destination.suffix != last_screenshot.suffix:
        destination = destination.with_suffix(last_screenshot.suffix)
    print(f"Screenshot from {delta_text}")
    print(f"Move to: {destination}")
    confirm = input("Confirm [Y/n]: ")
    if confirm.lower() in {"y", "yes", ""}:
        last_screenshot.rename(destination)


if __name__ == "__main__":
    main()
