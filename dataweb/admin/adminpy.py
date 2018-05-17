from urllib import parse
from flask import render_template, request, session, redirect, flash, jsonify, send_from_directory, send_file, make_response
from dataweb.admin import admin
from dataweb.database import *
import time, json, os, xlsxwriter
from flask_login import login_required
from flask_uploads import  UploadSet, configure_uploads, DOCUMENTS, patch_request_class
from io import BytesIO
from dataweb import xdocs
import config
import re

#创建学员的字典
def creatsdic(i):
    d = dict()
    d['id'] = i.id
    d['name'] = i.name
    d['iden'] = i.iden
    d['birth_y'] = i.birth_y
    d['birth_m'] = i.birth_m
    d['birth_d'] = i.birth_d
    d['telephone'] = i.telephone
    d['phone'] = i.phone
    d['address'] = i.address
    d['em_name'] = i.em_name
    d['em_tel'] = i.em_tel
    d['em_phone'] = i.em_phone
    return d

#创建课程的字典
def creatcdic(i):
    d = dict()
    d['id'] = i.id
    d['name'] = i.name
    d['course_class'] = i.course_class
    d['times'] = i.times
    d['duration'] = i.duration
    d['summary'] = i.summary
    d['teacher'] = i.teacher
    d['region'] = i.region
    d['limit'] = i.limit
    d['year'] = i.year
    d['cost'] = i.cost
    d['start_m'] = i.start_m
    d['start_w'] = i.start_w
    d['start_d'] = i.start_d
    d['start_t'] = i.start_t
    return d

def creatsddd(jsonmessage):
    #xxx只包含id信息
    dddp = json.loads(parse.unquote(jsonmessage))
    did = dddp['id']
    item = Students.query.filter(Students.id == did).first()
    ddd = creatsdic(item)
    return ddd

def creatcddd(jsonmessage):
    #xxx只包含id信息
    dddp = json.loads(parse.unquote(jsonmessage))
    did = dddp['id']
    item = Courses.query.filter(Courses.id == did).first()
    ddd = creatcdic(item)
    return ddd

@admin.route('/test', methods=['GET', 'POST'])
def sd1ownload():
    if request.method == 'POST':
        if 'xdoc1' in request.files:
            xdocs.save(request.files['xdoc1'])
        if 'xdoc2' in request.files:
            xdocs.save(request.files['xdoc2'])
        return redirect('admin/test')
    return render_template('main/tttest.html')


#    return render_template('main/tttest.html')

@admin.route('/test/U_Have_A_Message<xxx>')
def tttest(xxx):
    dict2 = json.loads(xxx)
    print('3', dict2)
    return render_template('main/tttest.html', wow=dict2)

@admin.route('/index')
@login_required
def index():
    return render_template('admin/admin_index.html')

@admin.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_y = request.form.get('course_y')
        if Courses.query.filter(Courses.name == course_name).first() and Courses.query.filter(Courses.year == course_y).first():
            flash('该課程已存在！')
            return redirect('admin/add_course')
        course_m = request.form.get('course_m')
        course_w = request.form.get('course_w')
        course_d = request.form.get('course_d')
        course_t = request.form.get('course_t')
        course_region = request.form.get('course_region')
        course_times = request.form.get('course_times')
        course_duration = request.form.get('course_duration')
        course_class = request.form.get('course_class')
        course_cost = request.form.get('course_cost')
        course_teacher = request.form.get('course_teacher')
        course_limit = request.form.get('course_limit')
        course_summary = request.form.get('course_summary')
        x = Courses(name=course_name, year=course_y, start_m=course_m, start_d=course_d, start_w=course_w, start_t=course_t, limit=course_limit, cost=course_cost,
                     region=course_region, teacher=course_teacher, times=course_times, duration=course_duration, summary=course_summary, course_class=course_class)
        db.session.add(x)
        db.session.commit()
        flash('√ 課程資料添加成功！')
        return redirect('admin/add_course')
    else:
        re1 = CRegion.query.all()
        re2 = []
        for i in re1:
            re2.append(i.region)
        return render_template('admin/addnew/add_course.html', region_list=re2)

