import argparse
import copy
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
    try:
        for k in ["name", "full_name", "html_url", "description", "size", "pushed_at"]:
            info[k] = data[k]
    except KeyError:
        print("ERROR get_repo_info: ", repo, data)
        raise
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


def save_repoinfo(output_dir, info):
    fm = {}
    fm["title"] = info["name"]
    fm["date"] = info["pushed_at"]
    fm["draft"] = False
    fm["repo"] = info
    file_name = fm["title"].replace("-", "_") + ".md"
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, "w") as f:
        print(f"  {output_path}...")
        json.dump(fm, f, indent=4)


def save_repolist(content_dir, repo_list):
    abs_content_dir = os.path.abspath(os.path.expanduser(content_dir))
    if not os.path.isdir(abs_content_dir):
        raise FileNotFoundError(f"指定されたディレクトリが存在しません: {abs_content_dir}")

    for key, values in repo_list.items():
        output_dir = os.path.join(abs_content_dir, key)
        print(f"save repolist {output_dir}...")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for repoinfo in values:
            save_repoinfo(output_dir, repoinfo)




def main():
    parser = argparse.ArgumentParser(description="GitHubリポジトリの情報を取得する")
    parser.add_argument("--content-dir", type=str,
                        help="出力するHugoのコンテントディレクトリのパス。未指定時は設定ファイルに定義された`content_dir`の値が使用される。")
    parser.add_argument("--config", type=str, help="設定ファイルのパス")

    args = parser.parse_args()
    print(args)

    config = get_config(args.config)
    token = get_token(config["token_file"])
    if args.content_dir:
        content_dir = args.content_dir
    else:
        content_dir = config["content_dir"]
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"token {token['access_token']}"}

    user = token["user_name"]
    interval = config["api_interval"]
    repo_list = {}
    for target in config["targets"]:
        section = target["section"]
        repo_list[section] = []

        for repo in target["repos"]:
            print(f"{repo}:", file=sys.stderr)
            sleep(interval, "    get_repo_info")
            info = get_repo_info(user, repo, headers)
            sleep(interval, "    get_languages")
            langs = get_languages(user, repo, headers)
            sleep(interval, "    get_merged_list")
            merged_list = get_merged_list(user, repo, headers)
            info["project_type"] = section
            info["langs"] = langs
            info["merged"] = merged_list
            repo_list[section].append(info)

    save_repolist(content_dir, repo_list)


if __name__ == "__main__":
    main()
