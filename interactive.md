# インタラクティブ実行

```
python3 interactive.py
```

インタラクティブに以下を行えます
・生成リクエスト
・ジョブ一覧の取得
・ジョブの進捗確認
・中断
・生成結果をダウンロード
生成が完了するまで待つ、等はできません。

# 書き換え方法
main2.pyの上の方を書き換えて適切なフォルダ構造に対応してください。

# 生成要求関数
```
run_id = SolaClient.request('material_folder', 'user_name', 'job_name','params_comfy_path')
```

生成の要求を行う関数。パラメータは以下。

`material_folder`: 素材フォルダのパス
`user_name`: ユーザー名、ex. `love_machine_noguchi`
`job_name` : ジョブ名、お好きな文字列
`params_comfy_path`: パラメータファイルのパス

返り値は以下。
`run_id`: 要求ごとに固有のIDが返される

# パラメータファイルについて

`PARAM_LORA_x_NAME` は `"angel\\\\angel_man_test00.safetensors"` か `"angel\\\\angel_woman_test01-000120.safetensors"`のどちらかを指定してください。

`"PARAM_UPSCALE"`は0.7から1.0の値にしてください。

その他の数値は0.0から1.0の値にしてください。`PARAM_LORA_x_STRENGTH`はLoraの強さで、0にするとLoraがない状態になります。

`"PARAM_PROMPT"`にはプロンプトの文字列を入れてください。

# ジョブ一覧取得関数
```
jobs = SolaClient.list_jobs_by_user('user_name')
jobs = SolaClient.list_all_jobs() #全ユーザーのジョブを取得
```

`user_name`: ユーザー名、リクエストしたときと同じ値

`jobs`: ユーザーがリクエストしたジョブのリストが返される。リストは二次元配列。例を示す。

```
[[1, 'lovemachine', 'test_man', 'TERMINATED', 0], 
[2, 'lovemachine', 'test_man2', 'TERMINATED', 0], 
[3, 'lovemachine', 'test_man3', 'RUNNING', 0]]
```

# 生成進捗確認関数
```
status = SolaClient.get_status(run_id)
```

生成の進捗を確認する関数。

`run_id`: 生成の要求を行った際に返されたID

`status`: 生成の進捗状況が返される。`'PENDING'`, `'RUNNING'`, `'FINISHED'`, `'ERROR'`, `TERMINATED`のいずれか。

# ジョブ中断関数
```
SolaClient.terminate(run_id)
```

生成を中断する関数。

`run_id`: 生成の要求を行った際に返されたID

# 生成動画ダウンロード関数
```
downloaded_path =  SolaClient.get_movie(run_id, download_path_you_want)
```

生成された動画をダウンロードする関数。

`run_id`: 生成の要求を行った際に返されたID
`download_path_you_want`: ダウンロードしたい場所

`downloaded_path`: 実際にダウンロードされた場所が返される、失敗ならNoneが返される