@admin.route('/add_course_region', methods=['GET', 'POST'])
@login_required
def add_course_region():
    if request.method == 'POST':
        region = request.form.get('region_name')
        if CRegion.query.filter(CRegion.region == region).first():
            flash('該地區已存在！')
            return redirect('admin/add_course_region')
        r = CRegion(region=region)
        db.session.add(r)
        db.session.commit()
        return redirect('admin/add_course')
    else:
        return render_template('admin/addnew/add_course_region.html')

@admin.route('/del_course_region', methods=['GET', 'POST'])
@login_required
def del_course_region():
    if request.method == 'POST':
        region = request.form.get('region_name')
        r = CRegion.query.filter(CRegion.region == region).first()
        db.session.delete(r)
        db.session.commit()
        return redirect('admin/add_course')
    else:
        re1 = CRegion.query.all()
        re2 = []
        for i in re1:
            re2.append(i.region)
        return render_template('admin/addnew/del_course_region.html', region_list=re2)

@admin.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_id = request.form.get('student_id')
        if Students.query.filter(Students.iden == student_id).first():
            flash('該身份證號已被使用！')
            return redirect('admin/add_student')
        student_tel = request.form.get('student_tel')
        student_phone = request.form.get('student_phone')
        birth_y = request.form.get('birth_y')
        birth_m = request.form.get('birth_m')
        birth_d = request.form.get('birth_d')
        student_address = request.form.get('student_address')
        student_emname = request.form.get('student_emname')
        student_emtel = request.form.get('student_emtel')
        student_emphone = request.form.get('student_emphone')
        x = Students(name=student_name, iden=student_id, telephone=student_tel, phone=student_phone, birth_y=birth_y, birth_m=birth_m,
                     birth_d=birth_d, address=student_address, em_name=student_emname, em_tel=student_emtel, em_phone=student_emphone)
        db.session.add(x)
        db.session.commit()
        flash('√ 學員資料添加成功！')
        return redirect('admin/add_student')
    else:
        return render_template('admin/addnew/add_student.html')

@admin.route('/search_student', methods=['GET'])
@login_required
def search_student():
    re1 = Students.query.all()
    l2 = [] #储存列表l1
    l4 = [] #储存每一个字典
    for i in re1:
        l1 = []  # 列表中的项目
        l1.append(i.name)
        l1.append(i.telephone)
        l1.append(i.phone)
        l1.append(i.em_name)
        l1.append(i.em_tel)
        l1.append(i.em_phone)
        l2.append(l1)
        d = dict()
        d['id'] = i.id
        xx = json.dumps(d)
        x = parse.quote(xx)
        l4.append(x)
    lens = len(l2)
    return render_template('admin/search/student/search_student.html', student_list=l2, student_dict=l4, lens=lens)

@admin.route('/search_student/U_Have_A_Preview_Message<xxx>', methods=['GET'])
@login_required
def student_Pre(xxx):
    try:
        ddd = creatsddd(xxx)
    except:
        return redirect('admin/search_student')
    re1 = SCtalble.query.filter(SCtalble.student_id == ddd['id']).all()
    try:
        l2 = []
        for each in re1:
            re2 = Courses.query.filter(Courses.id == each.course_id).first()
            if re2:
                sttr = str(re2.year) + '年' + str(re2.name)
                l2.append(sttr)
            else:
                pass
        return render_template('admin/search/student/student_Pre.html', student_dict=ddd, courselist=l2)
    except:
        return render_template('admin/search/student/student_Pre.html', student_dict=ddd)

