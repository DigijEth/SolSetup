# path: solana_auth.py
from solana.rpc.api import Client
from solana.keypair import Keypair
import os

class SolanaAuth:
    def __init__(self, rpc_url: str = "https://api.mainnet-beta.solana.com"):
        self.client = Client(rpc_url)
        self.keypair = None

    def load_keypair(self, path: str):
        with open(path, "r") as f:
            secret = f.read().strip()
        self.keypair = Keypair.from_secret_key(bytes.fromhex(secret))
        print("Wallet loaded:", self.keypair.public_key)

    def authenticate(self):
        if not self.keypair:
            path = input("Enter path to Solana secret key (hex file): ")
            self.load_keypair(path)
        nonce = os.urandom(24)
        signed = self.keypair.sign(nonce)
        print("Nonce:", nonce.hex())
        print("Signature:", signed.signature.hex())
        print("Authentication complete (zero-trust CLI placeholder).")
