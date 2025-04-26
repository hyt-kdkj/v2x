# OMNeT++

## サンプルコードの実行

以下のコマンドを実行し、tictocが実行できるかを確認

```
source venv/bin/activate

cd omnetpp-6.0.3

. setenv

./configure

make

cd samples/tictoc

./tictoc --network=Tictoc1

```

↓こんな感じのが出てたら大丈夫のはず

```
Preparing for running configuration General, run #0...
Assigned runID=General-0-20250414-13:36:42-3696
Setting up network "Tictoc1"...
Initializing...

Running simulation...
** Event #0   t=0   Elapsed: 5.4e-05s (0m 00s)
     Speed:     ev/sec=0   simsec/sec=0   ev/simsec=0
     Messages:  created: 1   present: 1   in FES: 1
** Event #23730176   t=2373017.6   Elapsed: 2.00008s (0m 02s)
     Speed:     ev/sec=1.1865e+07   simsec/sec=1.1865e+06   ev/simsec=10
     Messages:  created: 1   present: 1   in FES: 0
** Event #47376640   t=4737664   Elapsed: 4.0001s (0m 04s)
     Speed:     ev/sec=1.18231e+07   simsec/sec=1.18231e+06   ev/simsec=10
     Messages:  created: 1   present: 1   in FES: 0
** Event #71143680   t=7114368   Elapsed: 6.00012s (0m 06s)
     Speed:     ev/sec=1.18834e+07   simsec/sec=1.18834e+06   ev/simsec=10
     Messages:  created: 1   present: 1   in FES: 0
** Event #92233720   t=9223372   Elapsed: 7.76662s (0m 07s)
     Speed:     ev/sec=1.19389e+07   simsec/sec=1.19389e+06   ev/simsec=10
     Messages:  created: 1   present: 1   in FES: 0

<!> Error: simtime_t overflow adding 0.1 to 9223372: Result is out of range (-9223372.036854775807,9223372.036854775807), allowed by scale exponent -12 -- in module (Txc1) Tictoc1.tic (id=2), at t=9223372s, event #92233720
undisposed object: (omnetpp::cMessage) Tictoc1.tic.tictocMsg -- check module destructor

End.
```

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

# Veins