@admin.route('/search_student/U_Have_A_Updata_Message<xxx>', methods=['GET', 'POST'])
@login_required
def student_Up(xxx):
    ddd = creatsddd(xxx)
    tt = type(ddd)
    if tt != dict:
        return redirect('admin/search_student')
    else:
        if request.method == 'POST':
            x1 = request.form.get('student_id')
            if Students.query.filter(Students.iden == x1).first():
                flash('該身份證號已被使用！')
                return redirect('admin/add_student')
            result = Students.query.filter(Students.id == ddd['id']).first()
            result.name = request.form.get('student_name')
            result.iden = x1
            result.telephone = request.form.get('student_tel')
            result.phone = request.form.get('student_phone')
            result.birth_y = request.form.get('birth_y')
            result.birth_m = request.form.get('birth_m')
            result.birth_d = request.form.get('birth_d')
            result.address = request.form.get('student_address')
            result.em_name = request.form.get('student_emname')
            result.em_tel = request.form.get('student_emtel')
            result.em_phone = request.form.get('student_emphone')
            db.session.commit()
            return redirect('admin/search_student')
        else:
            return render_template('admin/search/student/student_Up.html', student_dict=ddd)

@admin.route('/search_student/U_Have_A_Delete_Message<xxx>', methods=['GET'])
@login_required
def student_Del(xxx):
    ddd = json.loads(parse.unquote(xxx))
    tt = type(ddd)
    if tt != dict:
        return redirect('admin/search_student')
    else:
        result = Students.query.filter(Students.id == ddd['id']).first()
        db.session.delete(result)
        db.session.commit()
        return redirect('admin/search_student')

@admin.route('/search_student/Enroll<xxx>', methods=['GET', 'POST'])
@login_required
def Enroll(xxx):
    ddd = creatsddd(xxx)
    compare = SCtalble.query.filter(SCtalble.student_id == ddd['id']).all()
    lc = []
    for each in compare:
        lc.append(each.course_id)
    l2 = []  # 储存列表l1
    l4 = []  # 储存每一个字典
    if request.method == 'POST':
        req = request.form.getlist('target')
        for each in lc:
            if not each in req:
                result = SCtalble.query.filter(SCtalble.course_id == each, SCtalble.student_id == ddd['id']).first()
                db.session.delete(result)
        for each in req:
            if not each in lc:
                sc = SCtalble(student_id=ddd['id'], course_id=each)
                db.session.add(sc)
        db.session.commit()
        return redirect('admin/s_Enrollsuccess')
    else:
        ytime = time.strftime('%Y', time.localtime(time.time()))
        mtime = time.strftime('%m', time.localtime(time.time()))
        c_year = str(int(ytime)-1911)
        n_year = str(int(ytime)-1910)
        final_result = []
        if int(mtime) > 2:
            result1 = Courses.query.filter(Courses.year == c_year, Courses.start_m >= int(mtime)).all()
            result2 = Courses.query.filter(Courses.year == n_year, Courses.start_m < 3).all()
            final_result = result1 + result2
        elif int(mtime) < 3:
            final_result = Courses.query.filter(Courses.year == c_year, Courses.start_m >= int(mtime)).all()
        for i in final_result:
            l1 = []  # 列表中的项目
            l1.append(i.name)
            example1 = str(i.year) + '/' + str(i.start_m) + '/' + str(i.start_d) + ' 周' + str(i.start_w) + str(i.start_t)
            l1.append(example1)
            l1.append(i.teacher)
            l1.append(i.region)
            example2 = str(i.times) + '堂 每堂' + str(i.duration) + '小時'
            l1.append(example2)
            l1.append(i.cost)
            l1.append(i.limit)
            l1.append(i.summary)
            l2.append(l1)
            d = creatcdic(i)
            l4.append(d)
        lens = len(l2)
        return render_template('admin/search/student/student_Enroll.html', course_list=l2, course_dict=l4, lens=lens, ddd=ddd, lc=lc)

@admin.route('/s_Enrollsuccess', methods=['GET'])
@login_required
def enrollsuccess():
    return render_template('admin/search/student/s_Enrollsuccess.html')

