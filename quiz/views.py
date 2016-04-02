from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from quiz.models import Questions as questions
from result.models import studentResponse
from django.db.models import Q
import datetime
import json

# Create your views here.
@login_required(login_url='/login/')
def attempt_quiz(request):
    username = request.user.username
    date_today = datetime.date.today()
    question_data = questions.objects.filter(Q(startDate__lte=date_today) & Q( endDate__gte=date_today))
    if question_data.exists():
        question_data_from_database = question_data[0]
        question_id = question_data_from_database.questionSetID
        if check_user_attempted_question_set(username,question_id):
            questions_to_display = json.loads(question_data_from_database.questionsJson)
            total_questions = len(questions_to_display)
            total_time = question_data_from_database.totalTime
            category_code = question_data_from_database.categoryCode
            context = {
                'qid':question_id,
                'categoryCode':category_code,
                'questionData':questions_to_display,
                'totalQuesions':total_questions,
                'totalTime':total_time
            }
            return render(request,'frame.html',context)
        else:
            redirect_url = '/result/'+question_id
            return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponse('Question Set Not Exist')

def get_student_response(request):
    if request.method == 'POST':
        student_response_data = request.POST
        username = request.user.username
        category_code = student_response_data.get('categoryCode')
        question_set_id = student_response_data.get('questionID')
        serialized_student_response = student_response_data.get('studentResponse')
        student_response_in_json = json.loads(student_response_data.get('studentResponse'))
        question_data_from_database, student_response_valid = fetch_question_data_and_validate(question_set_id,
                                                                                               student_response_in_json)
        if question_set_exist(question_set_id) and student_response_valid and \
                check_user_attempted_question_set(username,question_set_id):

            """
            We have validated the student response we received from user and it is correct.
            Now our aim is to calculate the result. Code for calculating the result is written in this part.

            """
            sections_list = json.loads(question_data_from_database.questionSections)
            total_number_of_sections = len(sections_list)

            """
            Below part initializes different variables used in this process
            """

            questions_in_each_section = [0] * total_number_of_sections
            attempts_in_each_section = [0] * total_number_of_sections
            correct_ans_each_section = [0] * total_number_of_sections
            unattempt_in_each_section = [0] * total_number_of_sections
            wrong_in_each_section = [0] * total_number_of_sections
            marks_in_each_section = [0] * total_number_of_sections
            time_for_each_section = [0] * total_number_of_sections

            """
            Initilize iterator, correct, wrong, marks obtained as zero and initilize negative marks value.
            """

            correct_answers = 0
            wrong_answers = 0
            marks_obtained = 0
            negative_marks = 0.25
            iterator = 0

            question_data_in_json = json.loads(question_data_from_database.questionsJson)

            for item in question_data_in_json:
                """ Here we increments the question section"""
                current_section = int(item['questionSection'])
                questions_in_each_section[current_section] += 1

                """ Here we check whether the student un-attempted a question"""
                if student_response_in_json[iterator] == 0 or student_response_in_json[iterator] == None or \
                                student_response_in_json[iterator][0] == None or student_response_in_json[iterator][0]==0:
                    if student_response_in_json[iterator] == 0 or student_response_in_json[iterator] == None:
                        unattempt_in_each_section[current_section] += 1
                        iterator += 1
                    else:
                        unattempt_in_each_section[current_section] += 1
                        time_for_each_section[current_section] += int(student_response_in_json[iterator][1])
                        iterator += 1

                elif item['correctAnswer'] == student_response_in_json[iterator][0]:
                    attempts_in_each_section[current_section] += 1
                    correct_ans_each_section[current_section] += 1
                    time_for_each_section[current_section] += int(student_response_in_json[iterator][1])
                    correct_answers += 1
                    iterator += 1

                else:
                    attempts_in_each_section[current_section] += 1
                    wrong_in_each_section[current_section] += 1
                    time_for_each_section[current_section] += int(student_response_in_json[iterator][1])
                    wrong_answers += 1
                    iterator += 1

            marks_obtained = float(correct_answers - wrong_answers * negative_marks)
            total_questions = sum(questions_in_each_section)
            total_correct_answers = sum(correct_ans_each_section)
            total_wrong_answers = sum(wrong_in_each_section)
            total_time_taken = sum(time_for_each_section)
            total_unattempted = sum(unattempt_in_each_section)
            total_attempted = sum(attempts_in_each_section)

            section_data_to_database = {
                'sectionsName': sections_list,
                'questionInSection': questions_in_each_section,
                'attemptsInSection': attempts_in_each_section,
                'correctAnsInSection': correct_ans_each_section,
                'unAttemptInSection': unattempt_in_each_section,
                'wrongInSection': wrong_in_each_section,
                'timeTakenSection': time_for_each_section
            }

            section_data_to_database_json = json.dumps(section_data_to_database)

            student_result = studentResponse(username=username, categoryCode=category_code,
                                             questionSetID=question_set_id, response=serialized_student_response,
                                             sectionResults=section_data_to_database_json, marksObtained=marks_obtained,
                                             totalCorrectAnswer=total_correct_answers,
                                             totalWrongAnswer=total_wrong_answers, totalTimeTaken=total_time_taken,
                                             totalUnAttempted=total_unattempted, totalAttempted=total_attempted)
            student_result.save()

            redirect_url = "/result/"+question_set_id+"/"

            return HttpResponseRedirect(redirect_url)

        else:
            return HttpResponse('Hi, Your data received is not valid, so try again')
    else:
        return HttpResponse('Error, The request is not a POST request, Sorry')


def question_set_exist(question_set_id):
    if questions.objects.filter(questionSetID=question_set_id).exists():
        return True
    else:
        return False


def fetch_question_data_and_validate(question_set_id, student_response):
    question_data_from_database = questions.objects.filter(questionSetID=question_set_id)[0]
    if question_data_from_database.totalQuestions == len(student_response):
        valid = True
    else:
        valid = False
    return question_data_from_database, valid


def check_user_attempted_question_set(username, question_set_id):
    whether_already_attempted = studentResponse.objects.filter(Q(username=username)&Q(questionSetID=question_set_id))
    if whether_already_attempted:
        return False
    else:
        return True
