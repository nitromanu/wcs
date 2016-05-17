from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from result.models import studentResponse, feedback
from django.http import HttpResponse, Http404
from quiz.models import Questions, Feedback
from django.db.models import Q
import json
from reportlab.pdfgen import canvas


# Create your views here.

@login_required(login_url='/login/')
def display_result(request, question_id):
    username = request.user.username
    result_data_from_database = studentResponse.objects.filter(Q(username=username) & Q(questionSetID=question_id))
    question_data = Questions.objects.filter(questionSetID=question_id)
    feedback_data = Feedback.objects.filter(Q(username=username) & Q(questionSetID=question_id))
    feedback_needed = True;
    if feedback_data.exists():
        feedback_needed = False

    average_analysis_data = 0
    if average_analysis_data:
        average_analysis_data = average_analysis_data[0]
    else:
        average_analysis_data = 0
    if question_data.exists():
        question_data = question_data[0]
        questions = json.loads(question_data.questionsJson)

        if result_data_from_database:
            result_data_from_database = result_data_from_database[0]
            section_data_from_database = json.loads(result_data_from_database.sectionResults)
            section_names = section_data_from_database['sectionsName']
            section_attempts = section_data_from_database['attemptsInSection']
            section_not_attempt = section_data_from_database['unAttemptInSection']
            section_total_questions = section_data_from_database['questionInSection']
            section_correct = section_data_from_database['correctAnsInSection']
            section_wrong = section_data_from_database['wrongInSection']
            zipped_data = zip(section_names, section_attempts, section_total_questions, section_correct, section_wrong,
                              section_not_attempt)
            context_data = {
                'first_name': request.user.first_name,
                'totalQuestions': result_data_from_database.totalAttempted + result_data_from_database.totalUnAttempted,
                'attempted': result_data_from_database.totalAttempted,
                'correct': result_data_from_database.totalCorrectAnswer,
                'wrong': result_data_from_database.totalWrongAnswer,
                'marks': result_data_from_database.marksObtained,
                'sectionResult': json.loads(result_data_from_database.sectionResults),
                'questionData': questions,
                'zipped_data': zipped_data,
                'question_id':question_id,
                'username':request.user.username,
                'feedback_needed':feedback_needed
            }
            return render(request, 'result.html', context_data)
        else:
            return HttpResponse('Invalid Question Set ID')
    else:
        return HttpResponse("You have not attempted this test")


def pdf_try(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


@login_required(login_url='/login/')
def admin_result(request):
    if request.user.is_staff:
        # Raw Query for retreiving data from database
        result = studentResponse.objects.raw(''' select q1.full_name ,
                                                q1.id,
                                                q2.questionSetID ,
                                                q2.marksObtained
                                                from wwcs.ninja1_userprofile as q1
                                                INNER JOIN result_studentresponse as q2
                                                on q1.email = q2.username ''')



        context = {
            'result_data' : result
        }
        return render(request, 'admin_result.html', context)

    else:
        raise Http404;


def feedback_msg(request):
    if request.method =='POST':
        username = request.user.username
        question_set = request.POST.get('question_set')
        feedback = request.POST.get('feedback')
        if feedback:
            new_feedback_data = Feedback(username = username, questionSetID = question_set, feedback = feedback)
            new_feedback_data.save();
        data_return = {'status': request.POST.get('feedback')}
        return HttpResponse(json.dumps(data_return), content_type='application/json')
    else:
        raise Http404
