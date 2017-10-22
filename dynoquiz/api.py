from .models import Quiz, Question, Choice, QuizUser
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, UserSerializer, QuizUserSerializer, QuizScoreSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from permissions import IsOwnerOrReadOnly
#import pdb; pdb.set_trace()             #FOR TESTING


# class IsOwner(BasePermission):
#     def has_permission(self, request, view):
#         return False

#     def has_object_permission(self, request, view, obj):
#         # if request.methods in SAFE_METHODS:
#         #     return True

#         return False


# Helper functions
def get_quiz(quiz_id):
    try:
        return Quiz.objects.get(pk=quiz_id) 
    except Quiz.DoesNotExist:
        raise Http404

#Check quiz ownership of object before deleting it
#Retuns status code of delete
#If we put these in a helper class I bet we could use a decorator for check ownership
def delete_check(modelObject, quiz, user):
    if(quiz.owner == user):
        modelObject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

def put_object(serializedObject, quiz, user):
    if(check_ownership(quiz, user)):
        if serializedObject.is_valid():
            serializedObject.save()
            return Response(serializedObject.data)
        else:
            return Response(serializedObject.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

def post_object(serializedObject, quiz, user):
    if(check_ownership(quiz, user)):
        if serializedObject.is_valid():
            savedObj = serializedObject.save()
            return Response(serializedObject.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializedObject.errors, status=status.HTTP_400_BAD_REQUEST)

def check_ownership(quiz, user):
    if(quiz.owner == user):
        return True
    else:
        return False

class QuizList(APIView):
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    #return loggedin user's list of quizses
    def get(self, request, fromat=None):
        quizzes = Quiz.objects.filter(owner=request.user)
        serialized_quiz = QuizSerializer(quizzes, many=True)
        return Response(serialized_quiz.data)

    #create new quiz for logged in user
    def post(self, request, format=None):
        serializer = QuizSerializer(data=request.data)
        #userS = UserSerializer(request.user)
        if serializer.is_valid():
            newQuiz = serializer.save()
            #TODO: There's probably a better way to do this w/o two saves
            #add user to quiz
            newQuiz.owner = request.user
            newQuiz.save()

            #Create Quiz User relation with owner (so owner can take own quizzes)
            QuizUser.objects.create(user=request.user, quiz=newQuiz, available=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizDetail(APIView):
    # permission_classes = [
        # IsAuthenticated,
        # IsOwner,
    # ]
    def get(self, request, pk, format=None):
        quiz = get_quiz(pk)
        serialized_quiz = QuizSerializer(quiz)
        return Response(serialized_quiz.data)
    
    def delete(self, request, pk, format=None):
        quiz = get_quiz(pk)
        status = delete_check(quiz, quiz, request.user)
        return status

    def put(self, request, pk, format=None):
        quiz = get_quiz(pk)
        serializer = QuizSerializer(quiz, data=request.data)
        status = put_obj(serializer, quiz, request.user)
        return status 


class QuestionList(APIView):
    def get(self, request, pk, format=None):
        quiz = get_quiz(pk)
        questions = quiz.question_set.all()
        serialized_questions = QuestionSerializer(questions, many=True)
        return Response(serialized_questions.data)

    def post(self, request, pk, format=None):
        serializer = QuestionSerializer(data=request.data)
        quiz = get_quiz(pk)
        status = post_object(serializer, quiz, request.user)
        return status
        # if (quiz.owner == request.user):
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #      return Response(status=status.HTTP_401_UNAUTHORIZED)

class QuestionDetail(APIView):
    def get_question(self, question_id):
        try:
            return Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, question_id, format=None):
        question = self.get_question(question_id)
        serialized_question = QuestionSerializer(question)
        return Response(serialized_question.data)

    def delete(self, request, pk, question_id, format=None):
        question = self.get_question(question_id)
        quiz = question.quiz
        status = delete_check(question, quiz, request.user)
        return status

    def put(self, request, pk, question_id, format=None):
        question = self.get_question(question_id)
        quiz = question.quiz
        serializer = QuestionSerializer(question, data=request.data)
        status = put_object(serializer, quiz, request.user)
        return status

class ChoiceList(APIView):
    def get(self, request, question_id, format=None):
        choices = Question.objects.get(pk=question_id).choices
        serialized_choices = ChoiceSerializer(choices, many=True)
        return Response(serialized_choices.data)

    def post(self, request, question_id, format=None):
        serializer = ChoiceSerializer(data=request.data)
        question = Question.objects.get(pk=question_id)
        quiz = question.quiz
        status = post_object(serializer, quiz, request.user)
        return status
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChoiceDetail(APIView):
    def get_choice(self, choice_id):
        try:
            return Choice.objects.get(pk=choice_id)
        except Choice.DoesNotExist:
            raise Http404

    #TODO: Clean up, no need for question_id in any of these
    def get(self, request, question_id, choice_id, format=None):
        choice = self.get_choice(choice_id)
        serialized_choice = ChoiceSerializer(choice)
        return Response(serialized_choice)

    def delete(self, request, question_id, choice_id, format=None):
        choice = self.get_choice(choice_id)
        quiz = choice.question.quiz
        status = delete_check(choice, quiz, request.user)
        # choice.delete()
        return status

    def put(self, request, question_id, choice_id, format=None):
        choice = self.get_choice(choice_id)
        quiz = choice.question.quiz
        serializer = ChoiceSerializer(choice, data=request.data)
        status = put_object(serializer, quiz, request.user)
        return status

class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        #import pdb; pdb.set_trace()             #FOR TESTING
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data)

