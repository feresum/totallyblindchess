#!/usr/bin/python3

import argparse, os, queue, random, subprocess, sys, threading
import common

def make_seed(random):
    return random.randrange(1 << 63)

def banner(msg, fill):
    print(msg.center(60, fill))

def build(args):
    players = [common.get_player(name) for name in args.players]
    for p in players:
        if p.build:
            banner('Building ' + p.name, '=')
            os.chdir(p.dir)
            for cmd in p.build:
                try:
                    subprocess.check_call(cmd)
                except OSError as e:
                    banner('Failed to build ' + p.name, '!')
                    print('This command returned failed to start: %s' % cmd)
                    sys.exit(1)
                except subprocess.CalledProcessError as e:
                    banner('Failed to build ' + p.name, '!')
                    print('This command returned %d: %s' % (e.returncode, cmd))
                    sys.exit(1)
            banner('Successfully built ' + p.name, '=')

def fight(args):
    [common.get_player(name) for name in args.players] # Validate
    players = {name + ('/%d' % args.players[:i].count(name)) * (args.players.count(name) > 1): name
               for i, name in enumerate(args.players)}
    task_q = queue.Queue()
    out_q = queue.Queue()
    def worker():
        while True:
            player_w, seed_w, player_b, seed_b = task_q.get()
            proc_args = [sys.executable, os.path.join(common.base_dir, 'game_helper.py'),
                         players[player_w], str(seed_w), players[player_b], str(seed_b)]
            if args.player_config is not None:
                proc_args.append(args.player_config)
            try:
                out = subprocess.check_output(proc_args)
            except subprocess.CalledProcessError:
                banner('ERROR in game_helper subprocess', '!')
                os._exit(2)
            out_q.put((player_w, player_b, out))
    for _ in range(args.parallelism):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    print('Seed:', args.seed)
    rando = random.Random(args.seed)
    score = {p: 0 for p in players}
    matches = [(a, b) for a in players for b in players if a is not b]
    move_log = open(args.move_log, 'w')
    for c in range(args.cycles):
        rando.shuffle(matches)
        for w,b in matches:
            task_q.put((w, make_seed(rando), b, make_seed(rando)))
        for _ in range(len(matches)):
            name_w, name_b, output = out_q.get()
            ((winner, how), notation) = map(str.strip, output.decode('ascii').splitlines())
            score[name_w] += {'W':2, 'D':1, 'B':0}[winner]
            score[name_b] += {'W':0, 'D':1, 'B':2}[winner]
            print('%-20s %-20s %s %s %4d' %(name_w, name_b, winner, how, notation.count('.')), file=sys.stderr)
            print(name_w, name_b, winner, how, notation, file=move_log)
        banner('Standings after %d cycle%s:' % (c + 1, 's'[:c]), '=')
        for z in sorted(score.items(), key=lambda z:z[1]):
            print('  %-20s %5d' % z)
        banner('', '=')

def sample_output(player, color, seed):
    def fail(msg):
        banner('Failed: ' + player.name, '!')
        sys.exit(msg)
    try:
        proc = common.start(player, color, seed)
    except OSError:
        fail('Run command failed to start.')
    moves = []
    for _ in range(1000):
        line = proc.stdout.readline()
        attempts = common.line_to_moves(line)
        if attempts is None:
            fail('Invalid output line: %r' % line)
        moves.append(attempts[1])
    proc.terminate()
    return moves

def check(args):
    players = [common.get_player(name) for name in args.players]
    for p in players:
        banner('Checking ' + p.name, '=')
        for color in 'wb':
            seed = make_seed(random)
            out0, out1 = (sample_output(p, color, seed) for _ in range(2))
            if out0 != out1:
                banner('Failed: ' + p.name, '!')
                sys.exit('Player produced two different outputs given args %s %d' % (color, seed))
        banner('OK: ' + p.name, '=')

U = '''controller.py [--players=alice,bob,...] build
       controller.py [--players=alice,bob,...] check
       controller.py [--players=alice,bob,...] fight [--cycles=N] [--parallelism=N] [--move-log=filename]'''

def main():
    ap = argparse.ArgumentParser(usage=U)
    ap.add_argument('--players', type=lambda s: list(filter(None, s.split(','))), help='Players to include (may repeat for fight)')
    ap.add_argument('--player-config', help='File containing player config (default players.json)')
    subparsers = ap.add_subparsers(title='command')
    subparsers.add_parser('build', usage=U).set_defaults(func=build)
    subparsers.add_parser('check', usage=U).set_defaults(func=check)
    ap_fight = subparsers.add_parser('fight', usage=U)
    ap_fight.set_defaults(func=fight)
    ap_fight.add_argument('--seed', type=int, default=make_seed(random), help='Random seed for the tournament')
    ap_fight.add_argument('--cycles', type=int, default=1<<60, help='Number of double-round-robin cycles to run')
    ap_fight.add_argument('--parallelism', type=int, default=1, help='Number of games to run concurrently (default: 1)')
    ap_fight.add_argument('--move-log', default=os.devnull, help='File to which to record the moves of the games')
    args = ap.parse_args()
    if not hasattr(args, 'func'):
        ap.print_help()
        sys.exit(1)
    common.init_players(args.player_config)
    if args.players is None:
        args.players = list(common.players)
    args.func(args)

if __name__ == '__main__':
    main()
