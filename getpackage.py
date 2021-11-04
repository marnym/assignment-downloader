import re
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import os, sys
import subprocess

# Example link:
# https://tarjotin.cs.aalto.fi/CS-A1140/2021/scala3-sbt/A1140-scala3-r6-knapsack.zip

def get_url() -> str:
    url = ""
    if len(sys.argv) < 2:
        url = input("Enter url: ")
    else:
        url = sys.argv[1]
    return url

def get_zip(url: str) -> ZipFile:
    resp = urlopen(url)
    return ZipFile(BytesIO(resp.read()))

def get_round(dirname: str) -> str:
    m = re.search(r'r\d', dirname)
    if not m:
        raise Exception("Round not found")
    return m.group()

def check_directory(dir: str) -> None:
    if os.path.isdir(dir):
        print("Directory already exists")
        subprocess.Popen(["code", dir])
        sys.exit(0)

def main():
    url = get_url()
    print("Downloading file from:", url)
    zipfile = get_zip(url)
    dirname = zipfile.namelist()[0]
    round_dir = get_round(dirname)
    full_path = f"{round_dir}/{dirname}"
    check_directory(full_path)

    print("Round is:", round_dir)
    print("Extracting:", dirname)
    zipfile.extractall(round_dir)

    package_name = dirname.split("-")[-1][:-1]

    subprocess.run(["git", "add", full_path])
    subprocess.run(["git", "commit", "-m", f"Add {package_name}"])

    subprocess.Popen(["code", full_path])

if __name__ == '__main__':
    main()
