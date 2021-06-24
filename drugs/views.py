from django.shortcuts import render, redirect
from workstation.models.hospital import DrugsIssuing, Exam, Drug,DrugForm, ExamForm
from django.views.generic import CreateView, ListView, UpdateView, DetailView
import sweetify
# Create your views here.

success = 'Success!'
error = 'Error!'
error_message = 'Something Wrong Happened, please Try Again'
class DrugCreateView(CreateView):
    model = DrugsIssuing
    class_form = DrugForm
    fields = '__all__'
    success_url = "list"
    template_name = "drugs/register_drug.html"

class DrugDetailView(DetailView):
    model = DrugsIssuing
    template_name = "drugs/view_drug.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DrugListView(ListView):
    model = DrugsIssuing
    context_object_name = 'drugs'
    template_name = "drugs/drugsissuing_list.html"
    
class DrugUpdateView(UpdateView): 
    model = DrugsIssuing
    fields = '__all__'
    success_url = "view"
    template_name = 'drugs/update_drug.html'
    
def drug_list(request):
    drugs = Drug.objects.all()
    context = {'drugs': drugs}
    return render(request, 'drugs/drug_list.html', context)

def drug_create(request):
    title = 'Add'
    userr = request.user
    form = DrugForm()
    if(request.method == "POST"):
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, success, text='You have successfully added drug', icon='success', timerProgressBar='true', timer=3000)
            return redirect('list_drug')
    context = {'form':form, 'title':title}
    return render(request,'drugs/drugForm.html',context)

def drugDetail(request, pk):
    drug = Drug.objects.get(id=pk)
    
    context = {'drug':drug}
    return render(request, 'drugs/view_drug.html', context)

def update_drug(request, pk):
    user = request.user
    drug = Drug.objects.get(id=pk)
    form = DrugForm(instance=drug)
    title = 'Update'
    # form.fields['sector'].queryset = School.objects.filter(sector=sector.id)
    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid:
            form.save()
            sweetify.success(request, success, text='You have successfully updated Drug', icon='success', timerProgressBar='true', timer=3000) 
            return redirect('list_drug')
    context = {'form':form, 'title':title}
    return render(request, 'drugs/drugUpdateForm.html',context)

def delete_drug(request, id):
    drug = Drug.objects.get(pk=id)
    drug.delete()
    sweetify.success(request, success, text='You have successfully deleted drug', icon='success', timerProgressBar='true', timer=3000)
    return redirect('list_drug')

def examDetail(request, pk):
    exam = Exam.objects.get(id=pk)
    
    context = {'exam':exam}
    return render(request, 'drugs/view_exam.html', context)

def exam_create(request):
    title = 'Add'
    user = request.user
    form = ExamForm()
    if(request.method == "POST"):
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, success, text='You have successfully added exam', icon='success', timerProgressBar='true', timer=3000)
            return redirect('exam_list')
    context = {'form':form, 'title':title}
    return render(request,'drugs/examForm.html',context)

def update_exam(request, pk):
    user = request.user
    exam = Exam.objects.get(id=pk)
    form = ExamForm(instance=exam)
    title = 'Update'
    # form.fields['sector'].queryset = School.objects.filter(sector=sector.id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid:
            form.save()
            sweetify.success(request, success, text='You have successfully updated Exam', icon='success', timerProgressBar='true', timer=3000) 
            return redirect('exam_list')
    context = {'form':form, 'title':title}
    return render(request, 'drugs/examUpdateForm.html',context)

def exam_list(request):
    exams = Exam.objects.all()
    context = {'exams': exams}
    return render(request, 'drugs/exams_list.html', context)

def delete_exam(request, id):
    exam = Exam.objects.get(id=id)
    exam.delete()
    sweetify.success(request, success, text='You have successfully deleted exam', icon='success', timerProgressBar='true', timer=3000)
    return redirect('exam_list')