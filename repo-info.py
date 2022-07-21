import json
import os
import requests
import sys
import time
import toml


def get_config(toml_file=None):
    if toml_file is None:
        toml_file = os.path.join(os.path.dirname(__file__), "pyproject.toml")

    return toml.load(toml_file).get(
        "repo-info",
        {},
    )


def get_token(toml_file):
    return toml.load(toml_file)


def get_repo_info(user, repo, headers):
    url = f"https://api.github.com/repos/{user}/{repo}"
    res = requests.get(url, headers=headers)
    data = res.json()
    info = {}
    for k in ["name", "full_name", "html_url", "description", "size", "pushed_at"]:
        info[k] = data[k]
    return info


def get_languages(user, repo, headers):
    url = f"https://api.github.com/repos/{user}/{repo}/languages"
    res = requests.get(url, headers=headers)
    return list(res.json().keys())


def get_merged_list(user, repo, headers):
    url = f"https://api.github.com/repos/{user}/{repo}/pulls?state=closed"
    res = requests.get(url, headers=headers)
    data = res.json()

    merged_list = []
    for item in data:
        if "merged_at" not in item:
            continue

        if item["user"]["login"] != user:
            continue

        info = {}
        for k in ["html_url", "title", "state", "body", "created_at", "merged_at", "closed_at"]:
            info[k] = item[k]

        info["user"] = item["user"]["login"]
        merged_list.append(info)

    return merged_list


def sleep(sec, msg):
    print(f"{msg}: waiting {sec}sec ...", file=sys.stderr)
    time.sleep(sec)


def main():
    config = get_config()

    token = get_token(config["token_file"])
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"token {token['access_token']}"}

    user = token["user_name"]
    interval = config["api_interval"]
    repo_info = {}
    for target in config["targets"]:
        name = target["name"]
        repo_info[name] = []

        for repo in target["repos"]:
            print(f"{repo}:", file=sys.stderr)
            sleep(interval, "    get_repo_info")
            info = get_repo_info(user, repo, headers)
            sleep(interval, "    get_languages")
            langs = get_languages(user, repo, headers)
            sleep(interval, "    get_merged_list")
            merged_list = get_merged_list(user, repo, headers)
            info["project_type"] = name
            info["langs"] = langs
            info["merged"] = merged_list
            repo_info[name].append(info)

    for k, v in repo_info.items():
        sorted_v = sorted(v, key=lambda i: i["pushed_at"], reverse=True)
        repo_info[k] = sorted_v

    print(json.dumps(repo_info, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
