# Setup and Testing Notes

This guide records the demonstrated workflow. Replace example usernames and IP addresses with the current values in your environment.

## Prerequisites

- Ubuntu host with KVM/QEMU and libvirt configured
- Virtual Machine Manager (optional GUI)
- Two Ubuntu Server VMs named `calculator-server` and `calculator-client`
- Python 3 and Flask dependencies on the Server VM
- Python 3 on the Client VM
- Host network access to the libvirt default NAT network

## Start and inspect VMs

On the host:

```bash
sudo virsh list --all
sudo virsh start calculator-server
sudo virsh start calculator-client
sudo virsh domifaddr calculator-server
sudo virsh domifaddr calculator-client
```

## Start Flask API

On the Server VM:

```bash
cd ~/calculator-server
python3 app.py
```

Keep the process running. The API listens on port 5000 and must bind to `0.0.0.0` for access from the Client VM.

## Start the static web server

On the Client VM:

```bash
cd ~
python3 -m http.server 8000 --bind 0.0.0.0
```

Open `http://<client-vm-ip>:8000` in the host browser.

## API checks

From the Client VM:

```bash
curl http://<server-vm-ip>:5000/
curl -X POST http://<server-vm-ip>:5000/calculate \
  -H 'Content-Type: application/json' \
  -d '{"a":10,"b":5,"operation":"add"}'
```

## Request generator

On the Client VM:

```bash
cd ~/calculator-client
chmod +x run.sh
./run.sh 6
```

The six-request run was observed to return six successful results. The Flask terminal on the Server VM showed the corresponding POST requests.

## Resource inspection

On the host:

```bash
free -h
swapon --show
sudo virsh dominfo calculator-server
sudo virsh dommemstat calculator-server
sudo virsh dominfo calculator-client
sudo virsh dommemstat calculator-client
```

A live memory target adjustment was tested on the Server VM:

```bash
sudo virsh setmem calculator-server 1572864 --live
```

This is a manual adjustment. It does not start another VM and must not be described as automated VM autoscaling.

## Recorded validation

| Test | Expected observation | Recorded result |
|---|---|---|
| VM lifecycle | Both guests running | Passed |
| API health | JSON status response | Passed |
| Client-to-server communication | Client can reach Flask API | Passed |
| Browser calculator | UI receives calculation result | Passed |
| Request generation | Six sequential requests return results | Passed |
| Server logs | POST requests visible in Flask terminal | Passed |
| Live memory target | Server VM reports 1.5 GiB target | Passed |
| Threshold-triggered VM launch | Secondary VM starts automatically | Not implemented |

## Troubleshooting

- If browser requests fail, verify Flask is running and listening on `0.0.0.0:5000`.
- Verify the frontend API URL matches the current Server VM IP.
- Re-check guest IP addresses after reboot; DHCP addresses may change.
- If the Client VM cannot reach the API, test `ping` and `curl` from the Client VM.
- Do not copy a running QCOW2 disk directly as a clone. Use a consistent shutdown or a supported image/clone workflow.
