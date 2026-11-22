# Screenshot Evidence Checklist

Save original screenshots in this directory. Prefer clear terminal or browser captures with the relevant command, VM name, and result visible. Avoid cropping away context needed to verify the result. Do not fabricate or recreate terminal output.

| Suggested filename | Evidence to capture | Priority |
|---|---|---|
| `01-vm-manager.png` | Virtual Machine Manager showing calculator-client and calculator-server running | Required |
| `02-server-api-running.png` | Server VM terminal showing Flask listening on port 5000 | Required |
| `03-client-web-server.png` | Client VM terminal showing HTTP server on port 8000 | Recommended |
| `04-network-connectivity.png` | Client VM ping/curl to Server VM | Required |
| `05-calculator-interface.png` | Browser displaying the actual calculator UI | Required |
| `06-calculation-result.png` | Browser showing a successful calculation | Required |
| `07-api-curl-response.png` | Successful POST /calculate JSON response | Required |
| `08-six-requests.png` | Client VM running `./run.sh 6` with six responses | Required |
| `09-server-access-logs.png` | Flask terminal showing incoming POST requests | Required |
| `10-vm-memory-stats.png` | `virsh dominfo` and/or `dommemstat` for the Server VM | Recommended |
| `11-host-resource-usage.png` | Host `free -h` and `swapon --show` output | Recommended |

## Capture commands

Run these in the appropriate terminals and capture the actual output:

**Host:**

```bash
sudo virsh list --all
sudo virsh dominfo calculator-server
sudo virsh dommemstat calculator-server
free -h
```

**Client VM:**

```bash
ping -c 4 <server-vm-ip>
curl http://<server-vm-ip>:5000/
cd ~/calculator-client
./run.sh 6
```

**Server VM:**

```bash
cd ~/calculator-server
python3 app.py
```

Keep screenshots authentic. If a result was not captured at the time, reproduce the test and capture it now. Do not label an unimplemented autoscaling event as a successful test.
