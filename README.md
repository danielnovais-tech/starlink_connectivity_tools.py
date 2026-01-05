# Starlink Connectivity Tools

Python tools for remotely accessing and monitoring Starlink devices using cookie-based authentication.

## Overview

This repository provides example scripts for interacting with Starlink devices remotely. The main script demonstrates how to:
- Authenticate using cookies
- Retrieve account information
- List service lines and dishes
- Get dish status and alerts
- View router/WiFi information
- List connected clients

## Installation

1. Clone this repository:
```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Setup

1. Create a `cookies.json` file with your Starlink authentication cookies:
   - Copy `cookies.json.example` to `cookies.json`
   - Update it with your actual authentication cookies from your browser
   - You can export cookies from your browser using browser developer tools or a cookie export extension

2. Example `cookies.json` structure:
```json
[
  {
    "name": "cookie_name",
    "value": "cookie_value",
    "domain": ".starlink.com",
    "path": "/",
    "secure": true,
    "httpOnly": false
  }
]
```

## Usage

Run the remote access example script:
```bash
python remote_access_example.py
```

The script will:
1. Read authentication cookies from `cookies.json`
2. Connect to your Starlink account
3. Retrieve and display information about:
   - Dishes (ID, serial number, status, alerts)
   - Routers (ID, software version)
   - WiFi networks (2.4GHz and 5GHz SSIDs)
   - Connected clients

## Output Example

```
-------------------------
DISH_ID: dish_12345
Dish Serial: UT12345678901234
Dish Status:
    alert1: value1
    alert2: value2

Router ID: router_12345
Software Version: 2024.01.01.mr12345
Networks: 
    2.4ghz: MyStarlink
    5ghz: MyStarlink_5G
Clients:
    Device1|192.168.1.100
    Device2|192.168.1.101
```

## Security Notes

- **Never commit `cookies.json` to version control** - it contains sensitive authentication information
- The `cookies.json` file is already included in `.gitignore`
- Cookie files stored in `dir_cookies` are also excluded from version control
- Keep your authentication cookies secure and rotate them regularly

## Requirements

- Python 3.7+
- starlink-client library
- protobuf
- grpcio

## License

See LICENSE file for details.