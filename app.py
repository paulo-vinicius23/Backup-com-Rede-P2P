import os
import requests
import subprocess  # Para executar o script de listagem


def upload_file_to_ipfs(node_url: str, file_path: str) -> str:
    """Upload a file to the specified IPFS node."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    with open(file_path, "rb") as file:
        response = requests.post(f"{node_url}/api/v0/add", files={"file": file})

    if response.status_code == 200:
        response_data = response.json()
        print(f"File uploaded successfully. Hash: {response_data['Hash']}")
        return response_data["Hash"]
    else:
        raise Exception(
            f"Failed to upload file. Status Code: {response.status_code}, Response: {response.text}"
        )


def download_file_from_ipfs(node_url: str, file_hash: str, output_path: str) -> None:
    """Download a file from the specified IPFS node."""
    response = requests.post(f"{node_url}/api/v0/cat?arg={file_hash}")

    if response.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully to {output_path}")
    else:
        raise Exception(
            f"Failed to download file. Status Code: {response.status_code}, Response: {response.text}"
        )


def main():
    """Main function to list networks, upload a file, and download it."""
    # Step 1: Call the List.py script
    print("Listing networks by calling List.py...\n")
    subprocess.run(["python", "List.py"], check=True)

    # Step 2: Proceed with upload and download
    node1_url = "http://localhost:5001"
    node2_url = "http://localhost:5002"

    file_to_upload = "test_file.txt"

    try:
        print("\nUploading file to the first node...")
        uploaded_file_hash = upload_file_to_ipfs(
            node_url=node1_url, file_path=file_to_upload
        )

        print("\nDownloading file from the second node...")
        output_file = "downloaded_testfile.txt"
        download_file_from_ipfs(
            node_url=node2_url, file_hash=uploaded_file_hash, output_path=output_file
        )
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
