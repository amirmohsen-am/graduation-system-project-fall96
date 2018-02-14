# Amirmohsen Ahanchi
from django.contrib.auth.models import User
from django.forms import ModelForm

from main.models import Process, Task, Payment


class ProcessForm(ModelForm):
    class Meta:
        model = Process
        fields = ['name', 'task_start']
        # widgets = {
        #     'task_start': forms.ModelChoiceField(queryset=Task.objects.filter(process=))
        # }

    def __init__(self, *args, **kwargs):
        super(ProcessForm, self).__init__(*args, **kwargs)
        self.fields['task_start'].queryset = Task.objects.filter(process=self.instance)


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        if 'process_custom' in kwargs:
            process = kwargs.pop('process_custom')
        super(TaskForm, self).__init__(*args, **kwargs)
        if hasattr(self.instance, 'process'):
            process = self.instance.process

        self.fields['next_task_accept'].queryset = Task.objects.filter(process=process)
        self.fields['next_task_reject'].queryset = Task.objects.filter(process=process)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'last_login']


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['bank', 'card_number', 'amount', 'payer']