import socket


def get_lan_ip():
    try:
        # Create a socket connection to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connecting to Google's public DNS server

        # Get the local IP address
        lan_ip = s.getsockname()[0]

        return lan_ip
    except Exception as e:
        print(f"Error getting LAN IP address: {str(e)}")
        return None
    finally:
        s.close()
