#!/usr/bin/env python3
# usage example(s)

import sqlalchemy as sa
import treedb

treedb.configure(log_sql=True)

print(next(treedb.iterlanguoids()))

engine = treedb.load()

# run sanity checks
treedb.check()

treedb.print_rows(sa.select(treedb.Languoid).order_by('id').limit(5))

query = treedb.get_query()  # big example query containing 'everything'

df = treedb.pd_read_sql(query, index_col='id')
if df is not None:
    df.info()

#treedb.write_csv()

#treedb.write_languoids()

#treedb.files.roundtrip()

#import treedb.raw
#print(next(treedb.raw.fetch_records()))
#treedb.raw.write_files()
