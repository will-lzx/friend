from django.db import models

# Create your models here.


class Customer(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    openid = models.CharField(max_length=200)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)


class Activity(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=200)
    time = models.DateTimeField()
    location = models.CharField(max_length=200)
    number = models.IntegerField()
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)


class Member(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11, default='')
    weixin_qq = models.CharField(max_length=100, default='')
    sex = models.IntegerField()
    birth = models.DateTimeField()
    open_id = models.CharField(max_length=200, default='', unique=True)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)


class Expert(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    member = models.ForeignKey(Member, on_delete=True, default=None)
    grade = models.IntegerField(default=0)
    description = models.TextField(default='')
    online = models.BooleanField(default=False)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)


class StudyMember(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    member = models.ForeignKey(Member, on_delete=True, default=None)
    # 0: not any member, 1: friend member, 2: study member
    member_type = models.IntegerField()
    description = models.TextField(default='')
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)


class Pic(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    index = models.IntegerField()
    binary = models.BinaryField()
    member_type = models.IntegerField(default=0)
    open_id = models.CharField(max_length=200, default='')
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)


class StudyContact(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    expert = models.ForeignKey(Expert, on_delete=True)
    member = models.ForeignKey(Member, on_delete=True)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)


class Issue(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    issue_type = models.IntegerField()
    description = models.TextField()
    owner = models.CharField(max_length=200)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)



