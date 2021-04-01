import json,os,time,re,requests,bs4


class mycitytree:
    def __init__(self, file_name):
        self.main_dic = {}
        self.mohu = {}
        self.add_file(file_name)

    def add_file(self, file_name):
        t = time.time()
        print("构建数据模型")
        with open(file_name, "r", encoding="utf8") as f:
            data = json.loads(f.read())
            self.data = data
            for province, citys in data.items():
                self.add(province)
                for city, xians in citys.items():
                    self.add(city)
                    for xian in xians:
                        self.add(xian)
                        h_xian = re.sub(
                            "(.{2,})[区市县州旗镇乡岛]$", lambda a: a.group(1), xian)
                        if h_xian != xian:
                            self.add(h_xian)
                            self.mohu[xian] = h_xian
        self.main_dic = {kk: [sorted(vv[0], reverse=True), vv[1]]
                         for kk, vv in self.main_dic.items()}
        print("加载模型耗时:", time.time()-t, "秒")

    def add(self, words):
        if len(words) < 2:
            return
        word_one = words[:2]
        word_str = words[2:]
        word_len = len(word_str)
        if word_one in self.main_dic:
            self.main_dic[word_one][0].add(word_len)
            self.main_dic[word_one][1].add(word_str)
        else:
            self.main_dic[word_one] = [{word_len}, {word_str}]

    def search(self, words):
        words = words.strip()
        words_len = len(words)
        if words_len < 2:
            return {}
        search_lis = {}
        word_start = 0
        while word_start < words_len-1:
            word_end = word_start+2
            word = words[word_start:word_end]
            word_start += 1
            if word in self.main_dic:
                last_len = words_len-word_end
                word_lens = self.main_dic[word][0]
                word_strs = self.main_dic[word][1]

                for word_len in word_lens:
                    if word_len > last_len:
                        continue
                    qg_str = words[word_end:word_end+word_len]
                    if qg_str in word_strs:
                        word_qg_str = word+qg_str
                        if word_qg_str in search_lis:
                            search_lis[word_qg_str] += 1
                        else:
                            search_lis[word_qg_str] = 1
                        word_start += word_len
                        break
        return search_lis


def get_city_files(file_name):
    main_url = "http://www.tcmap.com.cn/list/jiancheng_list.html"
    main_a = requests.get(main_url)
    main_html = bs4.BeautifulSoup(main_a.content.decode("gbk"), "html5lib")
    main_trs = main_html.find("div", {"id": "page_left"}).table.findAll("tr")
    zong = {}
    for main_tr in main_trs:
        province = main_tr.findAll("td")[1].get_text().replace("省", "").strip()
        if "香港" in province:
            province = "香港"
        if "内蒙古" in province:
            province = "蒙古"
        province_url = "http://www.tcmap.com.cn"+main_tr.a["href"]
        province_a = requests.get(province_url)
        province_html = bs4.BeautifulSoup(
            province_a.content.decode("gbk"), "html5lib")
        province_trs = province_html.find(
            "div", {"id": "page_left"}).table.findAll("tr")
        zong[province] = {}
        for province_tr in province_trs:
            province_tds = province_tr.findAll("td")
            city = province_tds[0].get_text().strip()
            if city and not re.search("^[东南西北中城河]{2}区$|^.区$|(产业|开发|示范|食品|名胜|示范|管理|工园)[区园]", city):
                city = re.sub("(.{2,})[市县州旗镇乡岛]$", lambda a: a.group(1), city)
                xians = [xian.strip(
                ) for xian in province_tds[-1].get_text().strip().split(" ") if xian.strip()]
                zong[province][city] = set()
                for xian in xians:
                    xian = re.sub("(.{2,})?自治.*", lambda a: a.group(1), xian)
                    xian = re.sub("[\(（].+?[\)）]$", "", xian)
                    if xian and not re.search("^[东南西北中城河]{2}区$|^.区$|(产业|开发|示范|食品|名胜|示范|管理|工园)[区园]", xian):
                        zong[province][city].add(xian)
                zong[province][city] = list(zong[province][city])
    with open(file_name, "wb") as f:
        f.write(json.dumps(zong).encode("gbk"))


