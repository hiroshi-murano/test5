from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sqlite3
import json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import qrcode
# from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import datetime
import uuid
import urllib.parse
from xml.sax.saxutils import unescape

DB = 'plot_data.sqlite3'

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def index(request):
    """
    """

    # day1 = datetime.date.today()    # 今日を取得(時間は含まず)
    day = datetime.datetime.today()
    day1 = day + datetime.timedelta(minutes=-10)
    day2 = day + datetime.timedelta(days=1)  # 1日加算

    str_day1 = day1.strftime("%Y-%m-%d %H:%M:%S")
    str_day2 = day2.strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cmd = "select * from sagyo_log where dt>='{}' and dt<'{}' ".format(
        str_day1, str_day2)
    print('---------')
    print(cmd)
    print('---------')
    cur.execute(cmd)
    lst = cur.fetchall()

    data_x = []
    data_y = []
    for row in lst:
        print(row)
        data_x.append(row[3])
        data_y.append(row[4])

    cur.close()
    conn.close()

    # data_x=['2019-04-18 16:00:00','2019-04-18 16:00:10','2019-04-18 16:00:13','2019-04-18 16:00:20',]
    # data_y=[1,0,1,0,]

    title = '({}) - ({})'.format(str_day1, str_day2)
    context = {'title': title,
               'data_x': data_x,
               'data_y': data_y}

    return render(request, 'app/index.html', context)


def data_input(request):
    """
    """

    context = {}

    return render(request, 'app/data_input.html', context)


def trace_input(request):
    """
    """

    if request.method == 'GET':
        user_id = request.GET['user_id']
        line = request.GET['line']
        kote = request.GET['kote']

        context = {'user_id': user_id, 'line': line, 'kote': kote}

        return render(request, 'app/trace_input.html', context)


def trace_list(request):
    """
    """

    if request.method == 'GET':
        user_id = request.GET['user_id']
        line = request.GET['line']

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cmd = "select *  from trace_data where user_id=? and line=? and date_time>=? order by id"

        # print('---------')
        # print(cmd)
        # print('---------')
        today = datetime.datetime.now()  # 現在の日時を取得
        cur.execute(cmd, [user_id, line, today.strftime("%Y/%m/%d")])
        lst = cur.fetchall()

        # print(lst)

        # for row in lst:
        #     print(row)
        #     data_x.append(row[3])
        #     data_y.append(row[4])

        cur.close()
        conn.close()

        context = {'data': lst}

        return render(request, 'app/trace_list.html', context)


@csrf_exempt
def api_01(request):
    """
    JSON返すAPI
    """

    method = request.method
    # print('メソッド={}'.format(method))

    if request.method == 'GET':
        keyword1 = request.GET['user_id']
        dt = request.GET['date']
        dictData = {}
        dictData['データ'] = '送信されたキーワードは「{}」です'.format(keyword1)
        dictData['date'] = '送信された時刻は「{}」です'.format(dt)

        json_str = json.dumps(dictData, ensure_ascii=False, indent=2,)
        status = 200
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
    elif request.method == 'POST':
        keyword1 = request.POST['keyword1']
        keyword2 = request.POST['keyword2']

        insert_date(keyword2, keyword1)

        dictData = {}
        dictData['データ'] = '送信されたキーワードは「{}+{}」です'.format(keyword1, keyword2)

        json_str = json.dumps(dictData, ensure_ascii=False, indent=2,)
        status = 200
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)


def insert_date(dt, status):
    """
    """

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    print('{} にステータス {} をインサートします'.format(dt, status))

    sql = "insert into sagyo_log('user_id','sagyo','dt','status') values (?,?,?,?)"
    # dt1=datetime.datetime.now()

    lstData = ['hoge', 'foo', dt, status]
    cur.execute(sql, lstData)
    conn.commit()

    cur.close()
    conn.close()


def qr_code(request):
    """
    """

    # url="|{0}://{1}|".format(request.scheme, request.get_host())
    # print(url)

    # url=HttpRequestRedirect(reverse('app1.views.first'))
    # print(url)

    # keywordがgetで与えられたとき(辞書のkeyが存在したら)
    if 'url' in request.GET:
        url = request.GET['url']
    else:
        url = None

    print('url={}'.format(url))

    if url != None:
        img = qrcode.make('http://' + url+'/app/data_input/')
    else:
        img = qrcode.make('http://www.yahoo.co.jp')

    # print(type(img))
    # print(img.size)
    # <class 'qrcode.image.pil.PilImage'>
    # (290, 290)

    u4 = str(uuid.uuid4())

    # today = datetime.datetime.now()  # 現在の日時を取得
    # img_file = today.strftime("%Y%m%d_%H%M%S")+'.png'  # datetimeのフォーマット
    img_file = u4+'.png'  # datetimeのフォーマット

    img.save('app/static/app/img/' + img_file)

    context = {'img_file': img_file}

    return render(request, 'app/qr_code.html', context)


def qr_code2(request):
    """
    """

    if 'url' in request.GET:
        url = request.GET['url']
    else:
        url = None

    print('url={}'.format(url))

    if url != None:
        url2 = urllib.parse.unquote(url)
        print('url2={}'.format(url2))

        url3 = unescape(url2)
        print('url3={}'.format(url3))

        img = qrcode.make(url3)
    else:
        img = qrcode.make('http://www.yahoo.co.jp')

    u4 = str(uuid.uuid4())

    # today = datetime.datetime.now()  # 現在の日時を取得
    # img_file = today.strftime("%Y%m%d_%H%M%S")+'.png'  # datetimeのフォーマット
    img_file = u4+'.png'  # datetimeのフォーマット

    img.save('app/static/app/img/' + img_file)

    context = {'img_file': img_file, 'url': url3}

    return render(request, 'app/qr_code.html', context)


@csrf_exempt
def api_02(request):
    """
    JSON返すAPI
    """

    print('postに来ました')

    if request.method == 'POST':
        user_id = request.POST['user_id']
        line = request.POST['line']
        kote = request.POST['kote']
        status = request.POST['status']
        data = request.POST['data']
        today = datetime.datetime.now()  # 現在の日時を取得
        date_time = today.strftime("%Y/%m/%d %H:%M:%S")
        pc_name = request.POST['pc_name']
        dictData = {}
        dictData['user_id'] = user_id
        dictData['line'] = line
        dictData['kote'] = kote
        dictData['status'] = status
        dictData['data'] = data
        dictData['date_time'] = date_time
        dictData['pc_name'] = pc_name

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        sql = "insert into trace_data('user_id', 'line', 'kote', 'status', 'data', 'date_time', 'pc_name')  values (?,?,?,?,?,?,?)"
        # dt1=datetime.datetime.now()

        lstData = [user_id, line, kote, status, data, date_time, pc_name]

        print(lstData)

        cur.execute(sql, lstData)
        conn.commit()

        cur.close()
        conn.close()

        json_str = json.dumps(dictData, ensure_ascii=False, indent=2,)
        status = 200

        return HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
