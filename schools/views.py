from django.shortcuts import render, redirect
from .models import Teacher
from .forms import TeacherForm
from .models import School, Student, Subject, Result
from django.db.models import Avg
import openpyxl

def admin_dashboard(request):
    schools = School.objects.all()
    return render(request, "schools/dashboard_admin.html", {"schools": schools})

def school_dashboard(request, school_id):
    school = School.objects.get(id=school_id)
    students = Student.objects.filter(school=school)
    return render(request, "schools/dashboard_school.html", {"school": school, "students": students})

def home(request): 
    return render(request, "schools/home.html") 



def students_list(request): 
    students = Student.objects.all()
    return render(request, "schools/students_list.html", {"students": students})

def students_list(request):
    results = Result.objects.select_related("student", "subject", "student__school")
    return render(request, "schools/students_list.html", {"results": results})

def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teachers_list")
    else:
        form = TeacherForm()
    return render(request, "schools/add_teacher.html", {"form": form})


def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("teachers_list")
    else:
        form = TeacherForm(instance=teacher)
    return render(request, "schools/edit_teacher.html", {"form": form, "teacher": teacher})

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        teacher.delete()
        return redirect("teachers_list")
    return render(request, "schools/delete_teacher.html", {"teacher": teacher})

def teachers_list(request): 
    teachers = Teacher.objects.select_related("school", "subject") 
    return render(request, "schools/teachers_list.html", {"teachers": teachers})

def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    average_score = Result.objects.aggregate(Avg("score"))["score__avg"]

    return render(request, "schools/dashboard.html", {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "average_score": round(average_score, 2) if average_score else 0,
    })


def import_students(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        # Excel format: School | Student | Parent Phone | Subject | Score
        for row in sheet.iter_rows(min_row=2, values_only=True):
            school_name, student_name, parent_phone, subject_name, score = row

            school, _ = School.objects.get_or_create(name=school_name)
            student, _ = Student.objects.get_or_create(
                name=student_name,
                school=school,
                parent_phone=parent_phone
            )
            subject, _ = Subject.objects.get_or_create(name=subject_name, school=school)

            Result.objects.create(student=student, subject=subject, score=score)

        return redirect("students_list")

    return render(request, "schools/import_students.html")
