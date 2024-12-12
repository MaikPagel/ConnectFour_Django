from django.shortcuts import render, redirect
from .models import Board, Player

def index(request):
    board = Board.objects.first()
    if not board:
        board = Board.objects.create()
    
    players = Player.objects.all()
    if players.count() < 2:
        Player.objects.create(name='Player 1', symbol='X')
        Player.objects.create(name='Player 2', symbol='O')
    
    current_player = request.session.get('current_player', 'Player 1')
    current_player = Player.objects.get(name=current_player)
    
    if request.method == 'POST':
        column = int(request.POST.get('column'))
        if board.drop_disc(column, current_player.symbol):
            if board.check_winner(current_player.symbol):
                return render(request, 'game/win.html', {'player': current_player})
            
            # Switch player
            next_player = 'Player 2' if current_player.name == 'Player 1' else 'Player 1'
            request.session['current_player'] = next_player
            current_player = Player.objects.get(name=next_player)  # Update current player for display

    board = Board.objects.first()
    return render(request, 'game/index.html', {'board': board, 'columns': range(board.columns), 'current_player': current_player})

def reset_game(request):
    Board.objects.all().delete()
    Player.objects.all().delete()
    Board.objects.create()
    Player.objects.create(name='Player 1', symbol='X')
    Player.objects.create(name='Player 2', symbol='O')
    request.session['current_player'] = 'Player 1'
    return redirect('index')