@admin.route('/students_Download', methods=['GET'])
@login_required
def sdownload():
    if request.method == 'GET':
        out = BytesIO()
        s = Students.query.all()
        workbook = xlsxwriter.Workbook(out)
        table = workbook.add_worksheet()
        headers = ['姓名', '聯繫方式', '生日', '地址', '身份證號', '緊急聯絡人', '緊急聯絡人聯繫方式']
        for i in range(7):
            table.write(0, i, headers[i])
        lens = len(s)
        for x1 in range(lens):
            for x2 in range(7):
                x = creatsdic(s[x1])
                conn = x['telephone'] + ' ; ' + x['phone']
                if x['telephone']=='' or x['phone']=='':
                    conn = conn.replace(' ; ', '')
                birth = str(x['birth_y']) + '.' + str(x['birth_m']) + '.' + str(x['birth_d'])
                em_conn = x['em_tel'] + ' ; ' + x['em_phone']
                if x['em_tel']=='' or x['em_phone']=='':
                    em_conn = em_conn.replace(' ; ', '')
                xx = [x['name'], conn, birth, x['address'], x['iden'], x['em_name'], em_conn]
                table.write(x1+1, x2, xx[x2])
        workbook.close()
        out.seek(0)
        filename = parse.quote('學員名單.xlsx')
        rv = send_file(out, as_attachment=True, attachment_filename=filename)
        rv.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
        return rv

@admin.route('/search_course', methods=['GET', 'POST'])
@login_required
def search_course():
    re1 = CRegion.query.all()
    re2 = []
    re3 = Courses.query.all()
    for i in re1:
        re2.append(i.region)
    l2 = []  # 储存列表l1
    l4 = []  # 储存每一个字典
    l3 = []  # 储存每一个的学生人数
    if request.method == 'POST':
        require1 = request.form.get('year')
        require2 = request.form.get('month')
        require3 = request.form.get('class')
        require4 = request.form.get('region')
        result1 = re3
        result2 = re3
        result3 = re3
        result4 = re3
        if not require1 == '0':
            result1 = Courses.query.filter(Courses.year == require1).all()
        if not require2 == '0':
            result2 = Courses.query.filter(Courses.start_m == require2).all()
        if not require3 == '0':
            result3 = Courses.query.filter(Courses.course_class == require3).all()
        if not require4 == '0':
            result4 = Courses.query.filter(Courses.region == require4).all()
        x1 = set(re3)
        x2 = set(result1)
        x3 = set(result2)
        x4 = set(result3)
        x5 = set(result4)
        final_result = x1&x2&x3&x4&x5
        cdic = dict()
        final_list = []
        for e in final_result:
            final_list.append(e)
        lens = len(final_list)
        for each in range(lens):
            cdic[str(each)] = final_list[each].id
        cjson = parse.quote(json.dumps(cdic))
        for i in final_result:
            l1 = []  # 列表中的项目
            d = dict()
            l1.append(i.name)
            l1.append(i.course_class)
            example = str(i.year) + '/' + str(i.start_m) + '/' + str(i.start_d) + ' 周' + str(i.start_w) + str(i.start_t)
            l1.append(example)
            l1.append(i.teacher)
            l1.append(i.region)
            l1.append(i.limit)
            l2.append(l1)
            d['id'] = i.id
            number = len(SCtalble.query.filter(SCtalble.course_id == d['id']).all())
            l3.append(number)
            xx = json.dumps(d)
            x = parse.quote(xx)
            l4.append(x)
        l2.reverse()
        lens = len(l2)
        return render_template('admin/search/course/search_course.html', course_list=l2, course_dict=l4, lens=lens, region_list=re2,
                               require1=str(require1), require2=require2, require3=require3, require4=require4, cjson=cjson, number=l3)
    else:
        cdic = dict()
        lens = len(re3)
        for each in range(lens):
            cdic[str(each)] = re3[each].id
        cjson = parse.quote(json.dumps(cdic))
        for i in re3:
            l1 = []  # 列表中的项目
            l1.append(i.name)
            l1.append(i.course_class)
            example = str(i.year) + '/' + str(i.start_m) + '/' + str(i.start_d) + ' 周' + str(i.start_w) + " " + str(i.start_t)
            l1.append(example)
            l1.append(i.teacher)
            l1.append(i.region)
            l1.append(i.limit)
            l2.append(l1)
            d = dict()
            d['id'] = i.id
            number = len(SCtalble.query.filter(SCtalble.course_id == d['id']).all())
            l3.append(number)
            xx = json.dumps(d)
            x = parse.quote(xx)
            l4.append(x)
        lens = len(l2)
        return render_template('admin/search/course/search_course.html', course_list=l2, course_dict=l4, lens=lens, region_list=re2, cjson=cjson, number=l3)

