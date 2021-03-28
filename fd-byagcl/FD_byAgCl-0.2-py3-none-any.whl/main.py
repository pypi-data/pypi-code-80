# coding = utf-8
import DBConnection, Downloader
if __name__ == '__main__':
    data_src = DBConnection.inst()
    Downloader.download(data_src)
