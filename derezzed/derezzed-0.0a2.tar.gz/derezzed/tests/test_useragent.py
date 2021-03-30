from nose.tools import assert_equal  # type: ignore

from derezzed.rechain import RegularExpressionChain
from derezzed.useragent import UserAgentApp
from derezzed.useragent import UserAgentOS


ua_app = UserAgentApp()
ua_os = UserAgentOS()


def check_useragent(ua_string: str, expected_app: str,
                    expected_os: str) -> None:
    print(f"uastring is {ua_string}")
    app = ua_app.match(ua_string, True)
    os = ua_os.match(ua_string, True)
    assert_equal((app, os), (expected_app, expected_os))


def test_useragent():
    tests = [
        # chrome
        ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36", "chrome", "linux"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", "chrome", "windows"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", "chrome", "windows"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", "chrome", "windows"),
        ("Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36","chrome", "windows"),
        ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36", "chrome", "linux"),
        ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36", "chrome", "linux"),
        ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/76.0.3803.0 Safari/537.36", "chrome", "linux"),
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36", "chrome", "mac os x"),
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36", "chrome", "mac os x"),
        ("Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36", "chrome", "android"),
        ("Mozilla/5.0 (Linux; Android 7.1.1; SM-T555 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.96 Safari/537.36", "chrome", "android"),
        ("Mozilla/5.0 (X11; CrOS armv7l 12105.100.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.144 Safari/537.36", "chrome", "chrome os"),
        ("Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36", "chrome", "freebsd"),
        # edge
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582", "edge", "windows"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577", "edge", "windows"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931", "edge", "windows"),
        ("Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHT(\"ML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393", "edge", "windows"),
        ("Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.9200", "edge", "windows"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586", "edge", "windows"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246", "edge", "windows"),
        ("Mozilla/5.0 (Windows Mobile 10; Android 8.0.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.92 Mobile Safari/537.36 Edge/40.15254.369", "edge", "winphone"),
        # firefox
        ("Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0", "firefox", "linux"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0", "firefox", "windows"),
        ("Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0", "firefox", "android"),
        ("Mozilla/5.0 (Linux; Android 8.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Focus/7.0.13 Chrome/70.0.3538.110 Mobile Safari/537.36", "firefox", "android"),
        ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0", "firefox", "windows"),
        ("Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0", "firefox", "windows"),
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0", "firefox", "mac os x"),
        ("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0", "firefox", "mac os x"),
        ("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0", "firefox", "linux"),
        ("Mozilla/5.0 (X11; Ubuntu i686; rv:52.0) Gecko/20100101 Firefox/52.0", "firefox", "linux"),
        ("Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0", "firefox", "linux"),
        ("Mozilla/5.0 (X11; OpenBSD i386; rv:72.0) Gecko/20100101 Firefox/72.0", "firefox", "openbsd"),
        ("Mozilla/5.0 (X11; FreeBSD amd64; rv:80.0) Gecko/20100101 Firefox/80.0", "firefox", "freebsd"),
        # opera
        ("Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2","opera", "linux"),
        ("Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16", "opera", "linux"),
        ("Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16", "opera", "mac os x"),
        ("Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14", "opera", "windows"),
        ("Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14", "opera", "windows"),
        ("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14", "opera", "windows"),
        ("Opera/9.80 (Android; Opera Mini/36.2.2254/119.132; U; id) Presto/2.12.423 Version/12.16", "opera", "android"),
        ("Opera/9.80 (Windows Mobile; Opera Mini/5.1.21594/28.2725; U; en) Presto/2.8.119 Version/11.10", "opera", "winphone"),
        # safari
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15", "safari", "mac os x"),
        ("Mozilla/5.0 (iPad; CPU OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1", "safari", "ios"),
        ("Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1", "safari", "ios"),
        ("Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1", "safari", "ios"),
        ("Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1", "safari", "ios"),
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15", "safari", "mac os x"),
        ("Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27", "safari", "mac os x"),
        ("Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27", "safari", "windows"),
        # IE
        ("Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko", "msie", "windows"),
        ("Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko", "msie", "windows"),
        ("Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)", "msie", "winphone"),
        ("Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)", "msie", "other"),
        # lynx
        ("Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1", "lynx", "other"),
        # curl
        ("curl/7.20.0 (x86_64-redhat-linux-gnu) libcurl/7.20.0 OpenSSL/0.9.8b zlib/1.2.3 libidn/0.6.5", "curl", "linux"),
        ("curl/7.21.3 (amd64-portbld-freebsd8.2) libcurl/7.21.3 OpenSSL/0.9.8q zlib/1.2.3", "curl", "freebsd"),
        ("curl/7.38.0", "curl", "other"),
        # wget
        ("Wget/1.12 (linux-gnu)", "wget", "linux"),
        ("Wget/1.16.1 (darwin14.0.0)", "wget", "mac os x"),
        ("Wget/1.10+devel", "wget", "other"),
        # android browser - TODO
        #("Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTT Build/LVY48F) CTV", "android browser", "android"),
        #("Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",  "android browser", "android"),
        # samsung browser
        ("Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/10.2 Chrome/71.0.3578.99 Mobile Safari/537.36", "samsung browser", "android"),
        # baidu box app
        ("Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 5.1.1)", "baidu box app", "android"),
        # UC browser
        ("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36", "uc browser", "android"),
        # watchOS
        ("server-bag [Watch OS,6.2.9,17U203,Watch2,3]", "other", "watch os"),
        ("Watch4,2/5.2.1 (16U113)", "other", "watch os"),
        # matrix
        ("Keanu_Example/0.1.0 (iPad; iOS 13.5; Scale/2.00)", "keanu", "ios"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Riot/1.6.7 Chrome/80.0.3987.134 Electron/8.0.3 Safari/537.36", "riot-desktop", "windows"),
        ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Riot/1.6.7 Chrome/80.0.3987.134 Electron/8.0.3 Safari/537.36", "riot-desktop", "linux"),
        ("Riot/0.11.5 (iPad; iOS 13.5; Scale/2.00)", "riot", "ios"),
        ("Riot/0.11.5 (iPhone; iOS 13.5.1; Scale/3.00)", "riot", "ios"),
        ("Riot.im/0.9.12 (Linux; U; Android 6.0.1; SM-J500FN Build/MMB29; Flavour GooglePlay; MatrixAndroidSDK 0.9.35", "riot.im", "android"),
        ("Zom 2/2.0.5 (iPad; iOS 13.5; Scale/2.00)", "zom", "ios"),
    ]
    for test in tests:
        yield check_useragent, test[0], test[1], test[2]
