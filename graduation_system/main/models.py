from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.


class Payment(models.Model):
    bank = models.CharField(max_length=100, blank=False, default='Mellat')
    card_number = models.IntegerField()
    amount = models.IntegerField(blank=False)
    payer = models.CharField(max_length=100, blank=True)
    datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "payment-id:{}-amount:{}".format(self.id, self.amount)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starting_year = models.IntegerField()

    def select_process(self, process):
        process_instance = ProcessInstance(student=self, process=process)
        process_instance.save()
        for task in process.task_set.all():
            TaskInstance.objects.create(process_instance=process_instance, task=task)
        process_instance.current_task = TaskInstance.objects.get(task=process.task_start,
                                                                 process_instance=process_instance)
        process_instance.save()

    def __str__(self):
        return self.user.get_username()


class Process(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    task_start = models.ForeignKey('Task', blank=True, null=True, related_name='+')

    # task_end = models.ForeignKey('Task', blank=True, null=True, related_name='+')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    process = models.ForeignKey(Process, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    group = models.ForeignKey(Group, blank=True, null=True)
    debt = models.IntegerField(default=0)

    end_task = models.BooleanField(default=False)

    next_task_accept = models.ForeignKey('self', blank=True, null=True, related_name='+')
    next_task_reject = models.ForeignKey('self', blank=True, null=True, related_name='+')

    def __str__(self):
        return self.name


class ProcessInstance(models.Model):
    # make blank = false
    student = models.ForeignKey(Student, blank=True, null=True)
    process = models.ForeignKey(Process, blank=False)
    current_task = models.ForeignKey('TaskInstance', blank=True, null=True, related_name='+')

    class Meta:
        unique_together = ("student", "process")

    def process_complete(self):
        return self.current_task.task.end_task and self.current_task.status == 'accept'

    def accept(self):
        self.current_task.status = 'accept'
        self.current_task.save()
        if not self.current_task.task.end_task:
            self.current_task = self.current_task.next_accept()
            self.save()

    def reject(self):
        self.current_task.status = 'reject'
        self.current_task.save()
        if not self.current_task.task.end_task:
            self.current_task = self.current_task.next_reject()
            self.save()

    def __str__(self):
        return self.process.name + "-instance-" + str(self.id)


class TaskInstance(models.Model):
    TASK_STATUS = (
        ('student_pending', 'Student Pending'),
        ('staff_pending', 'Staff Pending'),
        ('reject', 'Reject'),
        ('accept', 'Accept'),
    )

    process_instance = models.ForeignKey(ProcessInstance, blank=False)
    task = models.ForeignKey(Task, blank=False)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='student_pending')

    payment = models.ForeignKey(Payment, blank=True, null=True)

    class Meta:
        unique_together = ("process_instance", "task")

    def next_accept(self):
        next_task = self.task.next_task_accept
        return TaskInstance.objects.get(task=next_task, process_instance=self.process_instance)

    def next_reject(self):
        next_task = self.task.next_task_reject
        return TaskInstance.objects.get(task=next_task, process_instance=self.process_instance)

    def __str__(self):
        return self.task.name + "-instance-" + str(self.id)


class Comment(models.Model):
    user = models.ForeignKey(User, blank=False)
    text = models.TextField()
    task_instance = models.ForeignKey(TaskInstance, blank=False)
    time = models.DateTimeField('date commented', auto_now_add=True)

    def __str__(self):
        return self.text


