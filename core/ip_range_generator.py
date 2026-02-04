import ipaddress

def generate_ip_range(subnet_cidr: str):
    """
    Menghasilkan daftar IP host dari subnet CIDR
    Contoh input: '192.168.101.0/24'
    """
    network = ipaddress.ip_network(subnet_cidr, strict=False)
    return [str(ip) for ip in network.hosts()]


# ==========================
# TEST MANUAL
# ==========================
if __name__ == "__main__":
    subnet = "192.168.101.0/24"
    ips = generate_ip_range(subnet)

    print(f"Total IP aktif: {len(ips)}")
    print("Sample IP:")
    print(ips[:10])
