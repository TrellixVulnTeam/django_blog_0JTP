from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
from markdown import markdown
from comment.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import  User
from django.utils import timezone
# Create your views here.

'''
def index(request):
    post_list = Post.objects.all()
    return render(request,'blog/index.html',context={'post_list':post_list})
'''

class IndexView(ListView):

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    '''
        wenlist = urllist()
        for i in range(29):
            content = text(wenlist[i])
            if  not  Post.objects.filter(title=content.get('title')[0]):
                body = '&nbsp;'+"<br>  &nbsp;".join(content.get('content')[:-14])

                new_post = Post(title=content.get('title')[0],body=body
                                    ,author=User.objects.get(username='birdywings')
                                    , created_time=timezone.now(), modified_time=timezone.now()
                                    , category=Category.objects.get(name='log')
                                    )
                new_post.save()
    '''

    def get_context_data(self, **kwargs):



        context = super().get_context_data(**kwargs)
        post_list = context.get("post_list")  # 页对象实例
        for post in post_list:
            post.excerpt = markdown(post.excerpt, extensions=[
                    'markdown.extensions.extra',
                ])

        paginator = context.get("paginator")  # 页对象实例
        page = context.get('page_obj')  # 获得当前页
        is_paginated = context.get('is_paginated')  # 是否分页
        pagination_date = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_date)
        return context

    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated :
            return {}
        first = False
        last = False
        left_has_more = False
        right_has_more = False  #是否需要省略号
        left = []
        right = []

        page_num = page.number #当前页码
        total_num = paginator.num_pages #总页数
        page_range = paginator.page_range #全部页码列表

        #当当前页数为1
        if page_num == 1 :
             right = page_range[page_num:page_num+2]
             if right[-1] < total_num-1 :
                 right_has_more = True
             if right[-1] < total_num :
                 last =True

        # 当当前页数为最后一页
        elif page_num == total_num :
            left = page_range[(page_num-3) if(page_num-3)>0 else 0 :page_num-1]
            if left[0] > 2:
                left_has_more = True
            if left[0] >1:
                first=True

        # 当当前页数既不是第一页也不是最后一页
        else :
            right = page_range[page_num:page_num+2]
            left =  page_range[(page_num-3) if(page_num-3)>0 else 0 :page_num-1]
            if right[-1] < total_num:
                last = True
            if left[0] > 1:
                first = True
            if right[-1] < total_num-1 :
                right_has_more = True
            if left[0] > 2:
                left_has_more = True

        data = {
            'left':left,
            'right':right,
            'first':first,
            'last':last,
            'right_has_more':right_has_more,
            'left_has_more': left_has_more,
        }
        return  data


'''
def detail(request,pk):
    post = Post.objects.get(pk=pk)
    post.increase_views()
    post.body = markdown(post.body,extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                               ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
               'form':form,
               'comment_list': comment_list,
               'lenght':len(comment_list)
               }
    return render(request,'blog/detail.html',context=context)
'''
class PostDetaileView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        response = super(PostDetaileView,self).get(request,*args,**kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetaileView, self).get_object(queryset=None)
        post.body = markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetaileView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({"form":form,
                        "comment_list":comment_list,
                        'lenght':len(comment_list)})
        return context



'''
def achives(request,year,month,day):
    post_list = Post.objects.filter(modified_time__year=year,modified_time__month=month
                                    ,modified_time__day=day).order_by('-modified_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
'''
class AchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        return super(AchivesView,self).get_queryset().filter(modified_time__year=self.kwargs.get('year')
                                                             ,modified_time__month=self.kwargs.get('month')
                                                             ,modified_time__day=self.kwargs.get('day'))

'''
def category(request,pk):
    post_list = Post.objects.filter(category=Category.objects.get(pk=pk)).order_by('-modified_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
'''
class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)


class TagView(ListView):

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