@admin.route('/search_course/courses_download<xxx>', methods=['GET'])
@login_required
def cdownload(xxx):
    out = BytesIO()
    workbook = xlsxwriter.Workbook(out)
    table = workbook.add_worksheet()
    headers = ['課程', '課程概述', '上課地點', '授課講師', '開課時間', '上課時間', '上限']
    for i in range(7):
        table.write(0, i, headers[i])
    cdict = json.loads(parse.unquote(xxx))
    clist = []
    for key in cdict:
        item = Courses.query.filter(Courses.id == cdict[str(key)]).first()
        clist.append(item)
    lens = len(clist)
    for x1 in range(lens):
        for x2 in range(7):
            x = creatcdic(clist[x1])
            durtime = str(x['start_m']) + '/' + str(x['start_d']) + ' ; 每週' + x['start_w'] + ' ; 共' + str(x['times']) + '堂課'
            starttime = x['start_t'] + ' ; 每堂' + str(x['duration']) + '小時'
            xx = [x['name'], x['summary'], x['region'], x['teacher'], durtime, starttime, x['limit']]
            table.write(x1 + 1, x2, xx[x2])
    workbook.close()
    out.seek(0)
    filename = parse.quote('所選課程列表.xlsx')
    rv = send_file(out, as_attachment=True, attachment_filename=filename)
    rv.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
    return rv

@admin.route('/search_course/soc_download<xxx>', methods=['GET'])
@login_required
def socdownload(xxx):
    cid = json.loads(parse.unquote(xxx))['id']
    cc = Courses.query.filter(Courses.id == cid).first()
    cname = cc.name
    sids = SCtalble.query.filter(SCtalble.course_id == cid).all()
    sidlist = []
    for each in sids:
        sidlist.append(each.student_id)
    slist = []
    for each2 in sidlist:
        slist.append(Students.query.filter(Students.id == each2).first())
    out = BytesIO()
    workbook = xlsxwriter.Workbook(out)
    table = workbook.add_worksheet()
    headers = ['姓名', '聯繫方式', '生日', '地址', '身份證號', '緊急聯絡人', '緊急聯絡人聯繫方式']
    for i in range(7):
        table.write(0, i, headers[i])
    lens = len(slist)
    for x1 in range(lens):
        for x2 in range(7):
            x = creatsdic(slist[x1])
            conn = x['telephone'] + ' ; ' + x['phone']
            if x['telephone'] == '' or x['phone'] == '':
                conn = conn.replace(' ; ', '')
            birth = str(x['birth_y']) + '.' + str(x['birth_m']) + '.' + str(x['birth_d'])
            em_conn = x['em_tel'] + ' ; ' + x['em_phone']
            if x['em_tel'] == '' or x['em_phone'] == '':
                em_conn = em_conn.replace(' ; ', '')
            xx = [x['name'], conn, birth, x['address'], x['iden'], x['em_name'], em_conn]
            table.write(x1 + 1, x2, xx[x2])
    workbook.close()
    out.seek(0)
    filename = parse.quote(str(cname)+'學員名冊.xlsx')
    rv = send_file(out, as_attachment=True, attachment_filename=filename)
    rv.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
    return rv

@admin.route('/search_course_reset', methods=['GET'])
@login_required
def serch_reset():
    return redirect('admin/search_course')

@admin.route('/search_course/U_Have_A_Preview_Message<xxx>', methods=['GET'])
@login_required
def course_Pre(xxx):
    try:
        ddd = creatcddd(xxx)
    except:
        return redirect('admin/search_course')
    re1 = SCtalble.query.filter(SCtalble.course_id == ddd['id']).all()
    try:
        l2 = []
        for each in re1:
            re2 = Students.query.filter(Students.id == each.student_id).first()
            if re2:
                l2.append(re2.name)
            else:
                pass
        return render_template('admin/search/course/course_Pre.html', course_dict=ddd, studentlist=l2)
    except:
        return render_template('admin/search/course/course_Pre.html', course_dict=ddd)

