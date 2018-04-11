from website.models import Video,UserProfile
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication

# 构建图片序列化器
class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=1)
    # owner = UserProfileSerializer()
    class Meta:
        model = Video
        fields = '__all__'
        depth = 1

# 构建用户序列化器
class UserSerializer(serializers.ModelSerializer):
    menuShow = serializers.BooleanField(default=False)
    class Meta:
        model = User
        fields = ("id", "is_superuser", "username", "password", "profile", "is_active", "menuShow")
        depth = 1

    def create(self, userdata):
            user = User(
                username=userdata['username']
            )
            # print(user)
            user.set_password(userdata['password'])
            user.save()
            new_user_profile = UserProfile(belong_to=user)
            user.profile.role = userdata['role']
            new_user_profile.save()
            # print(userdata['role'])
            return user

    def update(self, userdata):
            user = User.objects.get(id=userdata['userid'])
            print(user)
            user.username = userdata['username']
            user.set_password(userdata['password'])
            user.save()
            return user

    def invited(self, userdata):
            user = User.objects.get(id=userdata['userid'])
            try:
                new_userprofile = UserProfile(belong_to=user)
                user.profile.role = 'author'
                new_userprofile.save()
            except:
                user.profile.role = 'author'
                user.save()
            return user

@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def video(request):
    video_list = Video.objects.order_by('-id')
    if request.method == 'GET':
        if request.auth:
            serializer = VideoSerializer(video_list, many=True)
            return Response(serializer.data)
        else:
            serializer = VideoSerializer(video_list[:7], many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        ownerid = request.data['owner']
        owner = UserProfile.objects.get(id=ownerid)
        title = request.data['title']
        url_image = request.data['url_image']
        content = request.data['content']
        newvideo = Video(title=title, url_image=url_image, content=content, owner=owner)
        newvideo.save()
        # print('userid',userid)
        serializer = VideoSerializer(newvideo)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
def video_card(request, id):
    video_card = Video.objects.get(id=id)
    user = User.objects.get(username=request.data['username'])
    USER_CAN = {
        "DELETE": user.profile == video_card.owner or user.is_superuser
    }
    if request.method == 'PUT':
        serializer = VideoSerializer(video_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if USER_CAN["DELETE"]:
            video_card.delete()
            return Response({'msg': 'A-OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'You cant touch this'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def userlist(request):
    print(request.user)
    print(request.auth)
    user_list = User.objects.filter(is_superuser=False)
    if request.method == 'GET':
        if request.auth:
            serializer = UserSerializer(user_list, many=True)
            print(serializer.data)
            return Response(serializer.data)
        else:
            serializer = UserSerializer(user_list[:10], many=True)
            print(serializer.data)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def update_user(request):
    print(request.user)
    print(request.auth)
    print(request.data)
    if request.method == 'GET':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data)
                return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def get_user(request):
    # print(request.user)
    # print(request.auth)
    # print(request.data)
    user = User.objects.get(id=request.data['userid'])
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
def change_user(request, id):
    user = User.objects.get(id=id)
    if request.method == 'PUT':
        try:
            print(request.data['role'])
            user.profile.role = request.data['role']
            user.profile.save()
            print(user.profile.role)
            return Response(status=status.HTTP_201_CREATED)
        except:
            new_userprofile = UserProfile(belong_to=user)
            new_userprofile.role = request.data['role']
            print(new_userprofile)
            new_userprofile.save()
            print(new_userprofile)
            return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
            user.delete()
            return Response({'msg': 'Delete-OK'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def ban_user(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return Response({'msg': 'Ban-OK'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def is_Author(request):
    username = request.data['username']
    user = User.objects.get(username=username)
    role = user.profile.role

    if (role == 'author'):
        print('shiauthor')
        return Response({'msg': 'isAuthor', 'userid': user.profile.id}, status=status.HTTP_201_CREATED)
    else:
        print('bushiauthor')
        return Response({'msg': 'notAuthor', 'userid': user.profile.id}, status=status.HTTP_400_BAD_REQUEST)
