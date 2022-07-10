import base64
import os
import zipfile


def reload_python_codes(path="/src/code"):
    decoded_file = "/tmp/func.decoded"
    if os.path.exists(path):
        with open(path, "r") as encoded_file, open(
            decoded_file, "wb"
        ) as decode_zipfile:
            decoded_bytes = base64.b64decode(encoded_file.read())
            decode_zipfile.write(decoded_bytes)
        with zipfile.ZipFile(decoded_file, "r") as zf:
            zf.extractall("/app")
        os.remove(decoded_file)


if __name__ == "__main__":
    reload_python_codes()
