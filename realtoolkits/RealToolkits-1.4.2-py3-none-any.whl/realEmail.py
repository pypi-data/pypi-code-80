# -*- coding: UTF-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formataddr

import smtplib, os, re


class realEmail(object):
    '''
    描述一个email邮件的类
    提供一封邮件通过smtp发送的全部信息
    '''

    '''
    类属性
    '''
    __MIMETable = { \
                   ''        :'application/octet-stream', \
                   '323'     :'text/h323', \
                   'acx'     :'application/internet-property-stream', \
                   'ai'      :'application/postscript', \
                   'aif'     :'audio/x-aiff', \
                   'aifc'    :'audio/x-aiff', \
                   'aiff'    :'audio/x-aiff', \
                   'asf'     :'video/x-ms-asf', \
                   'asr'     :'video/x-ms-asf', \
                   'asx'     :'video/x-ms-asf', \
                   'au'      :'audio/basic', \
                   'avi'     :'video/x-msvideo', \
                   'axs'     :'application/olescript', \
                   'bas'     :'text/plain', \
                   'bcpio'   :'application/x-bcpio', \
                   'bin'     :'application/octet-stream', \
                   'bmp'     :'image/bmp', \
                   'c'       :'text/plain', \
                   'cat'     :'application/vnd.ms-pkiseccat', \
                   'cdf'     :'application/x-cdf', \
                   'cer'     :'application/x-x509-ca-cert', \
                   'class'   :'application/octet-stream', \
                   'clp'     :'application/x-msclip', \
                   'cmx'     :'image/x-cmx', \
                   'cod'     :'image/cis-cod', \
                   'cpio'    :'application/x-cpio', \
                   'crd'     :'application/x-mscardfile', \
                   'crl'     :'application/pkix-crl', \
                   'crt'     :'application/x-x509-ca-cert', \
                   'csh'     :'application/x-csh', \
                   'css'     :'text/css', \
                   'dcr'     :'application/x-director', \
                   'der'     :'application/x-x509-ca-cert', \
                   'dir'     :'application/x-director', \
                   'dll'     :'application/x-msdownload', \
                   'dms'     :'application/octet-stream', \
                   'doc'     :'application/msword', \
                   'dot'     :'application/msword', \
                   'dvi'     :'application/x-dvi', \
                   'dxr'     :'application/x-director', \
                   'eps'     :'application/postscript', \
                   'etx'     :'text/x-setext', \
                   'evy'     :'application/envoy', \
                   'exe'     :'application/octet-stream', \
                   'fif'     :'application/fractals', \
                   'flr'     :'x-world/x-vrml', \
                   'gif'     :'image/gif', \
                   'gtar'    :'application/x-gtar', \
                   'gz'      :'application/x-gzip', \
                   'h'       :'text/plain', \
                   'hdf'     :'application/x-hdf', \
                   'hlp'     :'application/winhlp', \
                   'hqx'     :'application/mac-binhex40', \
                   'hta'     :'application/hta', \
                   'htc'     :'text/x-component', \
                   'htm'     :'text/html', \
                   'html'    :'text/html', \
                   'htt'     :'text/webviewhtml', \
                   'ico'     :'image/x-icon', \
                   'ief'     :'image/ief', \
                   'iii'     :'application/x-iphone', \
                   'ins'     :'application/x-internet-signup', \
                   'isp'     :'application/x-internet-signup', \
                   'jfif'    :'image/pipeg', \
                   'jpe'     :'image/jpeg', \
                   'jpeg'    :'image/jpeg', \
                   'jpg'     :'image/jpeg', \
                   'js'      :'application/x-javascript', \
                   'latex'   :'application/x-latex', \
                   'lha'     :'application/octet-stream', \
                   'lsf'     :'video/x-la-asf', \
                   'lsx'     :'video/x-la-asf', \
                   'lzh'     :'application/octet-stream', \
                   'm13'     :'application/x-msmediaview', \
                   'm14'     :'application/x-msmediaview', \
                   'm3u'     :'audio/x-mpegurl', \
                   'man'     :'application/x-troff-man', \
                   'mdb'     :'application/x-msaccess', \
                   'me'      :'application/x-troff-me', \
                   'mht'     :'message/rfc822', \
                   'mhtml'   :'message/rfc822', \
                   'mid'     :'audio/mid', \
                   'mny'     :'application/x-msmoney', \
                   'mov'     :'video/quicktime', \
                   'movie'   :'video/x-sgi-movie', \
                   'mp2'     :'video/mpeg', \
                   'mp3'     :'audio/mpeg', \
                   'mpa'     :'video/mpeg', \
                   'mpe'     :'video/mpeg', \
                   'mpeg'    :'video/mpeg', \
                   'mpg'     :'video/mpeg', \
                   'mpp'     :'application/vnd.ms-project', \
                   'mpv2'    :'video/mpeg', \
                   'ms'      :'application/x-troff-ms', \
                   'mvb'     :'application/x-msmediaview', \
                   'nws'     :'message/rfc822', \
                   'oda'     :'application/oda', \
                   'p10'     :'application/pkcs10', \
                   'p12'     :'application/x-pkcs12', \
                   'p7b'     :'application/x-pkcs7-certificates', \
                   'p7c'     :'application/x-pkcs7-mime', \
                   'p7m'     :'application/x-pkcs7-mime', \
                   'p7r'     :'application/x-pkcs7-certreqresp', \
                   'p7s'     :'application/x-pkcs7-signature', \
                   'pbm'     :'image/x-portable-bitmap', \
                   'pdf'     :'application/pdf', \
                   'pfx'     :'application/x-pkcs12', \
                   'pgm'     :'image/x-portable-graymap', \
                   'pko'     :'application/ynd.ms-pkipko', \
                   'pma'     :'application/x-perfmon', \
                   'pmc'     :'application/x-perfmon', \
                   'pml'     :'application/x-perfmon', \
                   'pmr'     :'application/x-perfmon', \
                   'pmw'     :'application/x-perfmon', \
                   'pnm'     :'image/x-portable-anymap', \
                   'pot'     :'application/vnd.ms-powerpoint', \
                   'ppm'     :'image/x-portable-pixmap', \
                   'pps'     :'application/vnd.ms-powerpoint', \
                   'ppt'     :'application/vnd.ms-powerpoint', \
                   'prf'     :'application/pics-rules', \
                   'ps'      :'application/postscript', \
                   'pub'     :'application/x-mspublisher', \
                   'qt'      :'video/quicktime', \
                   'ra'      :'audio/x-pn-realaudio', \
                   'ram'     :'audio/x-pn-realaudio', \
                   'ras'     :'image/x-cmu-raster', \
                   'rgb'     :'image/x-rgb', \
                   'rmi'     :'audio/mid', \
                   'roff'    :'application/x-troff', \
                   'rtf'     :'application/rtf', \
                   'rtx'     :'text/richtext', \
                   'scd'     :'application/x-msschedule', \
                   'sct'     :'text/scriptlet', \
                   'setpay'  :'application/set-payment-initiation', \
                   'setreg'  :'application/set-registration-initiation', \
                   'sh'      :'application/x-sh', \
                   'shar'    :'application/x-shar', \
                   'sit'     :'application/x-stuffit', \
                   'snd'     :'audio/basic', \
                   'spc'     :'application/x-pkcs7-certificates', \
                   'spl'     :'application/futuresplash', \
                   'src'     :'application/x-wais-source', \
                   'sst'     :'application/vnd.ms-pkicertstore', \
                   'stl'     :'application/vnd.ms-pkistl', \
                   'stm'     :'text/html', \
                   'svg'     :'image/svg+xml', \
                   'sv4cpio' :'application/x-sv4cpio', \
                   'sv4crc'  :'application/x-sv4crc', \
                   'swf'     :'application/x-shockwave-flash', \
                   't'       :'application/x-troff', \
                   'tar'     :'application/x-tar', \
                   'tcl'     :'application/x-tcl', \
                   'tex'     :'application/x-tex', \
                   'texi'    :'application/x-texinfo', \
                   'texinfo' :'application/x-texinfo', \
                   'tgz'     :'application/x-compressed', \
                   'tif'     :'image/tiff', \
                   'tiff'    :'image/tiff', \
                   'tr'      :'application/x-troff', \
                   'trm'     :'application/x-msterminal', \
                   'tsv'     :'text/tab-separated-values', \
                   'txt'     :'text/plain', \
                   'uls'     :'text/iuls', \
                   'ustar'   :'application/x-ustar', \
                   'vcf'     :'text/x-vcard', \
                   'vrml'    :'x-world/x-vrml', \
                   'wav'     :'audio/x-wav', \
                   'wcm'     :'application/vnd.ms-works', \
                   'wdb'     :'application/vnd.ms-works', \
                   'wks'     :'application/vnd.ms-works', \
                   'wmf'     :'application/x-msmetafile', \
                   'wps'     :'application/vnd.ms-works', \
                   'wri'     :'application/x-mswrite', \
                   'wrl'     :'x-world/x-vrml', \
                   'wrz'     :'x-world/x-vrml', \
                   'xaf'     :'x-world/x-vrml', \
                   'xbm'     :'image/x-xbitmap', \
                   'xla'     :'application/vnd.ms-excel', \
                   'xlc'     :'application/vnd.ms-excel', \
                   'xlm'     :'application/vnd.ms-excel', \
                   'xls'     :'application/vnd.ms-excel', \
                   'xlt'     :'application/vnd.ms-excel', \
                   'xlw'     :'application/vnd.ms-excel', \
                   'xof'     :'x-world/x-vrml', \
                   'xpm'     :'image/x-xpixmap', \
                   'xwd'     :'image/x-xwindowdump', \
                   'z'       :'application/x-compress', \
                   'zip'     :'application/zip'} # MIME类型字典
    __re_email = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$') # email地址合法性检查正则表达式
    __re_srv   = re.compile(r'^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$') # smtp服务器地址合法性检查正则表达式

    '''
    类方法
    '''
    @classmethod
    def __addr_list2dict(cls, addrs, names):
        '''
        根据严格匹配的addr列表和name列表，生成对应的地址信息字典
        :param addrs: list/tuple形式的收件人地址信息
                      合法元素必须为不存在复合的地址字符串
                      不满足条件的字符串和对应的name字符串都会被抛弃
        :param names: list/tuple形式的收件人名称信息
                      必须于addrs完全匹配，否则视作None，允许为None
                      合法元素必须为非复合的名称字符串
        :return:
            生成有效信息   地址信息字典 {addr:Name, ...}
            未生成有效信息 None
        '''
        if not isinstance(addrs, (list, tuple)) or 0==len(addrs):
            # 地址信息必须是list或tuple，且元素数量不能为0
            return None
        if not isinstance(names, (list, tuple)) or len(names)!=len(addrs):
            # 格式不正确，或不满足addrs对name的长度约束，抛弃names
            names = None
        # 配对addr和name，生成dict
        anDict = {}
        if names is None:
            # 如果没有提供names信息，直接按 addr:None 的形式整理
            for eachAddr in addrs:
                if cls.__valid_addr(eachAddr):
                    # 合法的addr才存储
                    # 如果同名的元素已经存在，则新出现的将替代老的
                    anDict[eachAddr] = None
        else:
            # 如果提供了names信息，则一一对应整理成 addr:name 形式
            idx = 0
            for eachAddr in addrs:
                if cls.__valid_addr(eachAddr):
                    # 合法的addr才存储
                    # 如果同名的元素已经存在，则新出现的将替代老的
                    anDict[eachAddr] = None if (not isinstance(names[idx], str)) or ''==names[idx].strip() else names[idx]
                idx += 1
        return None if 0==len(anDict) else anDict

    @classmethod
    def __addr_str2dict(cls, addrStr, nameStr):
        '''
        本函数针对 地址字符串/名称字符串 可能为复合结构的场景
        通过将绑定的addr和name字符串做一次以','为分割的split的方式获取下层结构
        然后生成形如 {addr:Name, ...} 的地址信息字典
        :param addrStr: 收件人地址字符串，允许是以','为分割的多个地址
        :param nameStr: 收件人名称字符串，允许是以','为分割的多个名称
                        必须与addrStr严格匹配，否则视作None，允许为None
        :return:
            生成有效信息   地址信息字典 {addr:Name, ...}
            未生成有效信息 None
        '''
        if not isinstance(addrStr, str):
            # addr必须是字符串
            return None
        if not isinstance(nameStr, str):
            # name可以不存在
            # 如果遇到非法的name（非字符串），则将其置为None
            nameStr = None
        # 按逗号切分addr、name信息
        # 切分之前先除去所有的空格
        addrs = addrStr.replace(' ', '').split(',')
        names = None if nameStr is None else nameStr.replace(' ', '').split(',')
        # 根据切分结果生成元素为 addr:name 的dict
        return cls.__addr_list2dict(addrs, names)

    @classmethod
    def __format_reveivers(cls, recvInfo):
        '''
        将传入的收件人信息转换成reveiver信息字典{addr:name, ...}
        :param recvInfo: 邮件接收人信息，必须是一个带格式的字符串，允许的格式如下
                         'addr'
                         'addr;addr;...'
                         'addr,name'
                         'addr,name;addr,name;...'
                         'addr;addr;...,name;name;...'
                         隐含的约束是
                             当地址与名称同时存在时addr一定在name之前
                             addr与name必须严格匹配
                             逗号用于分割addr和对应的name，分号用于分割收件人
        :return:
            recvInfo内存在有效信息   地址信息字典 {addr:name, ...}
            recvInfo内不存在有效信息 None
        '''
        if not isinstance(recvInfo, str):
            # 不是字符串
            return None
        # recvInfo整形：剔除空格、strip掉两端的逗号和分号
        recvInfo = recvInfo.replace(' ', '')
        headAt = -1 # 包含，与切片规则一致
        tailAt = -1 # 不包含，与切片规则一致
        for idx in range(len(recvInfo)):
            if recvInfo[idx] not in (',', ';'):
                headAt = idx
                tailAt = idx+1
                break
        if -1 == headAt:
            # 整形失败，strip了逗号和分号之后，变成了空串
            return None
        for idx in range(headAt+1, len(recvInfo)):
            if recvInfo[idx] not in (',', ';'):
                tailAt = idx+1
        recvInfo = recvInfo[headAt:tailAt]
        if len(recvInfo)<3:
            # 整形失败，strip了逗号和分号之后，剩下的不足以构成一个最短的邮件地址
            return None
        # 比较字符串中逗号和分号的位置
        # 以大致判断字符串的类型
        commaAt = recvInfo.find(',')
        semiAt  = recvInfo.find(';')
        if commaAt<0 and semiAt<0:
            # addr 类型
            return cls.__addr_str2dict(recvInfo, None)
        elif commaAt<0 and semiAt>0:
            # addr;addr;... 类型
            return cls.__addr_str2dict(recvInfo, None)
        elif commaAt>0 and semiAt<0:
            # addr,name 类型
            return cls.__addr_str2dict(recvInfo, None)
        elif commaAt<semiAt:
            # addr,name;addr,name;... 类型
            pass
        else:
            # addr;addr;...,name;name;... 类型
            pass

    @classmethod
    def __fmt_recv(cls, recvItem):
        '''
        将一个收件人信息转换成reveiver信息字典{addr:name, ...}
        :param recvItem:  "一个收件人信息"，允许表示成以下格式
            - 地址字符串，支持多个地址以逗号分割的复合
            - 列表/元组，固定为（地址字符串，名称字符串）形式，地址字符串/名称字符串均支持复合，但需匹配一致
            - 字典（'addr':地址字符串，'name':名称字符串），地址字符串/名称字符串均支持复合，但需匹配一致
            未在上面列出的形式均视为非法
        :return:
            生成有效信息   地址信息字典 {addr:name, ...}
            未生成有效信息 None
        '''
        if isinstance(recvItem, str):
            # 如果收件人信息只是一个字符串
            # 则直接生成对应的 {addr:None, ...}
            return cls.__addr_str2dict(recvItem, None)
        if isinstance(recvItem, dict) and 'addr' in recvItem:
            # 如果收件人信息是个字典
            # 则根据addr的类型进行处理
            if isinstance(recvItem['addr'], str):
                # 如果addr的值的类型是字符串
                # 直接当作addr字符串进行拆解并生成dict
                # 如果addr的值的内容不是合法的addr字符串，则终止解析此dict，返回None
                return cls.__addr_str2dict(recvItem['addr'], recvItem['name'] if 'name' in recvItem else None)
            elif isinstance(recvItem['addr'], (list, tuple)):



            if 'name' in recvItem and isinstance(recvItem['name'], str) and '' != recvItem['name'].strip():
                return recvItem['addr'], recvItem['name']
            else:
                return recvItem['addr'], None

    @classmethod
    def __fmt_recvs(cls, recvInfo):
        '''
        将传入的收件人信息转换成reveiver信息字典{addr:name, ...}
        :param recvInfo: 收件人信息允许以如下格式传入
            - 地址字符串
            - 列表/元组/集合，元素允许为 地址字符串、形态为（地址字符串，名称字符串）的列表/元组、字典
            - 字典（'addr':地址字符串，'name':名称字符串）
        :return:
            生成有效信息   地址信息字典 {addr:name, ...}
            未生成有效信息 None
        '''
        if isinstance(recvInfo, (str, dict)):
            # 如果传入的收件人信息是字符串或字典格式
            # 则判定为单个收件人
            # 直接根据 __fmt_recv() 的结果生成recveiver信息字典
            tmpAL = cls.__fmt_recv(recvInfo)
            return None if tmpAL is None else {tmpAL[0]:tmpAL[1]}
        if isinstance(recvInfo, (list, tuple, set)) and len(recvInfo)>0:
            # 如果传入的收件人信息是列表/元组/集合
            # 则取出其中每一个元素，转换成合法的reveiver信息
            allRecvs = {}
            for recvItem in recvInfo:
                tmpAL = cls.__fmt_recv(recvItem)
                if tmpAL is None:
                    # 该item非法，无法转换
                    continue
                if tmpAL[0] not in allRecvs or allRecvs[tmpAL[0]] is None:
                    # 转换成功，并且之前不存在此收件人（或收件人信息为None）
                    # 记录该收件人信息
                    allRecvs[tmpAL[0]] = tmpAL[1]
            return None if 0==len(allRecvs) else allRecvs
        else:
            # 非法reveiver信息
            return None

    @classmethod
    def __format_addr(cls, addr, name):
        '''
        将一个addr/name信息转换成smtp addr格式字符串
        :param addr: 收件人地址
        :param name: 收件人名称
        :return:
            成功 返回addr<name>格式的地址
            失败 返回None
        '''
        if not cls.__valid_addr(addr):
            # 自己保证参数的合法性
            # 非法返回None
            return None
        if isinstance(name, str) and '' != name.strip():
            # 有name信息，直接添加到addr
            return formataddr((Header(name, 'utf-8').encode(), addr))
        else:
            # 没有name信息，用'unknown'替代
            return formataddr((Header('unknown', 'utf-8').encode(), addr))

    @classmethod
    def __format_addrs(cls, recvDict):
        '''
        将收件人字典转换成smtp addr格式
        :param recvDict: 收件人字典 {addr:name, ...}
        :return:
            成功 smtp addr格式字符串，如果存在多个地址以逗号分割
            失败 None
        '''
        if not isinstance(recvDict, dict):
            return None
        fmtAddrs = ''
        for addr in recvDict:
            tmpAddr = cls.__format_addr(addr, recvDict[addr])
            if tmpAddr is None:
                continue
            if len(fmtAddrs)>0:
                fmtAddrs += ' , '
            fmtAddrs += tmpAddr
        return None if 0==len(fmtAddrs) else fmtAddrs

    @classmethod
    def __valid_addr(cls, addr):
        '''
        检查是否是合法的email地址
        :param addr: 需要判断是否是合法邮件地址的字符串
        :return:
            合法 True
            非法 False
        '''
        if not isinstance(addr, str):
            return False
        if cls.__re_email.match(addr):
            return True
        else :
            return False

    @classmethod
    def __valid_srv(cls, srv):
        '''
        检查是否是合法的服务器域名
        :param srv: 需要判断是否合法的服务器域名（不包含协议信息）
        :return:
            合法 True
            非法 False
        '''
        if not isinstance(srv, str):
            return False
        if cls.__re_srv.match(srv):
            return True
        else :
            return False

    @classmethod
    def __valid_attachment(cls, att):
        '''
        检查是否是合法的邮件附件信息
        :param att: 附件信息字典
        :return:
            合法 True
            非法 False
        '''
        if not isinstance(att, dict):
            return False
        if 'type' not in att or not isinstance(att['type'], str):
            return False
        if 'filename' not in att or not isinstance(att['filename'], str):
            return False
        if not os.path.isfile(att['filename']):
            return False
        return True

    @classmethod
    def __format_attachment(cls, attItem):
        #
        return None



    # 类成员函数定义

    def __init__(self, **kwargs):
        super(realEmail, self).__init__()
        # 邮件基本信息
        # TODO: to addr、form addr不能直接用，要改成 __xx，前面搞错了，后面的desc属性名称也不对，需要该
        self.__from_addr  =  None # 发送者，形如{addr:Name, ...}，只有一个元素
        self.smtp_pwd     =  None # 发送者密码
        self.smtp_srv     =  None # SMTP服务器
        self.__to_addrs   =  None # 主送，{addr:Name, ...}，可以有多个元素
        self.__cc_addrs   =  None # 抄送，{addr:Name, ...}，可以有多个元素
        self.__bcc_addrs  =  None # 秘送，{addr:Name, ...}，可以有多个元素
        self.recv_to      =  None # 收件人列表（主送）
        self.recv_cc      =  None # 收件人列表（抄送）
        self.recv_bcc     =  None # 收件人列表（密送）
        self.__mail_text  =  None # 邮件正文
        self.__text_type  =  None # 正文类型
        self.__att_list   =  None # 附件列表
        self.mail_title   =  ''   # 邮件标题
        # 邮件基本信息初始化
        if 'from' in kwargs:
            # 发件人信息
            self.__from_addr = self.__format_addrs(kwargs['from'])
        if 'pwd' in kwargs and isinstance(kwargs['pwd'], str):
            # 密码目前不控制长度
            self.smtp_pwd = kwargs['pwd']
        if 'srv' in kwargs and self.__valid_srv(kwargs['srv']):
            # smtp服务器必须是合法的域名字符串
            self.smtp_srv = kwargs['srv']
        if 'to' in kwargs:
            # 生成主送smtp addr
            self.__to_addrs = self.__format_addrs(kwargs['to'])
        if 'cc' in kwargs and isinstance(kwargs['cc'], (list, tuple, set)):
            # 生成抄送smtp addr
            self.__to_addrs = self.__format_addrs(kwargs['cc'])
        if 'bcc' in kwargs and isinstance(kwargs['bcc'], (list, tuple, set)):
            # 生成密送smtp addr
            self.__to_addrs = self.__format_addrs(kwargs['bcc'])
        if 'text' in kwargs and isinstance(kwargs['text'], str):
            # 邮件正文必须是字符串
            self.__mail_text = kwargs['text']
        if 'type' in kwargs and kwargs['type'] in ('plain', 'html'):
            # 邮件正文类型必须是'plain'或'html'
            self.__text_type = kwargs['type']
        if 'attachment' in kwargs and isinstance(kwargs['attachment'], (list, tuple, set)):
            # 附件信息以列表/元组/集合的形式提供，支持一个或多个附件
            fns  = set() # 缓存附件文件名，用于去重
            atts = []    # 缓存挑选出来的合法附件信息
            for att in kwargs['attachment']:
                # 检查每一个传入的附件信息是否合法
                if not self.__valid_attachment(att):
                    # 不合法就抛弃
                    continue
                if att['filename'] in fns:
                    # 如果文件重复了，也抛弃
                    continue
                # 是合法且未重复的附件信息
                fns.add(att['filename']) # 记录其文件名，用于后续去重
                atts.append({'type':att['type'], 'filename':att['filename']}) # 缓存该合法的附件信息(不直接存传进来的dict)
            if len(atts)>0:
                # 如果从传入的附件信息中找到了合法信息，则转存到对应的实例属性
                self.__att_list = atts
        elif 'attachment' in kwargs and isinstance(kwargs['attachment'], dict):
            # 只有一个附件时，附件信息可以以dict形式提供
            if self.__valid_attachment(kwargs['attachment']):
                # 如果附件信息合法，直接存储到对应的实例属性
                # 存储方式为提取数据重新生成，不直接存传进来的dict
                self.__att_list = [{'type':kwargs['attachment']['type'], 'filename':kwargs['attachment']['filename']}]
        return

    def valid(self):
        # 检查当前email实例是否信息完整、合法
        if self.__from_addr is None:
            return False
        if self.smtp_pwd  is None:
            return False
        if self.smtp_srv  is None:
            return False
        if self.recv_to is None and self.recv_cc is None and self.recv_bcc is None:
            return False
        if self.__mail_text is None or self.__text_type is None:
            return False
        return True

    # 类属性定义
    def get_MIME(self):
        # 获取次email实例的MIME信息
        if not self.valid():
            # 自身数据还不合法/不完整
            # 无法生成MIME信息
            return None
        msg = MIMEMultipart()
        msg.attach(MIMEText(self.__mail_text, self.__text_type, 'utf-8'))
        msg['From'] = self.format_addr('{} <{}>'.format(self.__from_lable, self.from_addr))
    strTo = ""
    for addr in to_addrs:
        tmpName = "unknown"
        if addr in nameDict:
            tmpName = nameDict[addr]
        if len(strTo)>0:
            strTo += ','
        strTo += sendAlarmWorker._format_addr('{} <{}>'.format(tmpName, addr))
    msg['To'] = strTo
    msg['Subject'] = Header('[{}] 平台预警 (自动)'.format(dateStr), 'utf-8').encode()
        return None



