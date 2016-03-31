from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from result.models import studentResponse
from django.http import HttpResponse
from quiz.models import Questions
from django.db.models import Q
import json

# Create your views here.

@login_required(login_url='/login/')
def display_result(request,question_id):
    username = request.user.username
    result_data_from_database = studentResponse.objects.filter(Q(username=username)&Q(questionSetID=question_id))
    question_data = Questions.objects.filter(questionSetID = question_id)
    average_analysis_data= 0
    if average_analysis_data:
        average_analysis_data = average_analysis_data[0]
    else:
        average_analysis_data = 0
    if question_data.exists():
        question_data = question_data[0]
        questions = json.loads(question_data.questionsJson)
        if result_data_from_database:
            result_data_from_database = result_data_from_database[0]
            context_data = {
                'first_name':request.user.first_name,
                'totalQuestions':result_data_from_database.totalAttempted+result_data_from_database.totalUnAttempted,
                'attempted':result_data_from_database.totalAttempted,
                'correct':result_data_from_database.totalCorrectAnswer,
                'wrong':result_data_from_database.totalWrongAnswer,
                'marks':result_data_from_database.marksObtained,
                'averageAnalysis':average_analysis_data,
                'questionData':questions
            }
            return render(request,'result.html',context_data)
        else:
            return HttpResponse('Invalid Question Set ID')
    else:
        return HttpResponse("You have not attempted this test")