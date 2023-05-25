# repo-info.py

本ツールは、[GitHub REST API](https://docs.github.com/ja/rest) を使って、設定ファイル(`pyproject.toml`)に定義したリポジトリの情報を取得し、指定された出力ディレクトリにMakdownファイルとして出力するツールです。

生成されるMarkdownファイルは、自作のHugoテーマ [kantas-spike/kantas-theme](https://github.com/kantas-spike/kantas-theme) 用の`mytools`、`ihc`セクション内のページとして利用することを想定しています。

以下のコマンドを実行すると、リポジトリの情報を取得し、Makdownファイルを出力します。(詳細は、[環境構築](#環境構築)と[使い方](#使い方)を参照してください。)

~~~shell
poetry run python3 repo-info.py
~~~

[呼び出し用シェルスクリプト](#呼び出し用シェルスクリプトのインストール)をインストールしている場合は、以下を実行します。

~~~shell
~/bin/repo-info.sh
~~~

[カスタマイズ](#カスタマイズ)手順に従い、御自身の環境にあわせて設定変更してからお使いください。

本ツールでリポジトリから取得する主な情報は、以下になります。

- 基本情報(名前、URL、説明、サイズなど)
- 使用言語(Python,Shellといったプロジェクトが使用している言語)
- 自身が作成したマージ済プルリクエスト情報(インクリメンタルハッキングサイクルのイテレーション)

## 使い方

~~~shell
$ poetry run python3 repo-info.py
API_URL: https://api.github.com/repos/kantas-spike
OUTPUT_DIR: ~/blog/content

odp2jpg.sh:
    get_repo_info: waiting 5.0sec ...
    get_languages: waiting 5.0sec ...
    get_merged_list: waiting 5.0sec ...
# ..略..
save repolist ~/blog/content/mytools...
  ~/blog/content/mytools/odp2jpg.sh.md...
  ~/blog/content/mytools/vv_wav2slide_wav.py.md...
# ..略..
save repolist ~/blog/content/ihc...
  ~/blog/content/ihc/Pong_Game_with_Pygame.md...
  ~/blog/content/ihc/kantas_theme.md...
# ..略..
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
~/bin/repo-info.sh
~~~

## カスタマイズ

`pyproject.toml` の `[repo-info]` テーブルに設定情報があります。

~~~toml
[repo-info]
token_file = "access_token.toml"
api_interval = 5.0
content_dir = "~/blog/content"
~~~

|項目|初期設定値|説明|
|:--:|:--:|:---|
| token_file | access_token.toml | ユーザー名とPersonal access tokens を格納した`tomel`ファイルのパス |
| api_interval | 5.0 | APIの使用制限を越えないようにAPI呼び出し前に一定時間(秒)間隔を開ける|
| content_dir | ~/blog/content | プロジェクトの情報を記載したMakdownファイルの出力先ディレクトリ|

`token_file`が必須ですので、[トークンファイルの作成方法](#トークンファイルの作成方法)に従って、必ず作成してください。

また、`pyproject.toml` の `[[repo-info.targets]]`に取得対象のプロジェクト情報があります。

~~~toml
[[repo-info.targets]]
section = "mytools"
repos = ["odp2jpg.sh", "vv_wav2slide_wav.py", "slide2video.py"]

[[repo-info.targets]]
section = "IHC"
repos = ["Pong-Game-with-Pygame"]
~~~

|項目|説明|
|:--:|:---|
| section | Makdownファイルの出力先ディレクトリ(`content_dir`)の配下に作成するサブディレクトリ名 |
| repos | 取得対象のプロジェクト名の一覧。各プロジェクト名でMarkdownファイルが作成される |

### トークンファイルの作成方法

`pyproject.toml` の `[repo-info]` 内、`token_file`で定義した`toml`ファイルに`Personal access tokens`を記載します。

`token_file`は以下の形式になります。ただし、`public_repo`スコープの権限が必要になります。

~~~toml
user_name = "実際のユーザー名"
access_token = "ghp_実際のトークン"
~~~
