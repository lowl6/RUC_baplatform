from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class User(models.Model):
    '''用户表'''
    username = models.CharField(verbose_name='用户', max_length=16, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    type_choices = (
        (1, "学生"),
        (2, "老师"),
        (3, "管理员"),
    )
    type = models.SmallIntegerField(verbose_name='用户类型', choices=type_choices)

class StudentInfo(models.Model):
    '''学生信息表'''
    user = models.OneToOneField(User, verbose_name='学生', on_delete=models.CASCADE, primary_key=True, related_name='Student')
    name = models.CharField(verbose_name='名字', max_length=64, default="未知")
    gender_choices = (
        (1, "男"),
        (2, "女"),  
        (3, "保密")
    )
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices, default=3, blank=True)
    email = models.EmailField(verbose_name='邮箱', max_length=64, blank=True)
    phone = models.CharField(verbose_name='手机号', max_length=16, blank=True)
    student_profile_pic = models.ImageField(verbose_name='头像', upload_to="userimg/student_profile_pic", blank=True)

    def __str__(self):
        return self.name

class TeacherInfo(models.Model):
    '''老师信息表'''
    user = models.OneToOneField(User, verbose_name='老师', on_delete=models.CASCADE, primary_key=True, related_name='Teacher')
    name = models.CharField(verbose_name='名字', max_length=64, default="未知")
    gender_choices = (
        (1, "男"),
        (2, "女"),  
        (3, "保密")
    )
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices, default=3, blank=True)
    email = models.EmailField(verbose_name='邮箱', max_length=64, blank=True)
    phone = models.CharField(verbose_name='手机号', max_length=16, blank=True)
    description = models.TextField(verbose_name='教师简介', max_length=1000, blank=True)
    teacher_profile_pic = models.ImageField(verbose_name='头像', upload_to="userimg/teacher_profile_pic", blank=True)
    description_richtext = RichTextField(verbose_name='教师简介', blank=True)
    order = models.IntegerField(verbose_name='顺序',default=0 ,blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']

class Course(models.Model):
    '''课程表'''
    name = models.CharField(verbose_name='课程名', max_length=64)
    teacher = models.ForeignKey(TeacherInfo, verbose_name='教课老师', on_delete=models.CASCADE, related_name='course_teacher')
    course_profile_pic = models.ImageField(verbose_name='课程图', upload_to="userimg/course_profile_pic/", blank=True)
    description = models.TextField(verbose_name='课程简介', max_length=1000, blank=True)
    description_richtext = RichTextField(verbose_name='课程简介', blank=True)
    order = models.IntegerField(verbose_name="课程顺序", default=0, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class CourseFiles(models.Model):
    '''课件表'''
    course = models.ForeignKey(Course, verbose_name='所属课程', on_delete=models.CASCADE, related_name='file_course')
    file = models.FileField(verbose_name='课件', upload_to="files/")
    file_name = models.CharField(verbose_name='课件名', max_length=64, default=file.name, blank=True)

    def __str__(self):
        return self.file_name

class Assignment(models.Model):
    '''任务表'''
    name = models.CharField(verbose_name='任务名', max_length=64)
    course = models.ForeignKey(Course, verbose_name='所属课程', on_delete=models.CASCADE, related_name='assignment_course')
    description = models.TextField(verbose_name='任务简介', max_length=1000, blank=True)
    description_richtext = RichTextField(verbose_name='任务简介', blank=True)
    is_group = models.BooleanField(verbose_name='是否是小组任务', default=False)
    ddl = models.DateField(verbose_name='任务截止时间')

    def __str__(self):
        return self.name

class AssignmentFile(models.Model):
    '''任务文档'''
    file = models.FileField(verbose_name='任务文档', upload_to="assignments/")
    file_name = models.CharField(verbose_name='文档名', max_length=64 ,default=file.name, blank=True)
    assignment = models.ForeignKey(Assignment, verbose_name='所属任务', on_delete=models.CASCADE, related_name='file_assignment')

    def __str__(self):
        return self.file_name

class AssignmentComment(models.Model):
    '''任务评价'''
    comment =  models.TextField(verbose_name='任务评价')
    assignment = models.ForeignKey(Assignment, verbose_name='所属任务', on_delete=models.CASCADE, related_name="comment_assignment")
    user = models.ForeignKey(User, verbose_name='评价人', on_delete=models.CASCADE, related_name='comment_user')
    created_at = models.DateField(verbose_name='评价时间', auto_now=True)

    class Meta:
        ordering = ['-created_at']

class CourseComment(models.Model):
    '''课程讨论'''
    comment = models.TextField(verbose_name="评论")
    course = models.ForeignKey(Course, verbose_name="所属课程", on_delete=models.CASCADE, related_name="comment_course")
    user = models.ForeignKey(User, verbose_name='评价人', on_delete=models.CASCADE, related_name='coursecomment_user')
    created_at = models.DateField(verbose_name='评价时间', auto_now=True)

    class Meta:
        ordering = ['-created_at']

class StudentCourse(models.Model):
    '''学生课程表'''
    student = models.ForeignKey(StudentInfo, verbose_name='选课学生', on_delete=models.CASCADE, related_name='course_student')
    course = models.ForeignKey(Course, verbose_name='被选课程', on_delete=models.CASCADE, related_name='student_course')
    
class AssignmentSubmit(models.Model):
    '''学生提交任务'''
    student = models.ForeignKey(StudentInfo, verbose_name='学生', on_delete=models.CASCADE, related_name='assignmentsubmit_student')
    assignment = models.ForeignKey(Assignment, verbose_name='所提交的任务', on_delete=models.CASCADE, related_name='submit_assignment')
    file = models.FileField(verbose_name='任务文档', upload_to="submission/")
    file_name = models.CharField(verbose_name='文档名', max_length=64 ,default=file.name, blank=True)
    marks = models.SmallIntegerField(verbose_name='获得分数', default=0)
    max_marks = models.SmallIntegerField(verbose_name='最大分数', default=100)
    submit_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

class Group(models.Model):
    '''小组表'''
    course = models.ForeignKey(Course, verbose_name='所属课程', on_delete=models.CASCADE, related_name='group_course')
    name = models.CharField(verbose_name="组名", max_length=64, unique=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    '''小组成员'''
    group = models.ForeignKey(Group, verbose_name='所属小组', on_delete=models.CASCADE, related_name='groupmember_group')
    student = models.ForeignKey(StudentInfo, verbose_name="小组成员", on_delete=models.CASCADE, related_name='groupmember_student')
    is_head = models.BooleanField()

    def __str__(self):
        return self.student.name
    submit_time = models.DateTimeField(auto_now=True)

class Announce(models.Model):
    '''老师通知'''
    announcement = models.TextField(verbose_name="通知")
    teacher = models.ForeignKey(TeacherInfo, verbose_name="所属老师", on_delete=models.CASCADE, related_name='announce_teacher')
    course = models.ForeignKey(Course, verbose_name='所属课程', on_delete=models.CASCADE, related_name="announce_course")

    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']

class TeacherDisabled(models.Model):
    '''禁用教师'''
    teacher = models.ForeignKey(User, verbose_name="禁用教师", on_delete=models.CASCADE, related_name="teacher_disabled")
