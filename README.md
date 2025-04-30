# Port Scanner 🔎

A simple Python-based port scanner tool that can scan specific ports or all ports on a target host.

## Features
- Scan specific ports by providing a list
- Scan all 65535 ports using `-a` or `--all`
- Accepts both lowercase and uppercase arguments
- Fast and simple to use

## Usage

```bash
python port_scanner.py -u <target_host> [-p <port1,port2,port3>] [-a | --all]
```

### Examples

- Scan selected ports:
  ```bash
  python port_scanner.py -u google.com -p 80,443
  ```

- Scan all ports:
  ```bash
  python port_scanner.py -u google.com --all
  ```

## Requirements

- Python 3.x

## License

This project is open-source and free to use.

---