@admin.route('/search_course/U_Have_A_Updata_Message<xxx>', methods=['GET', 'POST'])
@login_required
def course_Up(xxx):
    ddd = creatcddd(xxx)
    tt = type(ddd)
    if tt != dict:
        return redirect('admin/search_course')
    else:
        if request.method == 'POST':
            x1 = request.form.get('course_name')
            x2 = request.form.get('course_y')
            if Courses.query.filter(Courses.name == x1).first() and Courses.query.filter(
                            Courses.year == x2).first():
                flash('该課程已存在！')
                return redirect('admin/add_course')
            result = Courses.query.filter(Courses.id == ddd['id']).first()
            result.name = x1
            result.year = x2
            result.start_m = request.form.get('course_m')
            result.start_d = request.form.get('course_d')
            result.start_w = request.form.get('course_w')
            result.start_t = request.form.get('course_t')
            result.region = request.form.get('course_region')
            result.times = request.form.get('course_times')
            result.duration = request.form.get('course_duration')
            result.cost = request.form.get('course_cost')
            result.course_class = request.form.get('course_class')
            result.teacher = request.form.get('course_teacher')
            result.limit = request.form.get('course_limit')
            result.summary = request.form.get('course_summary')
            db.session.commit()
            return redirect('admin/search_course')
        else:
            re1 = CRegion.query.all()
            re2 = []
            for i in re1:
                re2.append(i.region)
            return render_template('admin/search/course/course_Up.html', course_dict=ddd, region_list=re2)

@admin.route('/search_course/U_Have_A_Delete_Message<xxx>', methods=['GET'])
@login_required
def course_Del(xxx):
    ddd = json.loads(parse.unquote(xxx))
    tt = type(ddd)
    if tt != dict:
        return redirect('admin/search_course')
    else:
        result = Courses.query.filter(Courses.id == ddd['id']).first()
        db.session.delete(result)
        db.session.commit()
        return redirect('admin/search_course')

@admin.route('/search_course/Enroll<xxx>', methods=['GET', 'POST'])
@login_required
def Enroll2(xxx):
    ddd = creatcddd(xxx)
    compare = SCtalble.query.filter(SCtalble.course_id == ddd['id']).all()
    lc = []
    for each in compare:
        lc.append(each.student_id)
    l2 = []  # 储存列表l1
    l4 = []  # 储存每一个字典
    if request.method == 'POST':
        return redirect('admin/c_Enrollsuccess' + str(ddd['id']))
    else:
        final_result = Students.query.all()
        for i in final_result:
            l1 = []  # 列表中的项目
            l1.append(i.name)
            l1.append(i.iden)
            example = str(i.birth_y) + '/' + str(i.birth_m) + '/' + str(i.birth_d)
            l1.append(example)
            l1.append(i.telephone)
            l1.append(i.phone)
            l2.append(l1)
            d = creatsdic(i)
            l4.append(d)
        lens = len(l2)
        return render_template('admin/search/course/course_Enroll.html', student_list=l2, student_dict=l4, lens=lens, ddd=ddd, lc=lc, c_id=ddd['id'])

@admin.route('/c_Enrollsuccess<c_id>', methods=['GET', 'POST'])
@login_required
def enrollsuccess2(c_id):
    compare = SCtalble.query.filter(SCtalble.course_id == c_id).all()
    lc = []
    for each in compare:
        lc.append(each.student_id)
    xdata = request.form.get('data')
    if type(xdata) == str:
        slist = json.loads(xdata)
        for each in lc:
            if not each in slist:
                result = SCtalble.query.filter(SCtalble.student_id == each, SCtalble.course_id == c_id).first()
                db.session.delete(result)
        for each in slist:
            if not each in lc:
                sc = SCtalble(course_id=c_id, student_id=each)
                db.session.add(sc)
        db.session.commit()
    else:
        pass
    return render_template('admin/search/course/c_Enrollsuccess.html')

