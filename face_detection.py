# path: face_detection.py
import face_recognition
import pickle
import os
from utils import encrypt_data, decrypt_data

class FaceDetection:
    def __init__(self, storage_path: str = "embeddings/"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)
        self.key = None

    def set_encryption_key(self):
        key_hex = input("Enter encryption key for embeddings (32-byte hex): ")
        self.key = bytes.fromhex(key_hex)

    def generate_embedding(self):
        image_path = input("Enter path to image file: ")
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            print("No faces found in image.")
            return
        embedding = encodings[0]
        data = pickle.dumps(embedding)
        if not self.key:
            self.set_encryption_key()
        token = encrypt_data(self.key, data)
        fname = os.path.join(self.storage_path, os.path.basename(image_path) + ".bin")
        with open(fname, "wb") as f:
            f.write(token)
        print("Encrypted embedding saved to", fname)
