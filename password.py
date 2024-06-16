import subprocess

def get_wifi_passwords():
    try:
        # Get the names of all saved Wi-Fi networks
        networks = subprocess.check_output("netsh wlan show profiles", shell=True).decode('utf-8').split('\n')
        wifi_profiles = [line.split(":")[1][1:-1] for line in networks if "All User Profile" in line]

        # Get the password for each Wi-Fi network
        wifi_passwords = {}
        for profile in wifi_profiles:
            try:
                password_info = subprocess.check_output(f"netsh wlan show profile {profile} key=clear", shell=True).decode('utf-8').split('\n')
                for line in password_info:
                    if "Key Content" in line:
                        password = line.split(":")[1][1:-1]
                        wifi_passwords[profile] = password
                        break
                else:
                    wifi_passwords[profile] = None
            except subprocess.CalledProcessError:
                wifi_passwords[profile] = None

        return wifi_passwords

    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve Wi-Fi profiles: {e}")
        return {}

wifi_passwords = get_wifi_passwords()
for wifi, password in wifi_passwords.items():
    print(f"SSID: {wifi}, Password: {password}")
