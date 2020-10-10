from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponse
from .models import Board
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
def board_topic(request,board_id):
    #try:
    #    board = Board.objects.get(pk=board_id)
    #except Board.DoesNotExist:
    #    raise Http404
    board = get_object_or_404(Board,pk=board_id) #this line = 5 line up.
    return render(request,'topic.html',{'board':board})