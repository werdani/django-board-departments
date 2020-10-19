from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from .models import Board,Topic,Post
from django.contrib.auth.models import User
from .forms import NewTopic
from django.contrib.auth.decorators import login_required
from boards.forms import PostForm

# Create your views here.

'''
def home(request):
    boards = Board.objects.all()
    board_name = []
    for board in boards:
        board_name.append(board.name)
    html = '<br>'.join(board_name)
    return HttpResponse(html)

'''
def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def about(request):
    pass
def board_topic(request,id):
    #try:
    #    board = Board.objects.get(pk=board_id)
    #except Board.DoesNotExist:
    #    raise Http404
    board = get_object_or_404(Board,pk=id) #this line = 5 line up.
    
    return render(request,'topic.html',{'board':board})



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

            return redirect('topics_posts',id=id,topic_id=topic_id)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})