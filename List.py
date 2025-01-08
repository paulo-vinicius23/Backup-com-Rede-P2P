import requests


def list_networks(node_url: str) -> None:
    """List networks connected to a specific IPFS node."""
    try:
        print(f"\nConnecting to node at {node_url}...")
        response = requests.post(f"{node_url}/api/v0/swarm/peers", timeout=5)

        if response.status_code == 200:
            peers = response.json().get("Peers", [])
            print(f"Networks for node at {node_url}:")
            if peers:
                unique_peers = {peer['Addr'] for peer in peers}
                for addr in unique_peers:
                    print(f"- Address: {addr}")
            else:
                print("No connected peers found.")
        else:
            print(f"Failed to list networks for {node_url}. Status Code: {response.status_code}")
    except requests.exceptions.ConnectTimeout:
        print(f"Connection to {node_url} timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while listing networks for {node_url}: {e}")


def main():
    """Main function to list networks of multiple IPFS nodes."""
    node_urls = [ 
        "http://localhost:5001",  # First node
        "http://localhost:5002"   # Second node
    ]

    print("Listing networks for P2P nodes...\n")
    for node_url in node_urls:
        list_networks(node_url)


if __name__ == "__main__":
    main()
