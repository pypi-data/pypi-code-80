import requests
import re
import time
import pandas as pd
from noti_hj3415 import telegram
import os
from sqlalchemy import create_engine

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def _make_first_url(sdate=None, edate=None, code=None, title=None) -> str:
    def _match_title_with_title_code(title: str) -> str:
        logger.info('<<<  _match_title_with_title_code() >>>')
        if title is None:
            title_code = None
        elif title in ['무상증자결정', '자기주식취득결정', '자기주식처분결정', '유상증자결정', '전환사채권발행결정',
                       '신주인수권부사채권발행결정', '교환사채권발행결정', '회사합병결정', '회사분할결정']:
            title_code = 'B' # 주요사항보고
        elif title in ['공급계약체결', '주식분할결정', '주식병합결정', '주식소각결정', '만기전사채취득', '신주인수권행사',
                       '소송등의', '자산재평가실시결정', '현물배당결정', '주식배당결정', '매출액또는손익구조', '주주총회소집결의']:
            title_code = 'I' # 거래소공시
        elif title in ['공개매수신고서', '특정증권등소유상황보고서', '주식등의대량보유상황보고서']:
            title_code = 'D' # 지분공시
        else:
            raise
        return title_code

    # 모든 인자를 생략할 경우 오늘 날짜의 공시 url를 반환한다.
    logger.info('<<<  _make_first_url() >>>')
    logger.info(f'corp_code : {code}\ttitle_code : {title}'
                f'\tstart_date : {sdate}\tend_date : {edate}')

    title_code = _match_title_with_title_code(title)

    # 최종 url을 만들기 위한 문장 요소들
    url = 'https://opendart.fss.or.kr/api/list.json'
    key = '?crtfc_key=f803f1263b3513026231f4eff69312165e6eda90'
    is_last = f'&last_reprt_at=Y'
    page_no = f'&page_no=1'
    page_count = f'&page_count=100'
    start_date = f'&bgn_de={sdate}' if sdate else ''
    end_date = f'&end_de={edate}' if edate else ''
    corp_code = f'&corp_code={code}' if code else ''
    pblntf_ty = f'&pblntf_ty={title_code}' if title_code else ''

    first_url = url + key + is_last + page_no + page_count + start_date + end_date + corp_code + pblntf_ty
    logger.info(f'first url : {first_url}')
    return first_url


def _make_dart_list(first_url: str, echo: bool) -> list:
    logger.info('<<<  _make_dart_list() start >>>')
    logger.info(f'first url : {first_url}')
    try:
        first_dict = requests.get(first_url).json()
    except requests.exceptions.ConnectionError:
        # 가끔 opendart접속이 안되는 경우가 있음.
        text = "Can't connect opendart.fss.or.kr.."
        logger.error(text)
        telegram.manager_bot(text)
        raise
    if first_dict['status'] != '000':
        raise Exception(first_dict['message'])
    total_page = first_dict['total_page']
    logger.info(f'total {total_page} page..')
    # reference from https://wikidocs.net/4308#match_1(정규표현식 사용)
    # [0-9]+ 숫자가 1번이상 반복된다는 뜻
    p = re.compile('&page_no=[0-9]+')
    list_raw_dict = []
    # 전체페이지만큼 반복하여 하나의 전체 공시리스트를 만들어 반환한다.
    if echo:
        print(f'Extracting pages({total_page}) ', end='', flush=True)
    for i in range(total_page):
        each_page_url = p.sub(f'&page_no={i + 1}', first_url)
        if echo:
            print(f'{i+1}..', end='', flush=True)
        list_raw_dict += requests.get(each_page_url).json()['list']
        time.sleep(1)
    if echo:
        print(f'total {len(list_raw_dict)} items..', flush=True)
    return list_raw_dict


def _make_df(items_list: list) -> pd.DataFrame:
    logger.info('<<<  _make_df() start >>>')
    # 전체데이터에서 Y(유가증권),K(코스닥)만 고른다.
    # reference by https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#selection-by-callable
    yk_df = pd.DataFrame(items_list).loc[lambda df: df['corp_cls'].isin(['Y', 'K']), :]
    logger.info(f'Count of df : {len(yk_df)}')
    return yk_df


def get_df(sdate=None, edate=None, code=None, title=None, restrict=True, echo=True) -> pd.DataFrame:
    # 공시는 오전 7시부터 오후 6시까지 나온다.
    logger.info('<<<  get_df() start >>>')
    restrict_words = ['기재정정', '첨부정정', '자회사의', '종속회사의', '기타경영사항']
    logger.info(f'restrict_words : {restrict_words}')
    if echo:
        print('Making a dataframe from dart website..')
        print(f'<<<<< Setting.. Code: {code}\tTitle:{title}\t'
              f'Start date: {sdate}\tEnd date: {edate} >>>>>')
    try:
        first_url = _make_first_url(sdate, edate, code, title)
        item_list = _make_dart_list(first_url, echo=echo)
        df = _make_df(item_list)
    except:
        return pd.DataFrame()
    if title is not None:
        df = df[df['report_nm'].str.contains(title, regex=False)]
    if restrict:
        for word in restrict_words:
            df = df[~df['report_nm'].str.contains(word, regex=False)]
    if echo:
        print(df.to_string())
    return df


def save_to_db(df: pd.DataFrame, db_fullpath: str, tablename: str, echo=False):
    if df.empty:
        print('Dataframe is empty..So we will skip saving db..')
        return 0
    dir_path = os.path.dirname(db_fullpath)

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    dsn = f"sqlite:///{db_fullpath}"
    engine = create_engine(dsn, echo=echo)

    # 테이블을 저장한다.
    print(f"Save dataframe on {tablename} table on {os.path.basename(db_fullpath)} ...", flush=True)
    df.to_sql(tablename, con=engine, index=False, if_exists='replace')
    return len(df)

