from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from .models import Comment
from .forms import CommentForm
from blog.models import Post


# Create your views here.
def post_comment(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST' : #提交表单 POST方法
        form = CommentForm(request.POST) #包含表单POST上来的信息
        if form.is_valid():
            comment = form.save(commit=False) #创建模型
            comment.post = post
            comment.save()
            return redirect(post)
    return redirect(post)

