## 概要
Let's Play Everybody は、友達と様々な種類のボードゲームを遊ぶことができるサイトです。   
Webアプリなので、OSに関わらず、パソコン・スマホ・タブレット等の様々なプラットフォームからアクセスすることができます。   
このリポジトリは、そのソースです。   

## ディレクトリ構成

    root/
    ├── logic/
    │   └── reversi/
    │       └── ...       （リバーシゲームのロジック関連ファイル）
    ├── manager/
    │   ├── manager.py    （部屋管理やユーザー管理のためのPythonファイル）
    │   ├── room.py       （部屋管理のためのPythonファイル）
    │   └── user.py       （ユーザー管理のためのPythonファイル）
    ├── static/
    │   └── index/
    │       └── ...       （トップページに必要な静的ファイル）
    │   └── reversi/
    │       └── ...       （リバーシゲームのプレイ画面に必要な静的ファイル）
    ├── templates/
    │   ├── index.html
    │   ├── create.html
    │   ├── enter.html
    │   └── reversi.html  （各ページのHTMLファイル）
    ├── requirements.txt  （必要なPythonパッケージの一覧）
    ├── .gitignore        （Gitで管理しないファイルの一覧）
    ├── glitch.json       （Glitchでの設定ファイル）
    └── readme.md         （プロジェクトの説明書）

## デプロイ

[Glitch](https://glitch.com/) で Github から Import で以下リンクを張り付ける   
https://github.com/TakanariShimbo/LetsPlayEverybody.git   