#上传文档
@admin.route('/Upload', methods=['GET', 'POST'])
@login_required
def csupload():
    if request.method == 'POST':
        try:
            if 'xdoc1' in request.files:
                doc1 = request.files['xdoc1']
                filename = doc1.filename
                if filename != '':
                    if str(filename) == 'Students.xlsx':
                        xdocs.save(doc1)
                    else:
                        flash('Error:學生文檔錯誤！')
            if 'xdoc2' in request.files:
                doc2 = request.files['xdoc2']
                filename = doc2.filename
                if filename != '':
                    if str(filename) == 'Courses.xlsx':
                        xdocs.save(doc2)
                    else:
                        flash('Error:課程文檔錯誤！')
            return redirect('admin/Upload_sheets')
        except:
            flash('Error:程式錯誤！')
            return redirect('admin/Upload')
    return render_template('admin/Upload.html')

#加载文档
import xlrd
def supload(spath):
    workbook = xlrd.open_workbook(spath)
    sheetname = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(sheetname)
    rowsquan = sheet.nrows
    rlist = []
    for i in range(int(rowsquan)):
        rlist.append(sheet.row_values(i))
    for each in rlist[1:]:
        item = Students.query.filter(Students.name==each[0], Students.iden==each[1]).first()
        if item:
            pass
        else:
            if each[4]=='':
                each[4] = 10
            if each[5]=='':
                each[5] = 1
            if each[6]=='':
                each[6] = 1
            additem = Students(name=each[0], iden=each[1], telephone=each[2], phone=each[3], birth_y=each[4],  birth_m=each[5],
                     birth_d=each[6], address=each[7], em_name=each[8], em_tel=each[9], em_phone=each[10])
            db.session.add(additem)
    db.session.commit()

def cupload(cpath):
    workbook = xlrd.open_workbook(cpath)
    sheetname = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(sheetname)
    rowsquan = sheet.nrows
    rlist = []
    for i in range(int(rowsquan)):
        rlist.append(sheet.row_values(i))
    for each in rlist[1:]:
        region_list = []
        item = Courses.query.filter(Courses.name==each[0], Courses.year==each[1], Courses.start_m==each[2]).first()
        if item:
            pass
        else:
            if str(each[5])[0] == '0':
                xxx = each[5]*24
                ind = str(xxx).index('.')
                if str(xxx)[ind+1] == '5':
                    each[5] = str(xxx)[:ind] + ':30'
                else:
                    each[5] = str(round(xxx)) + ':00'
            additem = Courses(name=each[0], year=each[1], start_m=each[2], start_d=each[3], start_w=each[4], start_t=each[5], limit=each[6],
                     region=each[7], teacher=each[8], times=each[9], duration=each[10], summary=each[11], cost=each[12], course_class=each[13])
            db.session.add(additem)
            region_all = CRegion.query.all()
            for ex in region_all:
                region_list.append(ex.region)
            if each[7] not in region_list:
                region_x = CRegion(region=each[7])
                db.session.add(region_x)
    db.session.commit()

@admin.route('/Upload_sheets', methods=['GET'])
@login_required
def csload():
    cpath = config.DatabaseConfig.UPLOADED_XDOCS_DEST + '/Courses.xlsx'
    spath = config.DatabaseConfig.UPLOADED_XDOCS_DEST + '/Students.xlsx'
    try:
        if os.path.exists(cpath):
            cupload(cpath)
            os.remove(cpath)
            flash('課程文檔成功上傳！')
        if os.path.exists(spath):
            supload(spath)
            os.remove(spath)
            flash('學生文檔成功上傳！')
        return redirect('admin/Upload')
    except:
        if os.path.exists(cpath):
            os.remove(cpath)
        if os.path.exists(spath):
            os.remove(spath)
        return redirect('admin/Upload')

