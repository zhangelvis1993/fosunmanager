from dataweb import db
from flask_login import UserMixin

class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), index=True)
    iden = db.Column(db.String(10), index=True, nullable=True)
    telephone = db.Column(db.String(15), index=True, nullable=True)
    phone = db.Column(db.String(15), index=True, nullable=True)
    birth_y = db.Column(db.Integer, nullable=True)
    birth_m = db.Column(db.Integer, nullable=True)
    birth_d = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(50), nullable=True)
    em_name = db.Column(db.String(5), nullable=True)
    em_tel = db.Column(db.String(15), index=True, nullable=True)
    em_phone = db.Column(db.String(15), index=True, nullable=True)
    what_courses = db.relationship('SCtalble', backref='what_students')

class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    year = db.Column(db.Integer, index=True)
    region = db.Column(db.String(15), index=True)
    course_class = db.Column(db.String(10), index=True)
    teacher = db.Column(db.String(5))
    start_m = db.Column(db.Integer)
    start_d = db.Column(db.Integer)
    start_w = db.Column(db.String(5))
    start_t = db.Column(db.String(7))
    times = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    cost = db.Column(db.String(5))
    summary = db.Column(db.String(200))
    limit = db.Column(db.Integer)
    what_students = db.relationship('SCtalble', backref='what_courses')

class CRegion(db.Model):
    __tablename__ = 'cregion'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(15), unique=True, index=True)

class SCtalble(db.Model):
    __tablename__ = 'sctalble'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), index=True)

class Admin(db.Model, UserMixin):
    __tablename__ = 'adminlist'
    id = db.Column(db.Integer, primary_key=True)
    #为了区分大小写，下面两项的字符集要改为utf8_bin
    ad_name = db.Column(db.String(20), unique=True, nullable=False, index=True)
    ad_secret = db.Column(db.String(20), nullable=False, index=True)