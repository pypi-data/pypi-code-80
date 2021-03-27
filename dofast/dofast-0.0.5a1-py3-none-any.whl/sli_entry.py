def _main():
    from .simple_parser import SimpleParser, PLACEHOLDER
    sp = SimpleParser()
    sp.add_argument('-cos',
                    '--cos',
                    sub_args=[["u", "up", "upload"], ["download", "d", "dw"],
                              ["l", "list"], ["del", "delete"]])
    sp.add_argument('-oss',
                    '--oss',
                    sub_args=[["u", "up", "upload"], ["download", "d", "dw"],
                              ["l", "list"], ["del", "delete"]])
    sp.add_argument('-dw', '--download', sub_args=[])
    sp.add_argument('-d', '--ddfile')
    sp.add_argument('-ip',
                    '--ip',
                    sub_args=[['p', 'port']],
                    default_value="localhost")
    sp.add_argument('-rc', '--roundcorner', sub_args=[['r', 'radius']])
    sp.add_argument('-gu', '--githubupload')
    sp.add_argument('-sm', '--smms')
    sp.add_argument('-yd', '--youdao')
    sp.add_argument('-fd', '--find', sub_args=[['dir', 'directory']])
    sp.add_argument('-m', '--msg', sub_args=[['r', 'read'], ['w', 'write']])
    sp.add_argument('-fund', '--fund', sub_args=[['ba', 'buyalert']])
    sp.add_argument('-stock', '--stock')
    sp.add_argument('-aes',
                    '--aes',
                    sub_args=[['en', 'encode'], ['de', 'decode']])

    sp.parse_args()
    if sp.cos:
        from .cos import COS
        cli = COS()
        if sp.cos.upload:
            cli.upload_file(sp.cos.upload, "transfer/")
        elif sp.cos.download:
            _file = sp.cos.download
            cli.download_file(f"transfer/{_file}", _file)
        elif sp.cos.delete:
            cli.delete_file(f"transfer/{sp.cos.delete}")
        elif sp.cos.list:
            print(cli.prefix())
            cli.list_files("transfer/")

    elif sp.oss:
        from .oss import Bucket, Message
        from .utils import download
        cli = Bucket()
        if sp.oss.upload:
            cli.upload(sp.oss.upload)
        elif sp.oss.download:
            # Note the download func here is: .utils.download
            download(cli.url_prefix + sp.oss.download)
        elif sp.oss.delete:
            cli.delete(sp.oss.delete)
        elif sp.oss.list:
            print(cli.url_prefix)
            cli.list_files()

    elif sp.download:
        from .utils import download
        print(sp.download)
        download(sp.download.value)

    elif sp.ddfile:
        from .utils import create_random_file
        create_random_file(int(sp.ddfile.value or 100))

    elif sp.ip:
        v_ip, v_port = sp.ip.value, sp.ip.port
        from .utils import shell
        if not sp.ip.port:
            print(shell("curl -s cip.cc"))
        else:
            print("Checking on:", v_ip, v_port)
            curl_socks = f"curl -s --connect-timeout 5 --socks5 {v_ip}:{v_port} ipinfo.io"
            curl_http = f"curl -s --connect-timeout 5 --proxy {v_ip}:{v_port} ipinfo.io"
            res = shell(curl_socks)
            if res != '':
                print(res)
            else:
                print('FAILED(socks5 proxy check)')
                print(shell(curl_http))

    elif sp.roundcorner:
        from .utils import rounded_corners
        image_path = sp.roundcorner.value
        radius = int(sp.roundcorner.radius or 10)
        rounded_corners(image_path, radius)

    elif sp.githubupload:
        from .utils import githup_upload
        githup_upload(sp.githubupload.value)

    elif sp.smms:
        from .utils import smms_upload
        smms_upload(sp.smms.value)

    elif sp.youdao:
        from .utils import youdao_dict
        youdao_dict(sp.youdao.value)

    elif sp.find:
        from .utils import findfile
        print(sp.find.value, sp.find.directory or '.')
        findfile(sp.find.value, sp.find.directory or '.')

    elif sp.msg:
        from .oss import Message
        if sp.msg.write:
            Message().write(sp.msg.write)
        elif sp.msg.read:
            Message().read()
        elif sp.msg.value != PLACEHOLDER:
            Message().write(sp.msg.value)
        else:
            Message().read()

    elif sp.fund:
        from .fund import invest_advice, tgalert
        if sp.fund.buyalert: tgalert(sp.fund.buyalert)
        else:
            invest_advice(None if sp.fund.value ==
                          PLACEHOLDER else sp.fund.value)

    elif sp.stock:
        from .stock import Stock
        if sp.stock.value != PLACEHOLDER: Stock().trend(sp.stock.value)
        else: Stock().my_trend()

    elif sp.aes:
        from .toolkits.endecode import short_decode, short_encode

        text = sp.aes.value
        if sp.aes.encode: print(short_encode(text, sp.aes.encode))
        elif sp.aes.decode: print(short_decode(text, sp.aes.decode))

    else:
        from .data.msg import display_message
        display_message()


main = _main

if __name__ == '__main__':
    main()
