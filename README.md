# Mancala Python

## これは何？ What's this?

[マンカラ](https://ja.wikipedia.org/wiki/%E3%83%9E%E3%83%B3%E3%82%AB%E3%83%A9a) のシミュレータ・AI。

## 遊び方

コマンドラインでマンカラがプレイできる。
要 Python3.6+

```sh
% python3 main.py
pit: 6
stone: 4
  | 4| 4| 4| 4| 4| 4|  
 0|  |  |  |  |  |  | 0
  | 4| 4| 4| 4| 4| 4|  
next: 0
pos: 2

  | 4| 4| 4| 4| 4| 4|  
 0|  |  |  |  |  |  | 1
  | 4| 4| 0| 5| 5| 5|  
next: 0
pos: 
```

1. Python3.6 を入れる
1. `python3 main.py` で起動
1. `pit` （片側の穴の数）と `stone` （初期配置での１つの穴あたりの石の数）を入れる
1. `pos: ` は `0-index` で動かしたい場所を指定する。
`next: 0` が下側、 `next: 1` が上側。

## TODO

+ 全探索の実装
+ AIの実装
