from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from .models import Board,Topic,Post
from django.contrib.auth.models import User

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
    board = Board.objects.get(pk=id)
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        print(subject,message)
        user = User.objects.first()
        topic = Topic.objects.create(
            subject = subject,
            board = board,
            created_by= user,
        )
        post = Post.objects.create(
            message = message,
            topic = topic,
            created_by= user,

        )
        return redirect('board_topic',id=board.pk)


    return render(request,'new_topic.html',{'board':board})