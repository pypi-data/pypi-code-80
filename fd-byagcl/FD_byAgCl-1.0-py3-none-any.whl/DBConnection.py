# coding = utf-8
import psycopg2, re, Request_Receiver, os, requests, sys
def inst():
    if not os.path.isfile('./url_src.txt'):
        print('It seems that you don\'t have the resource of urls, they will be downloaded soon.')
        conn = psycopg2.connect(database='firmware', user='root', password='root', host='118.126.65.110', port='5432')
        cursor = conn.cursor()
        print('Database connection completed, directing cursor...')
        sql = 'SELECT url FROM public.product'
        cursor.execute(sql)
        print('Cursor direction completed.')
        all_url = cursor.fetchall()
        file = open('url_src.txt', 'w', encoding='utf-8')
        for url in all_url:
            file.write(url[0] + '\n')
        print('URL data downloaded.')
        file.close()
    else:
        print('You have the resource of URLs in the database, so you don\'t have to connect to it again.')
    src = open('./url_src.txt', 'r', encoding='utf-8')
    all_url = src.read().split('\n')
    Need_dict = Request_Receiver.Questions()
    num = 0
    url_foot = 0
    data = []
    src.close()
    while num <= Need_dict['num']:
        src = open('./url_src.txt', 'r', encoding='utf-8')
        if url_foot >= len(all_url):
            print('All searched.')
            break
        temp_data = all_url[url_foot]
        sys.stdout.write('\b' * 40 + 'Searching process: %d / %d URLs' % (url_foot + 1, len(all_url)))
        if re.findall('^ftp', temp_data):
            url_foot += 1
            src.close()
            continue
        if Need_dict.get('kw') is None:
            if re.findall('\\.' + Need_dict['mode'], temp_data):
                if os.path.isfile('./Firmwares/' + re.sub("',\\)", '', re.split('/', temp_data)[-1])):
                    print('\nThis file ' + temp_data + ' was already downloaded.')
                else:
                    length = int(requests.get(temp_data).headers['Content-Length'])
                    if length < 10240:
                        print("\nLength of ", temp_data, 'is too small(' + str(length) + ' B), abandoned.')
                        delete_line(src, temp_data)
                        print('This invalid url was removed from the resource file.')
                    else:
                        data.append(temp_data)
                        num += 1
        else:
            if re.findall(Need_dict['kw'], temp_data, re.I) and re.findall('\\.' + Need_dict['mode'], temp_data):
                if os.path.isfile('./Firmwares/' + re.sub("',\\)", '', re.split('/', temp_data)[-1])):
                    print('\nThis file ' + temp_data + ' was already downloaded.')
                else:
                    if int(requests.get(temp_data).headers['Content-Length']) < 10240:
                        print("\nLength of ", temp_data, 'is too small, abandoned.')
                        delete_line(src, temp_data)
                        print('This invalid url was removed from the resource file.')
                    else:
                        data.append(temp_data)
                        num += 1
        url_foot += 1
        src.close()
    return data
def delete_line(file, string):
    file_bcp = open('url_src_bcp.txt', 'w', encoding='utf-8')
    line_list = file.readlines()
    line_list.remove(string + '\n')
    file.close()
    os.remove(file.name)
    for line in line_list:
        file_bcp.write(line)
    file_bcp.close()
    os.rename('url_src_bcp.txt', 'url_src.txt')
