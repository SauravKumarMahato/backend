from rest_framework import serializers

from .models import User, SectionYear, Subject, Topic, Chapter, Assignment, Resource, Plan, PlanAssignment, PlanTopic, PlanResource


class UserRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['username','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


# Serializer for sections:
class SectionSeializer(serializers.ModelSerializer):
    class Meta:
        model = SectionYear
        fields = ['id', 'section']

# Serializer for viewing subjects and sections:
class SubjectViewSerializer(serializers.ModelSerializer):
    sectionyear_set = SectionSeializer(many=True)
    class Meta:
        model = Subject
        fields = ['id', 'sub_name','sectionyear_set']
    queryset = Subject.objects.all()


# Serializer for creating subject.
class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'sub_name','user']



# serializer for creating section year.
class SectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionYear
        fields = ['id','section', 'subject']


# serializer for viewing Topics.
class TopicViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'topic_name']


# serializer for viewing assignment
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'assign_name','file','chapter']


# serializer for viewing resources. 
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource 
        fields = ['id', 'res_name','file','chapter']


# serializer for viewing Chpater and topic.
class ChapterViewSerializer(serializers.ModelSerializer):
    topic_set = TopicViewSerializer(many=True) 
    assignment_set = AssignmentSerializer(many=True)
    resource_set = ResourceSerializer(many=True)
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_name', 'section_year', 'topic_set','assignment_set','resource_set']


# serializer for creating chapters.
class ChapterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_name','section_year']


# serializer for creating topics.
class TopicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'topic_name', 'chapter']


# serializer for viewing chapter in plan
class ChapterOnlyViewPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id','chapter_name']


class TopicOnlyViewPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'topic_name']

class AssignmentOnlyViewPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'assign_name']

class ResourceOnlyViewPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'res_name']


# serializer for adding Chapter in Plan
# class ChapterAddPlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PlanChapter
#         fields = ['plan', 'chapter'] 

# class ChapterViewPlanSerializer(serializers.ModelSerializer):
#     chapter = ChapterOnlyViewPlanSerializer()
#     class Meta:
#         model = PlanChapter
#         fields = ['chapter']


# serializer for adding Topic in Plan
class TopicAddPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanTopic
        fields = ['plan', 'chapter','topic'] 


class TopicViewPlanSerializer(serializers.ModelSerializer):
    topic = TopicOnlyViewPlanSerializer()
    chapter = ChapterOnlyViewPlanSerializer()
    class Meta:
        model = PlanTopic
        fields = ['chapter', 'topic']


# serializer for adding assginment in Plan
class AssignmentAddPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanAssignment
        fields = ['plan','chapter', 'assignment'] 


class AssignmentViewPlanSerializer(serializers.ModelSerializer):
    assignment = AssignmentOnlyViewPlanSerializer()
    chapter = ChapterOnlyViewPlanSerializer()
    class Meta:
        model = PlanAssignment
        fields = ['chapter','assignment']


# serializer for adding Resources in Plan
class ResourceAddPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanResource
        fields = ['plan','chapter', 'resource'] 


class ResourceViewPlanSerializer(serializers.ModelSerializer):
    resource = ResourceOnlyViewPlanSerializer()
    chapter = ChapterOnlyViewPlanSerializer()
    class Meta:
        model = PlanResource
        fields = ['chapter','resource']


# serializer for creating in plan
class PlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'plan_name', 'sectionyear']

# serializer for viewing plan
class PlanViewSerializer(serializers.ModelSerializer):
    plantopic_set = TopicViewPlanSerializer(many=True)
    planassignment_set = AssignmentViewPlanSerializer(many=True)
    planresource_set = ResourceViewPlanSerializer(many=True)
    class Meta:
        model = Plan
        fields = ['id', 'plan_name', 'sectionyear', 'plantopic_set', 'planassignment_set','planresource_set']



class AssignmentListSerializer(serializers.ModelSerializer):
    assignment_set = AssignmentSerializer(many=True)
    class Meta:
        model = Chapter
        fields = ['id','chapter_name', 'assignment_set']


class ResourceListSerializer(serializers.ModelSerializer):
    resource_set = ResourceSerializer(many=True)
    class Meta:
        model = Chapter 
        fields = ['id','chapter_name', 'resource_set']