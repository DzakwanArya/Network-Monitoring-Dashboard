import psutil
import ipaddress

def detect_network():
    interfaces = psutil.net_if_addrs()
    result = []

    for iface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == 2:
                if addr.address.startswith(("169.254", "127.")):
                    continue

                network = ipaddress.IPv4Network(
                    f"{addr.address}/{addr.netmask}",
                    strict=False
                )

                result.append({
                    "interface": iface,
                    "ip": addr.address,
                    "netmask": addr.netmask,
                    "subnet": str(network.network_address),
                    "cidr": network.prefixlen
                })

    return result


if __name__ == "__main__":
    print(detect_network())
