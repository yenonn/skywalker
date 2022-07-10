import base64
import os
import zipfile
import hashlib
import time


def md5sum_changed(path="/src/code"):
    md5sum_out_path = "/tmp/md5sum.out"
    md5sum_out = ""
    md5sum_src = hashlib.md5(open(path, "rb").read()).hexdigest()
    if not os.path.exists(md5sum_out_path):
        with open(md5sum_out_path, "w") as md5sum_file:
            md5sum_file.write(md5sum_src)
    else:
        md5sum_out = open(md5sum_out_path, "r").read()
    if md5sum_src == md5sum_out:
        return False
    else:
        with open(md5sum_out_path, "w") as file:
            file.write(md5sum_src)

    return True


def reload_configmap(path="/src/code"):
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
    while True:
        time.sleep(10)
        if md5sum_changed():
            reload_configmap()
