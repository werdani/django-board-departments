from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from .models import Board,Topic,Post
from django.contrib.auth.models import User
from .forms import NewTopic
from django.contrib.auth.decorators import login_required
from boards.forms import PostForm
from django.db.models import Count
from django.views.generic import UpdateView , ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

'''
def home(request):
    boards = Board.objects.all()
    board_name = []
    for board in boards:
        board_name.append(board.name)
    html = '<br>'.join(board_name)
    return HttpResponse(html)


def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

'''

class Boardlistview(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

def about(request):
    pass
def board_topic(request,id):
    #try:
    #    board = Board.objects.get(pk=board_id)
    #except Board.DoesNotExist:
    #    raise Http404
    board = get_object_or_404(Board,pk=id) #this line = 5 line up.
    topics = board.topics.order_by('-created_dt').annotate(comments=Count('posts'))
    page = request.GET.get('page',1)
    paginator = Paginator(topics,20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage :
        topics = paginator.page(paginator.num_pages)

    return render(request,'topic.html',{'board':board,'topics':topics})



@login_required
def new_topic(request,id):
    board = get_object_or_404(Board,pk=id)
    form = NewTopic()
     #user = User.objects.first()
    if request.method == "POST":
        form = NewTopic(request.POST)
        if form.is_valid():
            topic= form.save(commit=False)
            topic.board= board
            topic.created_by = request.user
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                created_by = request.user,
                topic=topic
            )
            return redirect('board_topic',id=board.pk)
    else:
        form = NewTopic()
    return render(request,'new_topic.html',{'board':board,'form':form})

def topics_posts(request,id,topic_id):
    topic = get_object_or_404(Topic,board__pk =id,pk=topic_id)
    session_key = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(session_key,False):
        topic.views+=1
        topic.save()
        request.session[session_key] = True
    return render(request,'topic_posts.html',{'topic':topic})

@login_required
def reply_topic(request,id,topic_id):
    topic = get_object_or_404(Topic,board__pk =id,pk=topic_id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit=False)
            post.topic=topic
            post.created_by = request.user
            post.save()
            topic.updated_by = request.user
            topic.updated_dt = timezone.now()
            topic.save()

            return redirect('topics_posts',id=id,topic_id=topic_id)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})




@method_decorator(login_required,name='dispatch')
class PostUpdateview(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post=form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topics_posts',id=post.topic.board.pk,topic_id=post.topic.pk)
