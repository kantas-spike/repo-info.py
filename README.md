# repo-info.py

本ツールは、[GitHub REST API](https://docs.github.com/ja/rest) を使って、設定ファイル(`pyproject.toml`)に定義したリポジトリの情報を取得し、`JSON`形式で標準出力に出力するツールです。

自作のHugoテーマ [kantas-spike/kantas-theme](https://github.com/kantas-spike/kantas-theme) のデータファイルとして利用することを想定しています。

~~~shell
poetry run python3 repo-info.py > ${hugo_site}/data/projects.json
~~~

[呼び出し用シェルスクリプト](#呼び出し用シェルスクリプトのインストール)をインストールしている場合は、以下を実行します。

~~~shell
~/bin/repo-info.sh > ${hugo_site}/data/projects.json
~~~

[カスタマイズ](#カスタマイズ)手順に従い、御自身の環境にあわせて設定変更してからお使いください。

本ツールでリポジトリから取得する主な情報は、以下になります。

- 基本情報(名前、URL、説明、サイズなど)
- 使用言語(Python,Shellといったプロジェクトが使用している言語)
- 自身が作成したマージ済プルリクエスト情報(インクリメンタルハッキングサイクルのイテレーション)

## 使い方

~~~shell
$ poetry run python3 repo-info.py
odp2jpg.sh:
    get_repo_info: waiting 5.0sec ...
    get_languages: waiting 5.0sec ...
    get_merged_list: waiting 5.0sec ...
# ..略..
{
    "mytools": [
        {
            "name": "slide2video.py",
            "full_name": "kantas-spike/slide2video.py",
            "html_url": "https://github.com/kantas-spike/slide2video.py",
            "description": "Blenderを利用して、スライド資料と、その資料用の音声データから動画編集ファイルを作成するツールです。",
            "size": 20,
            "pushed_at": "2022-07-11T21:09:05Z",
            "project_type": "mytools",
            "langs": [
                "Python",
                "Shell",
                "Makefile"
            ],
            "merged": []
        },
        // ..略..
    ],
    "IHC": [
        {
            "name": "Pong-Game-with-Pygame",
            "full_name": "kantas-spike/Pong-Game-with-Pygame",
            "html_url": "https://github.com/kantas-spike/Pong-Game-with-Pygame",
            "description": "A simple Pong game with Pygame",
            "size": 23,
            "pushed_at": "2022-07-05T18:45:27Z",
            "project_type": "IHC",
            "langs": [
                "Python"
            ],
            "merged": [
                {
                    "html_url": "https://github.com/kantas-spike/Pong-Game-with-Pygame/pull/17",
                    "title": "ドキュメント修正 フォント設定についての記述を追加",
                    "state": "closed",
                    "body": null,
                    "created_at": "2022-07-03T18:15:38Z",
                    "merged_at": "2022-07-03T18:15:51Z",
                    "closed_at": "2022-07-03T18:15:51Z",
                    "user": "kantas-spike"
                },
                // ..略..
            ]
        }
    ]
}
~~~

## 環境構築

以下を実行し、関連するモジュールをインストールしてください。

注意: poetry でパッケージを管理しています。事前にpoetryをインストールしてください。

~~~shell
poetry install
~~~

## 呼び出し用シェルスクリプトのインストール

`repo-info.py`を呼び出す場合、ディレクトリの移動が必要など、実行するまでの作業が煩雑なため、
呼び出し用のシェルスクリプト `repo-info.sh` を用意しています。

以下を実行してインストールしてください。デフォルトでは`~/bin`にインストールされます。

~~~shell
make install
~~~

インストール後は、以下で実行できるようになります。

~~~shell
~/bin/repo-info.sh > ${hugo_site}/data/projects.json
~~~


## カスタマイズ

`pyproject.toml` の `[repo-info]` テーブルに設定情報があります。

~~~toml
[repo-info]
token_file = "access_token.toml"
api_interval = 5.0
~~~

|項目|初期設定値|説明|
|:--:|:--:|:---|
| token_file | access_token.toml | ユーザー名とPersonal access tokens を格納した`tomel`ファイルのパス |
| api_interval | 5.0 | APIの使用制限を越えないようにAPI呼び出し前に一定時間(秒)間隔を開ける|

`token_file`が必須ですので、[トークンファイルの作成方法](#トークンファイルの作成方法)に従って、必ず作成してください。

また、`pyproject.toml` の `[[repo-info.targets]]`に取得対象のプロジェクト情
報があります。取得対象は`name`項目を変更すれば、複数定義可能です。

~~~toml
[[repo-info.targets]]
name = "mytools"
repos = ["odp2jpg.sh", "vv_wav2slide_wav.py", "slide2video.py"]

[[repo-info.targets]]
name = "IHC"
repos = ["Pong-Game-with-Pygame"]
~~~

|項目|説明|
|:--:|:---|
| name | 取得対象のプロジェクトグループの名称 |
| repos | 取得対象のプロジェクト名の一覧 |

### トークンファイルの作成方法

`pyproject.toml` の `[repo-info]` 内、`token_file`で定義した`toml`ファイルに`Personal access tokens`を記載します。

`token_file`は以下の形式になります。ただし、`public_repo`スコープの権限が必要になります。

~~~toml
user_name = "実際のユーザー名"
access_token = "ghp_実際のトークン"
~~~
