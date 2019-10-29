import atexit, os, re, sys, threading, time
import chess
import common

colors = 'WB'

def start_bot(player, color, seed):
    try:
        bot = common.start(player, colors[color].lower(), seed)
    except OSError:
        print(colors[color ^ 1] + 'e')
        print()
        sys.exit()
    atexit.register(bot.terminate)
    return bot

def run_game(bots):
    time_forfeit_lock = threading.Lock()
    moves = 0
    board = chess.Board()
    def result(res, how):
        print(res + how)
        print(chess.Board().variation_san(board.move_stack))
        sys.exit()
    def timer_thread():
        last_moves = 0
        while True:
            time.sleep(5)
            time_forfeit_lock.acquire()
            if moves == last_moves:
                result(colors[~moves & 1], 'h')
            last_moves = moves
            time_forfeit_lock.release()
    failed_attempts = 0
    thread = threading.Thread(target=timer_thread)
    thread.daemon = True
    thread.start()
    while True:
        line = bots[moves & 1].stdout.readline()
        time_forfeit_lock.acquire()
        uci_attempts = common.line_to_moves(line)
        if uci_attempts is None:
            result(colors[~moves & 1], 'i')
        for uci_move in uci_attempts:
            try:
                board.push_uci(uci_move)
            except ValueError:
                pass
            else:
                if board.is_checkmate():
                    result(colors[moves & 1], 'c')
                if board.is_stalemate():
                    result('D', 's')
                if board.halfmove_clock == 200:
                    result('D', 'm')
                moves += 1
                failed_attempts = 0
                break
        else:
            failed_attempts += 1
            if failed_attempts == 2000:
                result(colors[~moves & 1], 'f')
        time_forfeit_lock.release()

def main(args):
    if len(args) == 4:
        common.init_players()
    elif len(args) == 5:
        common.init_players(args[4])
    else:
        sys.exit('Usage: <white player> <white seed> <black player> <black seed> [player config]')
    white_player = common.get_player(args[0])
    white_seed = int(args[1])
    black_player = common.get_player(args[2])
    black_seed = int(args[3])
    run_game([start_bot(white_player, 0, white_seed), start_bot(black_player, 1, black_seed)])

if __name__ == '__main__':
    main(sys.argv[1:])
