import requests
import argparse
import json

def fetch_github_activity(username, count=5):
    url = f"https://api.github.com/users/{username}/events"
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return

    events = response.json()
    return events[:count]
    
def display_activity(username, events):
    if not events:
        return
    
    for event in events:
        match event["type"]:
            case "PushEvent":
                print(f"Pushed to {event['repo']['name']} at {event['created_at']}")
            case "CreateEvent":
                print(f"Created {event['payload']['ref_type']} {event['payload']['ref']} at {event['repo']['name']} at {event['created_at']}")
            case "DeleteEvent":
                print(f"Deleted {event['payload']['ref_type']} {event['payload']['ref']} at {event['repo']['name']} at {event['created_at']}")
            case "WatchEvent":
                print(f"Starred {event['repo']['name']} at {event['created_at']}")
            case "IssuesEvent":
                print(f"{event['payload']['action']} issue #{event['payload']['issue']['number']} at {event['repo']['name']} at {event['created_at']}")
            case "IssueCommentEvent":
                print(f"{event['payload']['action']} comment on issue #{event['payload']['issue']['number']} at {event['repo']['name']} at {event['created_at']}")
            case "PullRequestEvent":
                print(f"{event['payload']['action']} pull request #{event['payload']['number']} at {event['repo']['name']} at {event['created_at']}")
            case "ForkEvent":
                print(f"Forked {event['repo']['name']} at {event['created_at']}")
            case "ReleaseEvent":
                print(f"Released {event['payload']['release']['tag_name']} at {event['repo']['name']} at {event['created_at']}")
            case "PublicEvent":
                print(f"Made {event['repo']['name']} public at {event['created_at']}")
            case _:
                print(f"Unknown event type: {event['type']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch recent GitHub activity for a user")
    parser.add_argument("username", help="The GitHub username to fetch activity for")
    parser.add_argument("-c", "--count", type=int, default=5, help="Number of recent activities to fetch")
    args = parser.parse_args()

    events = fetch_github_activity(args.username, args.count)
    display_activity(args.username, events)