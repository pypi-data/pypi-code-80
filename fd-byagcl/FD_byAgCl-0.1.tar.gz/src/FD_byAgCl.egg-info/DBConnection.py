# coding = utf-8
import psycopg2, re, Request_Receiver
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
        if Need_dict.get('kw') is None:
            if re.findall('\\.' + Need_dict['mode'], temp_data[0]):
                data.append(temp_data)
                num += 1
        else:
            if re.findall(Need_dict['kw'], temp_data[0], re.I) and re.findall('\\.' + Need_dict['mode'], temp_data[0]):
                data.append(temp_data)
                num += 1
    return data