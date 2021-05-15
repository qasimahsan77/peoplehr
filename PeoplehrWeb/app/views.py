"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import requests,time

class Employee():
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)
    def basicdata(self):
        print('yes')
    pass

def GetEmployeeId():
    EmployeeId = []
    EmployeeName=[]
    EmployeeSalary=[]
    url = "https://api.peoplehr.net/Employee"
    payload = '{"APIKey": "e794266cd54842e79cd0f1b07a3988fe","Action":"GetAllEmployeeDetail","IncludeLeavers":"false"}'
    headers = {'Method': 'POST', 'ContentType': 'text/json'}
    response = requests.request("POST", url, data=payload)
    for k in response.json().get('Result'):
        try:
            EmployeeId.append(k.get('EmployeeId').get('DisplayValue'))
            EmployeeSalary.append(GetEmployeeSalary(k.get('EmployeeId').get('DisplayValue')))
        except:
            pass
        try:
            EmployeeName.append(k.get('FirstName').get('DisplayValue') + " " + \
                                k.get('LastName').get('DisplayValue'))
        except:
            pass
    pass
    return EmployeeId, EmployeeName,EmployeeSalary
    pass

def GetEmployeeSalary(id):
    try:
        url = "https://api.peoplehr.net/Salary"
        payload = '{"APIKey":"e794266cd54842e79cd0f1b07a3988fe","Action":"GetSalaryDetail","EmployeeId":"'+str(id)+'","IsIncludeHistory":"false"}'
        headers = {'Method': 'POST', 'ContentType': 'text/json'}
        response = requests.request("POST", url, data=payload)
        return response.json().get('Result')[0].get('SalaryAmount')
    except:
        return 0
    pass
    pass

def home(request):
    HolidayData = []
    Message = ""
    if request.method == "POST":
        StartDate = request.POST["From"]
        EndDate = request.POST["To"]
        HolidayStartDate = []
        HolidayEndDate = []
        DurationInDays = []
        DurationInMinutes = []
        CurrentEmployeeId=[]
        CurrentEmployeeName=[]
        CurrentEmployeeSalary=[]
        SalaryRemain=[]
        LeaveHours=[]
        TotalMinutes=[]
        TotalDays=[]
        EmployeeId,EmployeeName,EmployeeSalary =GetEmployeeId()
        if len(EmployeeId)>0:
            id=0
            while id<len(EmployeeId):
                url = "https://api.peoplehr.net/Holiday"
                payload = '{"APIKey": "e794266cd54842e79cd0f1b07a3988fe","Action":"GetHolidayDetail","EmployeeId":"'+str(EmployeeId[id])+'","StartDate":"'+str(StartDate) + '","EndDate":"' + str(EndDate) + '"}'
                print(payload)
                headers = {'Method': 'POST', 'ContentType': 'text/json'}
                response = requests.request("POST", url, data=payload)
                Salary=float(EmployeeSalary[id])
                try:
                    if len(response.json().get('Result')) ==0:
                        DurationInMinutes.append('--')
                        HolidayStartDate.append('--')
                        HolidayEndDate.append('--')
                        DurationInDays.append('--')
                        SalaryRemain.append('--')
                        LeaveHours.append('--')
                        CurrentEmployeeId.append(EmployeeId[id])
                        CurrentEmployeeName.append(EmployeeName[id])
                        CurrentEmployeeSalary.append(EmployeeSalary[id])
                    else:
                        for data in response.json().get('Result'):
                            for k,v in data.items():
                                if k == 'StartDate':
                                    HolidayStartDate.append(v)
                                if k == 'EndDate':
                                    HolidayEndDate.append(v)
                                if k == 'DurationInDays':
                                    DurationInDays.append(int(v))
                                    One="%.2f" % round((float(v)*(float(EmployeeSalary[id])/22)), 2)
                                    Salary-=float(One)
                                    SalaryRemain.append("£"+"%.2f" % round(Salary, 2))
                                    LeaveHours.append(str(float(v)*7.5)+"=> £"+str(One))
                                if k == 'DurationInMinutes':
                                    DurationInMinutes.append(int(v))
                                pass
                            pass                          
                            CurrentEmployeeId.append(EmployeeId[id])
                            CurrentEmployeeName.append(EmployeeName[id])
                            CurrentEmployeeSalary.append(EmployeeSalary[id])
                        pass
                        TotalMinutes.append(sum(DurationInDays))
                        TotalDays.append(sum(DurationInMinutes))
                    pass
                except Exception as E:
                    print(E)
                pass
                id+=1
            pass
            return render(request,'app/index.html',
                      {
                          'title':'Home Page',
                          'HolidayPack':list(zip(CurrentEmployeeId,CurrentEmployeeName,HolidayStartDate,HolidayEndDate,DurationInDays,DurationInMinutes,CurrentEmployeeSalary,LeaveHours,SalaryRemain)),
                          'TotalMinutes':TotalMinutes,
                          'TotalDays':TotalDays,
                      })
        pass
    else:
        EmployeeId = []
        EmployeeName = []
        EmployeeEmail = []
        EmployeeStartDate = []
        EmploymentType = []
        url = "https://api.peoplehr.net/Employee"
        payload = '{"APIKey": "e794266cd54842e79cd0f1b07a3988fe","Action":"GetAllEmployeeDetail","IncludeLeavers":"false"}'
        headers = {'Method': 'POST', 'ContentType': 'text/json'}
        response = requests.request("POST", url, data=payload)
        for k in response.json().get('Result'):
            try:
                EmployeeId.append(k.get('EmployeeId').get('DisplayValue'))
            except:
                pass
            try:
                EmployeeName.append(k.get('FirstName').get('DisplayValue') + " " + \
                                k.get('LastName').get('DisplayValue'))
            except:
                pass
            try:
                EmployeeEmail.append(k.get('EmailId').get('DisplayValue'))
            except:
                pass
            try:
                EmployeeStartDate.append(k.get('StartDate').get('DisplayValue'))
            except:
                pass
            try:
                EmploymentType.append(k.get('EmploymentType').get('DisplayValue'))
            except:
                pass
        pass
        return render(request,'app/index.html',
                      {
                          'title':'Home Page',
                          'Result':list(zip(EmployeeId,EmployeeName,EmployeeEmail,EmployeeStartDate,EmploymentType)),
                          'Holiday':HolidayData,
                      })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
