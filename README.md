# 歩行情報蓄積及び現在位置推定サーバ

> [!IMPORTANT]
> 環境変数は[こちらから](https://kjlb.esa.io/posts/6068)確認してください

## 実行方法

```
make app-up
```

## その他

### DB コンテナに入りたいとき

```bash
make db
```

### ER 図生成

```
make spy-up
```

`http://localhost:8080/public/relationships.html`にアクセスすると ER 図を閲覧できます

> [!NOTE]
> 初期化用 SQL の修正を反映したい場合は
>
> ```
> make all-restart
> ```
>
> を実行してください
