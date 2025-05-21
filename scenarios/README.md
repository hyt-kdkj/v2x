# SUMO

## 各ファイルの役割

・nod.xmlファイル
交差点や道路の単点を定義するためのファイル
ノードは道路（エッジ）をつなぐ基準点で，x,y は2D空間での位置

```
<nodes>
    <node id="n0" x="0.0" y="0.0"/>
    <node id="n1" x="500.0" y="0.0"/>
</nodes>
```

・edg.xmlファイル
ノード間を結ぶ道路を定義するためのファイル
エッジは方向付きでfrom/toで始点と終点のノードを指定

```
<edges>
    <edge id="edge0" from="n0" to="n1" priority="1" numLanes="1" speed="13.89"/>
</edges>
```

・net.xmlファイル
nod.xml, edg.xmlを元に生成される実際にシミュレーションで使用する道路ネットワークの統合ファイル
車線数，速度制限，リンク（接続関係）など詳細な情報が含まれる
以下のコマンドを実行すると作成される
(example.edg.xmlとexample.nod.xmlファイルは事前に準備しておく必要あり，net.xmlファイル名は自分で指定)

```
netconvert -n example.nod.xml -e example.edg.xml -o example.net.xml
```

・rou.xmlファイル
車両の生成タイミング，ルート，出発時間など交通流の情報を定義するためのファイル

```
<routes>
    <vType id="car" accel="1.0" decel="4.5" length="5" maxSpeed="13.89"/>

    <vehicle id="veh0" type="car" depart="0">
        <route edges="edge0"/>
    </vehicle>

    <vehicle id="veh1" type="car" depart="5">
        <route edges="edge0"/>
    </vehicle>

    <vehicle id="veh2" type="car" depart="10">
        <route edges="edge0"/>
    </vehicle>
</routes>
```

・run.sumocfg
SUMOシミュレータを実行するための設定ファイル（シナリオファイル）
シミュレータ全体の構成上情報（どのネットワークやルートを使うか，シミュレーション時間設定など）が書かれており，SUMOを動かすときに中心的な役割を果たす
**net.xmlファイルがないとエラーになるので，作ったことを確認してから実行してください**

```
<configuration>
    <input>
        <net-file value="example.net.xml"/>
        <route-files value="example.rou.xml"/>
    </input>

    <time>
        <begin value="0"/>
        <end value="50"/>
    </time>

    <output>
        <!-- 各車両の移動ログ（時刻ごとの位置） -->
        <fcd-output value="fcd.xml"/>
  
        <!-- 各車両の出発〜到着までの統計情報 -->
        <tripinfo-output value="tripinfo.xml"/>

        <!-- ネットワーク全体の状態（各エッジの車両数など） -->
        <netstate-dump value="netstate.xml"/>

        <!-- 概要統計（1ステップあたりの車両数など） -->
        <summary-output value="summary.xml"/>

        <!-- ルート選択のログ（ルートが変更された場合など） -->
        <vehroutes value="vehroutes.xml"/>

        <!-- 車両が使ったエッジのステップごとの滞在時間など -->
        <emission-output value="emissions.xml"/>

        <!-- 各車両の滞在時間ヒートマップの元データ -->
        <lanechange-output value="lanechange.xml"/>
    </output>
</configuration>

```

## シミュレータの実行

必要なファイルが入っているディレクトリ内で

```
sumo -c run.sumocfg
```

を実行すると，各種出力ファイルがディレクトリ内に作成される

| 出力ファイル名     | 説明                                               |
| ------------------ | -------------------------------------------------- |
| `fcd.xml`        | 各車両のステップごとの位置（位置追跡データ）       |
| `tripinfo.xml`   | 車両ごとの走行結果（出発時刻、走行時間など）       |
| `netstate.xml`   | ネットワークの状態（車両数、エッジごとの密度など） |
| `summary.xml`    | シミュレーション全体の概要統計                     |
| `vehroutes.xml`  | 各車両が実際に走行したルート                       |
| `emissions.xml`  | 排出ガス（必要なら設定を追加で有効に）             |
| `lanechange.xml` | 車線変更イベントの記録                             |