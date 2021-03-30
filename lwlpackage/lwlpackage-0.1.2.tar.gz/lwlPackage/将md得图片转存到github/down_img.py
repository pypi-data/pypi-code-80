import os

os.makedirs('./image/', exist_ok=True)



def request_download(path,IMAGE_URL):
    import requests
    r = requests.get(IMAGE_URL)
    with open(path, 'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    request_download('./image/img2.png', IMAGE_URL='')
    print('download img2')
