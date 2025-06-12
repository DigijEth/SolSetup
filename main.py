# path: main.py
from solana_auth import SolanaAuth
from face_detection import FaceDetection
from csam_scan import CSAMScan

def main():
    auth = SolanaAuth()
    face = FaceDetection()
    scanner = CSAMScan()

    menu = """
Select an option:
1) Authenticate Solana Wallet
2) Generate Face Embedding
3) Scan CSAM Database
4) Exit
"""
    while True:
        print(menu)
        choice = input("Choice: ").strip()
        if choice == '1':
            auth.authenticate()
        elif choice == '2':
            face.generate_embedding()
        elif choice == '3':
            scanner.scan_db()
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
