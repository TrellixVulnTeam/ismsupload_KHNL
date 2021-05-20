import tarfile
import requests
from urllib.request import urlopen
import os
import shutil

from fnmatch import fnmatch

eos_dir_path = os.path.join(os.getcwd(), 'eos')

def eos_dirtory(items) :
    if os.path.exists(eos_dir_path) and os.path.isdir(eos_dir_path):
        shutil.rmtree(eos_dir_path)
    os.mkdir(eos_dir_path)
    for item in items :
        os.mkdir(os.path.join(eos_dir_path, item['ip']))

def eos_download(items) :
    for item in items :
        id = str(item['id'])
        tarfile = urlopen("http://poll.medialog.co.kr/ords/aws/isms/download_file/" + id)
        with open(eos_dir_path + '/' +  item['ip'] + '/' + item['ip'] + '.tar','wb') as output:
            output.write(tarfile.read())

def eos_tar_extract(items) :
    for item in items :
        tardir = os.path.join(eos_dir_path, item['ip'])
        try :
            with tarfile.open(tardir + '/' + item['ip'] + '.tar')  as ap :
                ap.extractall(tardir)        
        except Exception as e :
            print(e)


def file_encoding (filename) :

    with open(filename, "r") as f: 
        try :
            file_data = f.readline()
            return 'utf-8'
        except :
            return 'cp949' 

def eos_ip_info (ip_input) :
    import re
    ip = re.search ("([0-9]+).([0-9]+).([0-9]+).([0-9]+)", ip_input)
    return ip.group(0)


def eos_check_update(ip, yn, msg) :
    post_url = 'https://poll.medialog.co.kr/ords/aws/isms/filecheck/'
    data = {'ip': ip, 'yn': yn, 'msg' :msg} 
    res = requests.post(post_url, data=data)
    print(res.status_code)

def eos_check():

    root = eos_dir_path
    pattern = "*.txt"

    filelists = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern) and 'scan' in os.path.join(path, name) :
                filelists.append(os.path.join(path, name))

    for file in filelists :
        enc = file_encoding(file)
        ip = eos_ip_info (file) 
        msg = ''
        yn  = 'Y'
        with open(file,'r', encoding=enc) as f:
            for line in f:
                msg = msg + line
                if '[취약]' in line :
                    yn = 'N'

        eos_check_update(ip, yn, msg)
        # print(ip, yn, msg)


if __name__ == '__main__' :
    pass
    list_url = 'https://poll.medialog.co.kr/ords/aws/isms/download/list' 
    response = requests.get(list_url) 
    items = response.json()['items'] 
    eos_dirtory(items)
    eos_download(items)
    eos_tar_extract(items)
    eos_check()
    # print(items)
