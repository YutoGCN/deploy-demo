---
marp: true
theme: gaia
size: 16:9
paginate: true
header: sola project 2024/7/29
footer: © 2024 Love Machine Inc.
---
<!--
headingDivider: 1
-->

# sola project demo
<!--
_class: lead
_paginate: false
_header: ""
-->

# 環境構築
```
git clone https://github.com/YutoGCN/deploy-demo

cd deploy-demo

pip3 install -r requirements.txt
```

# エンドポイントの設定
```
BASE_URL = ""
```

`endopoint.py`の`""`の間にお渡ししたエンドポイントのurlを入れてください。


# 実行

```
python3 main.py
```

main.pyの簡略化された中身
```
run_id = SolaClient.request('test_man', 'user-demo-1', 'man', 'upper')

while True:
    status = SolaClient.get_status(run_id)

    if status == 'FINISHED':
        SolaClient.get_movie(run_id, f'tmp\\{run_id}.mp4')
        break
```


# 生成要求関数
```
run_id = SolaClient.request('material_folder', 'user_name', 'lora_option', 'scale_option')
```

生成の要求を行う関数。パラメータは以下。

`user_name`: ユーザー名、お好きな文字列
`lora_option`: 何のloraを使うか、`'man'` or `'woman'`
`scale_option`: 上半身か全身か、`'upper'` or `'whole'`

返り値は以下。
`run_id`: 要求ごとに固有のIDが返される

# 生成進捗確認関数
```
status = SolaClient.get_status(run_id)
```

生成の進捗を確認する関数。

`run_id`: 生成の要求を行った際に返されたID

`status`: 生成の進捗状況が返される。`'PENDING'`, `'RUNNING'`, `'FINISHED'`, `'ERROR'` のいずれか


# 生成動画ダウンロード関数
```
downloaded_path =  SolaClient.get_movie(run_id, download_path_you_want)
```

生成された動画をダウンロードする関数。

`run_id`: 生成の要求を行った際に返されたID
`download_path_you_want`: ダウンロードしたい場所

`downloaded_path`: 実際にダウンロードされた場所が返される、失敗ならNoneが返される

# 展望
生成のパラメータを増加させる予定

 - promptを指定可能にする
 - loraの種類を増加
 - controlnetの比重を変更可能にする 等

