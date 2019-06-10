from django.test import TestCase

# Create your tests here.
import sqlite3
import datetime
import random

DB = 'plot_data.sqlite3'


def dummy_data():
    """
    """

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
  
    sql="insert into sagyo_log('user_id','sagyo','dt','status') values (?,?,?,?)"
    # dt1=datetime.datetime.now()
    dt1 = datetime.datetime(2018, 2, 1, 12, 15, 30,0)
    for cnt in range(100):

        if cnt % 2==0:
            delta=15
        else:
            delta=2
            
        dt1 = dt1 + datetime.timedelta(seconds=delta)
        lstData=['hoge','foo',dt1,cnt % 2]
        cur.execute(sql, lstData)
        conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':


    dummy_data()
