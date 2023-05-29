from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Group, Post


@login_required
def index(request):
    groups = request.user.user_groups.all()
    context = {
        'groups': groups,
    }
    return render(request, 'groups/index.html', context)


# class PostsList(APIView):
#     def get_group(self, group_pk):
#         try:
#             return Group.objects.get(pk=group_pk)
#         except Group.DoesNotExist:
#             raise Http404

#     def post(self, request, group_pk):
#         group = self.get_group(group_pk)
#         new_post = PostSerializer(data=request.data)
#         success = True
#         if new_post.is_valid():
#             new_post.save(user=request.user, group=group)
#             post = Post.objects.get(pk=new_post.data['id'])
#             images = dict(request.data.lists())['image']
#             arr = []
#             for image in images:
#                 image_serializer = PostImageSerializer(data={'image': image})
#                 if image_serializer.is_valid():
#                     image_serializer.save(post=post)
#                     arr.append(image_serializer.data)
#                 else:
#                     success = False
#         else:
#             success = False
#         if success:
#             return Response({'post': new_post.data,
#                             'images': arr,},
#                             status=status.HTTP_201_CREATED)
#         else:
#             return Response({'post': new_post.data,
#                             'images': arr,},
#                             status= status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     def get_post(self, post_pk):
#         try:
#             return Post.objects.get(pk=post_pk)
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, post_pk):
#         post = self.get_post(post_pk)
#         # 조회수
#         if request.user not in post.hits.all():
#             post.hits.add(request.user)

#         serializer = PostReadSerializer(post)
#         return Response(serializer.data)
    
#     def delete(self, request, post_pk):
#         post = self.get_post(post_pk)
#         # media file에서 image file 삭제 아직--
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

    # def put(self, request, post_pk):
    #     post = self.get_post(post_pk)
