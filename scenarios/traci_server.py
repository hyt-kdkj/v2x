"""
TraCIサーバー: SUMOとns-3間のコ・シミュレーションを行うPythonスクリプト。
Usage:
  python3 traci_server.py \
    --sumo-config run.sumocfg \
    --step-length 1.0 \
    --traci-port 8813 \
    --server-port 5000
"""
import socket
import traci
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="TraCI server for SUMO-ns3 co-simulation")
    parser.add_argument('--sumo-config', '-c', type=str, default="run.sumocfg", help="SUMO configuration file (.sumocfg)")
    parser.add_argument('--step-length', '-s', type=float, default=1.0, help="SUMO simulation step length (seconds)")
    parser.add_argument('--traci-port', '-t', type=int, default=8813, help="Port for TraCI (SUMO <-> Python)")
    parser.add_argument('--server-port', '-p', type=int, default=5000, help="Port for ns-3 Gateway TCP server")
    args = parser.parse_args()

    # Start SUMO via TraCI
    sumo_cmd = ["sumo", "-c", args.sumo_config, "--step-length", str(args.step_length)]
    print(f"Starting SUMO: {' '.join(sumo_cmd)}, TraCI port {args.traci_port}")
    traci.start(sumo_cmd, port=args.traci_port)

    # Set up TCP server for ns-3
    HOST = '127.0.0.1'
    PORT = args.server_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(1)
        print(f"ns-3 Gateway server listening on {HOST}:{PORT}")
        conn, addr = srv.accept()
        conn.settimeout(0.1)  # 応答がない場合に recv でブロックしないようにする
        print(f"ns-3 connected from {addr}")

        MAX_STEP = 20
        step = 0
        try:
            while traci.simulation.getMinExpectedNumber() > 0 and step < MAX_STEP:
                traci.simulationStep()
                step += 1

                # Collect vehicle positions
                veh_ids = traci.vehicle.getIDList()
                if len(veh_ids) == 0:
                    # 車両がいないときは送らない
                    continue 
                payload = f"{step},0"
                for vid in veh_ids:
                    x, y = traci.vehicle.getPosition(vid)
                    payload += f",{x:.2f},{y:.2f}"
                payload += ';'

                # デバッグ出力
                print(f"[SUMO→ns-3] step={step}, vehicles={len(veh_ids)}")

                # Send to ns-3
                conn.sendall(payload.encode())

                # 応答があれば受信する（なくても次ループへ）
                try:
                    resp = conn.recv(1024).decode()
                    if resp:
                        print(f"[ns-3→SUMO] resp={resp}")
                except socket.timeout:
                    pass

        except Exception as e:
            print(f"Error during co-simulation: {e}", file=sys.stderr)
        finally:
            traci.close()
            conn.close()
            print("Simulation finished. Resources cleaned up.")

if __name__ == '__main__':
    main()