# 针对每一年获取数据
def dataofyear(x):
    courses_1 = Courses.query.filter(Courses.year == x, Courses.start_m > 2).all()
    courses_2 = Courses.query.filter(Courses.year == x+1, Courses.start_m < 3).all()
    courses_year_list = courses_1 + courses_2
    # 每年的开课数
    courses_year_number = len(courses_year_list)
    # 每年上课的人数
    students_year_number = 0
    for each in courses_year_list:
        sc_list = SCtalble.query.filter(SCtalble.course_id == each.id).all()
        each_cousers_students_number = len(sc_list)
        students_year_number += each_cousers_students_number
    # 每年的拓點
    region_number_list = []
    for each in courses_year_list:
        region_number_list.append(each.region)
    new_region_number_list = []
    for each in region_number_list:
        if each not in new_region_number_list:
            new_region_number_list.append(each)
    region_number = len(new_region_number_list)
    # 每种课上课的人数
    courses_class = ['樂齡核心課程', '自主規劃課程', '貢獻服務課程', '樂齡自主社團']
    courses_class_students_number = dict()
    for each in courses_class:
        xxx = []
        i = 0
        for each2 in courses_year_list:
            if each2.course_class == each:
                xxx.append(each2)
        for x1 in xxx:
            sc_list = SCtalble.query.filter(SCtalble.course_id == x1.id).all()
            i += len(sc_list)
        courses_class_students_number[each] = i
    # 地区的课程数
    region_list = CRegion.query.all()
    region_name_list = []
    region_courses_number = dict()
    region_courses_students_number = dict()
    for each in region_list:
        if each.region in new_region_number_list:
            region_name_list.append(each.region)
    for each in region_name_list:
        xxx = []
        i = 0
        ii = 0
        for each2 in courses_year_list:
            if each2.region == each:
                xxx.append(each2)
        i += len(xxx)
        region_courses_number[each + '開課數量'] = i
        # 地区课程的人数
        for x1 in xxx:
            sc_list = SCtalble.query.filter(SCtalble.course_id == x1.id).all()
            ii += len(sc_list)
        region_courses_students_number[each + '上課人數'] = ii
    allitem = dict()
    allitem['year'] = x
    allitem['year_courses'] = courses_year_number
    allitem['year_students'] = students_year_number
    allitem['region_number'] = region_number
    allitem['courses_class_students_number'] = courses_class_students_number
    allitem['region_courses_number'] = region_courses_number
    allitem['region_courses_students_number'] = region_courses_students_number
    return allitem

@admin.route('/Charts', methods=['GET', 'POST'])
@login_required
def charts():
    ytime = time.strftime('%Y', time.localtime(time.time()))
    c_year = int(ytime) - 1911
    alldata = dict()
    for i in range(105, c_year+1):
        ddd = dataofyear(i)
        alldata[i] = ddd
    lens = len(alldata)
    key_year = []
    for key in alldata:
        key_year.append(key)
    if request.method == 'POST':
        mod_require = request.form.get('mod_year')
        if mod_require == '0':
            return redirect('admin/Charts')
        else:
            region_list = []
            for each in alldata[int(mod_require)]['region_courses_number']:
                region_list.append(each[:-4])
            return render_template('admin/Charts2.html', alldata=alldata, mod_require=mod_require, region_list=region_list)
    return render_template('admin/Charts1.html', alldata=alldata, lens=lens, key_year=key_year)

from flask_login import logout_user
@admin.route('/Personal_Modify', methods=['GET', 'POST'])
@login_required
def selfmodify():
    if request.method == 'POST':
        user = Admin.query.filter(Admin.ad_name == session['log_in']).first()
        real_secret = user.ad_secret
        old_secret = request.form.get('old_secret')
        if old_secret != real_secret:
            flash('原密碼錯誤！請檢查後重新輸入')
            return redirect('admin/Personal_Modify')
        new_secret = request.form.get('new_secret')
        new_secret_repeat = request.form.get('new_secret_repeat')
        if new_secret == old_secret:
            flash('新密碼請勿與原密碼一致！請檢查後重新輸入')
            return redirect('admin/Personal_Modify')
        if new_secret != new_secret_repeat:
            flash('兩次新密碼輸入不一致！請檢查後重新輸入')
            return redirect('admin/Personal_Modify')
        else:
            user.ad_secret = new_secret
            db.session.commit()
            return redirect('admin/modify_successed')
    return render_template('admin/personalmodify.html')

@admin.route('/modify_successed', methods=['GET', 'POST'])
@login_required
def modifysuccessed():
    logout_user()
    return render_template('admin/modify_successed.html')