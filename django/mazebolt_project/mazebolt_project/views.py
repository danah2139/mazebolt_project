import os
import socket
from . import server_default
from django.utils import timezone
from django.db import IntegrityError
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Instance, Test
from .google_cloud import create_instance, delete_instance, list_instances
V1_BASE_URL = 'https://www.googleapis.com/compute/v1/projects/mbexam-4'
base_image_name = V1_BASE_URL + '/global/images/mb-exam-base'

NEW_TEST_INSTANCES=[]

def instance(request):
    if request.method == 'GET':
        all_instances = Instance.objects.all()
        context = {'all_instances': all_instances}
        return render(request, 'instances.html', context)
    if request.method == 'POST':
        try:
            instance_count = int(request.POST.get('instance_count'))
        except ValueError:
            all_instances = Instance.objects.all()
            context = {'all_instances': all_instances,
                       'error_message_count': "Please select intacne count"}
            return render(request, 'instances.html', context)
        print(instance_count)
        # This will create an instance:
        import uuid
        for i in range(instance_count):
            instance_name = 'mbexam-' + str(uuid.uuid4())
            print("Creating", instance_name)
            res = create_instance(instance_name=instance_name, image_name=base_image_name, size='n1-highcpu-2')
            print("Operation Result Create:", res)
            new_instance = Instance(name=instance_name, status=res['status'], created_at=res['startTime'])
            new_instance.save()

        return redirect('instance')


def list_networkIP(res,test_instances):
    host_list = []
    print('check',test_instances)
    for inst in res:
        for filter_inst in test_instances:
            if inst["name"] ==  getattr(filter_inst, 'name'):
                host_list.append(inst["networkInterfaces"][0]["networkIP"])
    return host_list


def test(request):
    print(request.method)
    if request.method == 'GET':
        all_tests = Test.objects.all()
        context = {'all_tests': all_tests}
        return render(request, 'tests.html', context)
    if request.method == 'POST':
        
        test_name = request.POST.get('test_name')
        command = request.POST.get('command')
        if not command:
            context = {'filter_instance': NEW_TEST_INSTANCES,
                       'error_message': 'please set type test'}
            return render(request, 'create_test.html', context)
        res = list_instances()
        host_list = list_networkIP(res,NEW_TEST_INSTANCES)
        #add_test(host_list,command,test_name)
        print(host_list,'host_list')
        try:
            new_test = Test(name = test_name , status = 'RUNNING',start_test_at=timezone.now(),command=command)
            new_test.save()
            new_test.instances.set(NEW_TEST_INSTANCES)
        except IntegrityError:
            context = {'filter_instance': NEW_TEST_INSTANCES,
                       'error_message': 'please insert valid test name'}
            return render(request, 'create_test.html', context)
        all_tests = Test.objects.all()
        context = {'all_tests': all_tests}         
        return render(request, 'tests.html', context)
        
def stop_test_checked(request):
    if request.method == 'POST':
        print(request.POST.keys())
        selected_keys = [k for k in request.POST.keys() if request.POST[k] == 'on']
        if not selected_keys:
            return redirect(test)
        filter_test_list = Test.objects.filter(name__in=selected_keys)
        print(selected_keys,'selected_keys')
        res = list_instances()
        print(filter_test_list,'filter_test_list')
        for filter_test in filter_test_list:
            #host_list = list_networkIP(res,filter_test.instances)
            #stop_test(host_list,filter_test.name)
            filter_test.status="STOP"
            filter_test.save()
        return redirect('test')
    
        
    


def terminate_instance(request):
    if request.method == 'POST':
        print(request.POST.keys())
        selected_keys = [k for k in request.POST.keys() if request.POST[k] == 'on']
        if not selected_keys:
            all_instances = Instance.objects.all()
            context = {'all_instances': all_instances,
                       'error_message_select': "Please select instacnes to test "}
            return render(request, 'instances.html', context)
        print(selected_keys)

        filter_instance = Instance.objects.filter(name__in=selected_keys)
        for instance in filter_instance:
            instance.delete()
            res = delete_instance(instance.name)
            print("Operation Result Delete:", res)
        return redirect('instance')


def add_test(host_list, command_type, test):
    for host in host_list:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(host,'host')
            s.connect((host, server_default.PORT))
            s.send(server_default.Message.ADD)
            if s.recv(1024) == server_default.Message.TEST_NAME:
                s.send(test)
                if s.recv(1024) == server_default.Message.TEST_TYPE:
                    s.send(command_type)
                
def stop_test(host_list,test):
     for host in host_list:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, server_default.PORT))
            s.send(server_default.Message.STOP)
            if s.recv(1024) == server_default.Message.TEST_NAME:
                s.send(test)





def create_test(request):
    if request.method == 'POST':
        print(request.POST.keys())
        selected_keys = [k for k in request.POST.keys() if request.POST[k] == 'on']
        print(selected_keys,'selected_keys')
        if not selected_keys:
            all_instances = Instance.objects.all()
            context = {'all_instances': all_instances,
                       'error_message_select': "Please select instacnes to test "}
            return redirect(instance)
        filter_instance = Instance.objects.filter(name__in=selected_keys)
        global NEW_TEST_INSTANCES
        NEW_TEST_INSTANCES = filter_instance
        return render(request, 'create_test.html', {'filter_instance': filter_instance})
