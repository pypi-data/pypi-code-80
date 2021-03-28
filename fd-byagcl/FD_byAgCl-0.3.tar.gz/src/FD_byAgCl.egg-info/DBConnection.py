# coding = utf-8
import psycopg2, re, Request_Receiver, os, requests
def inst():
    conn = psycopg2.connect(database='firmware', user='root', password='root', host='118.126.65.110', port='5432')
    cursor = conn.cursor()
    print('Database connection completed, directing cursor...')
    sql = 'SELECT url FROM public.product'
    cursor.execute(sql)
    print('Cursor direction completed.')
    data = []
    Need_dict = Request_Receiver.Questions()
    num = 0
    while num <= Need_dict['num']:
        temp_data = cursor.fetchone()
        if temp_data is None:
            print('All searched.')
            break
        if re.findall('^ftp', temp_data[0]):
            continue
        if Need_dict.get('kw') is None:
            if re.findall('\\.' + Need_dict['mode'], temp_data[0])\
            and not os.path.isfile('./Firmwares/' + re.sub("',\\)", '', re.split('/', temp_data[0])[-1])):
                if int(requests.get(temp_data[0]).headers['Content-Length']) < 10240:
                    print("Length of ", temp_data[0], 'is too small, abandoned.')
                else:
                    data.append(temp_data[0])
                    num += 1
        else:
            if re.findall(Need_dict['kw'], temp_data[0], re.I) and re.findall('\\.' + Need_dict['mode'], temp_data[0])\
            and not os.path.isfile('./Firmwares/' + re.sub("',\\)", '', re.split('/', temp_data[0])[-1])):
                if int(requests.get(temp_data).headers['Content-Length']) < 10240:
                    print("Length of ", temp_data[0], 'is too small, abandoned.')
                else:
                    data.append(temp_data[0])
                    num += 1
    return data