class UserDetail(APIView):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user = self.get_user(user_id)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)

    #checks for user name, returns none if username doesnt exist
    def get(self, request, username, format=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)

    #TODO: Delete
    # def put(self, request, user_id, format=None):
    #     user = self.get_user(user_id)
    #     serializer = UserSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Return quizzes that have been shared with the user
class AvailableQuizzes(APIView):
    #TODO: Consolidate this with other get user id
    #TODO: Find way to consolidate this entire function with the class UserDetail
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user = self.get_user(user_id)
        quizzes = user.quizzes.all().exclude(owner=user.id)
        serialized_quizzes = QuizSerializer(quizzes, many=True)
        return Response(serialized_quizzes.data)

#TODO:This class should be a user list class with different methods for different uses
class NonUserList(APIView):
    def get(self, request, quiz_id, format=None):
        nonUsers = User.objects.exclude(quizzes=quiz_id)

        serialized_nonUsers = UserSerializer(nonUsers, many=True)
        return Response(serialized_nonUsers.data)

#Handle Quiz User Relationships and Scores
class QuizUserDetailList(APIView):
    #TODO this is ugly messign with put in a post, might need to be two calls
    #Posts quiz user relation if it doesn't exist, else it updates the relationship
    def post(self, request, quiz_id, user_id, format=None):
        quiz = get_quiz(quiz_id)
        if(check_ownership(quiz, request.user)):
            try:
                #if quiz user already exists, update it
                quiz_user = QuizUser.objects.get(user__id=user_id, quiz__id=quiz_id)
                serializer = QuizUserSerializer(quiz_user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except QuizUser.DoesNotExist:
                #if quiz does not exist, post it
                serializer = QuizUserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



    def get(self, request, quiz_id, user_id, format=None):
        quiz_user = QuizUser.objects.get(user__id=user_id, quiz__id=quiz_id)
       # import pdb; pdb.set_trace()
        serialized_quiz_user = QuizUserSerializer(quiz_user, many=True)
        return Response(serialized_quiz_user.data)

#TODO: This should be included in view above QuizUserDetailList with just different get parameters
class QuizUserUserDetailList(APIView):
    #Get all quiz_users relations for a particular quiz
    def get(self, request, quiz_id, format=None):
        quiz_user = QuizUser.objects.filter(quiz_id=quiz_id)
        serializer = QuizUserSerializer(quiz_user, many=True)
        return Response(serializer.data)


class QuizScoreDetailList(APIView):
    def get(self, request, quiz_id, user_id, format=None):
        quiz_user = QuizUser.objects.get(user__id=user_id, quiz__id=quiz_id)
        quiz_score = quiz_user.scores
       # import pdb; pdb.set_trace()
        serialized_quiz_score = QuizScoreSerializer(quiz_score, many=True)
        return Response(serialized_quiz_score.data)

#TODO: Should updates be handled in serializer?
#add user to quiz
# class QuizUser(APIView):
#     def get_quiz(self, quiz_id):
#         try:
#             return Quiz.objects.get(pk=quiz_id)
#         except Quiz.DoesNotExist:
#             raise Http404
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             raise Http404
#
#     def put(self, request, quiz_id, user_id, format=None):
#         #import pdb; pdb.set_trace()             #FOR TESTING
#
#         quizSerialized =  QuizSerializer(self.get_quiz(quiz_id), data=request.data)
#         if quizSerialized.is_valid():
#             quizSerialized.update(self.get_quiz(quiz_id), request.data)
#
#             #quizSerialized.users.add(user_id)
#             quizSerialized.save()
#             return Response(quizSerialized.data)
#         else:
#             return Response(quizSerialized.errors, status=status.HTTP_400_BAD_REQUEST)
#
#









