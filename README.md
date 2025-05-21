# シミュレータの動かし方

1. scenariosディレクトリ内に交通シナリオを作成する
2. SUMOとTraCIサーバーを起動
   scenariosディレクトリの下で、以下のコマンドを実行。

   ```
   python3 traci_server.py \
     --sumo-config ./scenario2/run.sumocfg \
     --step-length 1.0 \
     --traci-port 8813 \
     --server-port 5000
   ```
   SUMOが `run.sumocfg`を読みこみ、ポート8813でTraCIサーバーを立ち上げ、Python が TCP サーバー(127.0.0.1:5000)をリッスン
3. ns-3クライアントを起動
   2とは異なるターミナルなるを開き、ns-3-devディレクトリの下で、以下のコマンドを実行。

   ```
   ./ns3 run simple-gateway -- --serverPort=5000
   ```
