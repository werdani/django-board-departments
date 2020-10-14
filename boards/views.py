from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from .models import Board,Topic,Post
from django.contrib.auth.models import User
from .forms import NewTopic

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

def new_topic(request,id):
    board = get_object_or_404(Board,pk=id)
    form = NewTopic()
    user = User.objects.first()
    if request.method == "POST":
        form = NewTopic(request.POST)
        if form.is_valid():
            topic= form.save(commit=False)
            topic.board= board
            topic.created_by = user
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                created_by = user,
                topic=topic
            )
            return redirect('board_topic',id=board.pk)
    else:
        form = NewTopic()
    return render(request,'new_topic.html',{'board':board,'form':form})