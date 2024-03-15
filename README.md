# Umardle
Wordle uma version

## データ設計

index.htmlにインポートされる定数

対象馬名(list)
```
const horses = ["馬名",...]
```

- central_g1_horses
- central_all_horses
- local_g1_horses
- local_all_horses
- overseas_g1_horses
- overseas_all_horses
- jump_g1_horses
- jump_all_horses

レース情報(dict)
```
const xxx_races = {
    "レースキーワード" : {
        name: "レース名",
        type: "レース種別(芝/ダート)",
        grade: グレード,
        organize: "主催(中央/地方/海外)",
        start: 開始年,
        last: 終了年,
        keyword: "レースキーワード"
    },...
}
```

- central_races
- local_races
- ovearseas_races

レース結果(list)
```
const レースキーワード = [
    {
        race: "レースキーワード",
        year: 開催年,
        horse: "勝ち馬"
    },...
]
```

- 全レース（定数名：レースキーワード）

レースリスト(list)
※対象レースの選択条件用のショートカット
```
const race_list = ["レースキーワード",...]
```

- central_g1
- central_all
- local_g1
- local_all
- overseas_g1
- overseas_all
- jump_g1
- jump_all

## UI設計

[開始・リセットボタン]

[対象レース選択] ▶ [詳細設定]

[テキストボックス][実行ボタン]

第1レース：入力履歴

第2レース：入力履歴

・・・

第Xレース

惜しい文字

外れた文字

## 処理設計

### 開始前
1. 選択レースを基に抽出元リスト/対象馬リストを作成する
    選択レースのレース結果リストをすべて連結する
    デフォルト条件：中央G1レース(障害競走を除く)
1. 抽出元リストからランダムに要素（レース結果）を１つ取得し解答として登録する
    抽出元リストの要素数を上限とするrandom()
1. 入力した馬名が対象馬リストに存在しているか確認する
    存在していない場合は、エラーメッセージを表示する
1. 解答馬名と１字ずつ比較する
1. 文字ごとに完全一致、採用、非採用の分類分けをする
1. 分類分け処理
    1. すべてが一致している → ゲームクリア
    1. 一致リストを更新、不一致の部分があれば入れ替える → 描画
    1. 採用リストを追加（重複は追加しない）、一致リストと重複しているものを削除する → 描画
    1. 不採用リスト追加（重複は追加しない） → 描画

## 参考サイト

おうまのアイコン wire-to-wire
https://horseicon.web.fc2.com/