class city_api():
    def __init__(self, file_name=None):
        self.tree = mycitytree(file_name)

    def get_province_tree(self, data):
        if not data:
            return []
        zong_tree = []
        for province, citys in self.tree.data.items():
            province_score = data.get(province, 0)
            for city, xians in citys.items():
                city_score = data.get(city, 0)
                for xian in xians:
                    xian_score = data.get(xian, 0)
                    h_xian = self.tree.mohu.get(xian)
                    h_xian_score = data.get(h_xian, 0) if h_xian else 0
                    zong = province_score+city_score+xian_score+h_xian_score
                    if zong > 0:
                        if h_xian_score:
                            zong_tree.append(
                                (province, province_score*5, city, city_score*2, xian, h_xian_score*1, True))
                        elif xian_score:
                            zong_tree.append(
                                (province, province_score*5, city, city_score*2, xian, xian_score*1, False))
                        elif city_score:
                            zong_tree.append(
                                (province, province_score*5, city, city_score*2, None, 0, False))
                        elif province_score:
                            zong_tree.append(
                                (province, province_score*5, None, 0, None, 0, False))
        zong_rs = []
        [zong_rs.append(ll) for ll in zong_tree if ll not in zong_rs]
        return zong_rs

    def get_fillter_province(self, data, h_province=None, h_city=None, h_xian=None, h_mh=None, bd=False):
        fen = 0
        rs = []
        for ll in data:
            province, province_score, city, city_score, xian, xian_score, mh = ll
            if not bd:
                if h_mh and not mh:
                    continue
                if not h_mh and mh:
                    continue
            if h_province and province not in h_province:
                continue
            if h_city and city not in h_city:
                continue
            if h_xian and xian not in h_xian:
                continue
            num = province_score+city_score+xian_score
            if fen == num:
                rs.append(ll)
            else:
                fen = num
                rs = [ll]
        return rs

    def bd_lls(self, lls, lls2):
        lls2 = self.get_fillter_province(lls2, bd=True)
        zong = []
        for ll in lls:
            province, province_score, city, city_score, xian, xian_score, mh = ll
            for ll2 in lls2:
                province2, province2_score, city2, city2_score, xian2, xian2_score, mh2 = ll2
                if province == province2:
                    if city:
                        city2, xian2 = city, xian
                    zong.append((province2, province2_score, city2,
                                 city2_score, xian2, xian2_score, mh2))
        return zong
    def xun_sorted(self,lls):
        lls=[list(ll) for ll in lls]
        for ll in lls:
            ll.append([1,1])
        for n,ll in enumerate(lls):
            for n2,ll2 in enumerate(lls):
                if n!=n2:
                    if ll[2]==ll2[2]:
                        ll[-1][0]+=1
                        ll2[-1][0]+=1

                        ll[-1][1]+=1
                        ll2[-1][1]+=1
                    elif ll[0]==ll2[0]:
                        ll[-1][0]+=1                    
                        ll2[-1][0]+=1
        lls = sorted(lls, key=lambda a: "".join([str(li) for li in a[-1]]))
        return lls


                    
        

                    
                
            




    def get_city(self, txt, h_zd=False):
        def get_xun(zd=True, h_province=None, h_city=None, h_xian=None, h_mh=None):
            if zd:
                lls = self.get_fillter_province(
                    h_zd_tree, h_province, h_city, h_xian, h_mh)
            else:
                lls = self.get_fillter_province(
                    txt_tree, h_province, h_city, h_xian, h_mh)
            if len(lls) == 1 and lls[0][5]:
                return lls
            if zd:
                if h_mh:
                    if lls:
                        lls2 = [hhs for province, province_score, city, city_score, xian, xian_score, mh in lls for hhs in get_xun(
                            zd=False, h_province=province, h_city=None, h_xian=None, h_mh=False)]
                        return self.bd_lls(lls, lls2) if lls2 else lls
                    else:
                        return get_xun(zd=False, h_province=h_province, h_city=h_city, h_xian=h_xian, h_mh=False)
                else:
                    if lls:
                        lls2 = [hhs for province, province_score, city, city_score, xian, xian_score, mh in lls for hhs in get_xun(
                            zd=True, h_province=province, h_city=None, h_xian=None, h_mh=True)]
                        return self.bd_lls(lls, lls2) if lls2 else lls
                    else:
                        return get_xun(zd=True, h_province=h_province, h_city=h_city, h_xian=h_xian, h_mh=True)
            else:
                if h_mh:
                    return lls
                else:
                    if lls:
                        lls2 = [hhs for province, province_score, city, city_score, xian, xian_score, mh in lls for hhs in get_xun(
                            zd=False, h_province=province, h_city=None, h_xian=None, h_mh=True)]
                        return self.bd_lls(lls, lls2) if lls2 else lls
                    else:
                        return get_xun(zd=False, h_province=h_province, h_city=h_city, h_xian=h_xian, h_mh=True)
        txt = re.sub("\s|北京时间", "", txt)
        h_zd = re.sub("\s|北京时间", "", h_zd) if h_zd else h_zd
        txt_tree = self.get_province_tree(self.tree.search(txt))
        if h_zd:
            h_zd_tree = self.get_province_tree(self.tree.search(h_zd))
            xun_rs=get_xun()
        else:
            xun_rs=get_xun(zd=False)
        return self.xun_sorted(xun_rs)

mycity = city_api(os.path.join(os.path.abspath(__file__),"../citys.py"))




