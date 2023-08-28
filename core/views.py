from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from .renderers import UserRenderer
from .models import User, Subject, SectionYear, Chapter, Topic, Assignment, Resource, Plan, PlanAssignment, PlanResource, PlanTopic
from .serializers import ChapterCreateSerializer, UserRegisterationSerializer, UserLoginSerializer, UserProfileSerializer, SubjectViewSerializer, SubjectCreateSerializer, SectionCreateSerializer, ChapterViewSerializer, TopicCreateSerializer, AssignmentSerializer, ResourceSerializer, PlanCreateSerializer, TopicAddPlanSerializer, AssignmentAddPlanSerializer, ResourceAddPlanSerializer, PlanViewSerializer, AssignmentListSerializer, ResourceListSerializer 
from .plan_pdf import make_plan_table


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegisterationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    password = serializer.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectListCreateAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        return Subject.objects.prefetch_related('sectionyear_set').all().filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubjectCreateSerializer
        elif self.request.method == 'GET':
            return SubjectViewSerializer


class SubjectDeleteAPI(DestroyAPIView):
    serializer_class = SubjectCreateSerializer
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated]


class SectionYearCreateAPI(CreateAPIView):
    queryset = SectionYear.objects.all()
    serializer_class = SectionCreateSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]


class ChapterTopicAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        return Chapter.objects.prefetch_related('topic_set', 'assignment_set').all().filter(section_year=self.kwargs['id'])
   
    def get_serializer_class(self):
        if self.request.method == 'GET':
          return ChapterViewSerializer
        elif self.request.method == 'POST':
          return ChapterCreateSerializer


class ChapterDeleteAPI(DestroyAPIView):
    serializer_class = ChapterCreateSerializer
    queryset = Chapter.objects.all()
    permission_classes = [IsAuthenticated]


class TopicCreateAPI(CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicCreateSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]


class AssignmentCreateAPI(CreateAPIView):
   queryset = Assignment.objects.all()
   serializer_class = AssignmentSerializer
   permission_classes = [IsAuthenticated]
   renderer_classes = [UserRenderer]


class ResourceCreateAPI(CreateAPIView):
   queryset = Resource.objects.all()
   serializer_class = ResourceSerializer
   permission_classes = [IsAuthenticated]
   renderer_classes = [UserRenderer]


class PlanListCreateAPI(ListCreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      return Plan.objects.prefetch_related('plantopic_set', 'planassignment_set', 'planresource_set').all().filter(sectionyear=self.kwargs['id'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
          return PlanCreateSerializer
        elif self.request.method == 'GET':
           return PlanViewSerializer

class PlanDeleteAPI(DestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanCreateSerializer
    permission_classes = [IsAuthenticated]


# class PlanChapterCreateAPI(CreateAPIView):
#     queryset = PlanChapter.objects.all()
#     serializer_class = ChapterAddPlanSerializer
#     renderer_classes = [UserRenderer] 
#     permission_classes = [IsAuthenticated]


class PlanTopicCreateAPI(CreateAPIView):
    queryset = PlanTopic.objects.all()
    serializer_class = TopicAddPlanSerializer
    renderer_classes = [UserRenderer] 
    permission_classes = [IsAuthenticated]


class PlanAssigmentCreateAPI(CreateAPIView):
    queryset = PlanAssignment.objects.all()
    serializer_class = AssignmentAddPlanSerializer
    renderer_classes = [UserRenderer] 
    permission_classes = [IsAuthenticated]
    

class PlanResouceCreateAPI(CreateAPIView):
    queryset = PlanResource.objects.all()
    serializer_class = ResourceAddPlanSerializer
    renderer_classes = [UserRenderer] 
    permission_classes = [IsAuthenticated]


  
class PlanPdfView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self, request, id, format=None):
        data = Plan.objects.prefetch_related('plantopic_set', 'planassignment_set', 'planresource_set').all().filter(sectionyear=self.kwargs['id'])
        serializer = PlanViewSerializer(data, many=True)

        user = User.objects.get(id=request.user.id)
        section = SectionYear.objects.select_related('subject').get(id=self.kwargs['id'])
 
        filepath = make_plan_table(serializer.data, user.username, section.subject.sub_name, section.section)

        url = request.build_absolute_uri('/') + filepath[1:]


        return Response({"file":url}, status=status.HTTP_201_CREATED)



class AssignmentListViewAPI(ListAPIView):
    serializer_class = AssignmentListSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_queryset(self):
       return Chapter.objects.prefetch_related('assignment_set').filter(section_year=self.kwargs['id'])


class ResourceListViewAPI(ListAPIView):
    serializer_class = ResourceListSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_queryset(self):
       return Chapter.objects.prefetch_related('resource_set').filter(section_year=self.kwargs['id'])