'''
发送预警邮件
'''
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def sendMail(self, eMailStr, cType, toList, ctoList, btoList, attachList):
    # 检查对应的html、附件是否都存在
    dayFilePath = os.path.join(self.wCfg.getCfgValue('sysWebpageRoot'), 'noticehistory')
    htmlFileN = os.path.join(dayFilePath, '{}.html'.format(dateStr))
    attFileN  = os.path.join(dayFilePath, 'dl_att/{}.xlsx'.format(dateStr))
    if not os.path.exists(htmlFileN):
        return False
    if not os.path.exists(attFileN):
        return False

    # 邮件服务信息
    from_addr = "message@deepwatertech.net"
    password = "Jk235TtQN+"
    to_addrs = ["20913824@qq.com", "ljd791@qq.com"] # 收件人列表
    bto_addrs = []  # 密送列表
    nameDict = {"20913824@qq.com": "Real He", "ljd791@qq.com": "李君达"}
    smtp_server = "smtp.mxhichina.com"

    # 读取html内容到mailStr
    try:
        with open(htmlFileN, 'rb') as htmlFile:
            mailStr = htmlFile.read().decode('utf-8')
    except Exception as err:
        ...

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    mimeAtt = None
    with open(attFileN, 'rb') as attF:
        mimeAtt = MIMEBase('excel', 'xlsx', filename='test.png')
        mimeAtt.add_header('Content-Disposition', 'attachment', filename='{}.xlsx'.format(dateStr))
        mimeAtt.add_header('Content-ID', '<0>')
        mimeAtt.add_header('X-Attachment-Id', '0')
        mimeAtt.set_payload(attF.read())
        encoders.encode_base64(mimeAtt)

    # 生成邮件
    msg = MIMEMultipart()
    msg.attach(MIMEText(mailStr, 'html', 'utf-8'))
    msg['From'] = sendAlarmWorker._format_addr('标准投资 <{}>'.format(from_addr))
    strTo = ""
    for addr in to_addrs:
        tmpName = "unknown"
        if addr in nameDict:
            tmpName = nameDict[addr]
        if len(strTo)>0:
            strTo += ','
        strTo += sendAlarmWorker._format_addr('{} <{}>'.format(tmpName, addr))
    msg['To'] = strTo
    msg['Subject'] = Header('[{}] 平台预警 (自动)'.format(dateStr), 'utf-8').encode()
    msg.attach(mimeAtt)

    # 发送邮件
    rlst = None
    try:
        to_addrs.extend(bto_addrs)
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(0)
        server.login(from_addr, password)
        rlst = server.sendmail(from_addr, to_addrs, msg.as_string())
        server.quit()
    except Exception as err:
        return False
    else:
        if isinstance(rlst, dict) and len(rlst)>0:
            return False
    return True