import collections, json, os, re, subprocess, sys

base_dir = os.path.dirname(__file__)
players_dir = os.path.join(base_dir, 'players')

Player = collections.namedtuple('Player', ['name', 'dir', 'build', 'run'])

def uncomment_json(s):
    return re.sub(r'("(?:\\?.)*?")|/\*.*?\*/', lambda m: m.group(1) or '', s, flags=re.DOTALL)
def is_cmd_type(x):
    return type(x) is list and all(type(y) is str for y in x)

def init_players(path=None):
    if path is None:
        path = os.path.join(base_dir, 'players.json')
    global vars
    global players
    config = json.loads(uncomment_json(open(path).read()))
    vars = config['vars']
    if 'PYTHON3' not in vars:
        vars['PYTHON3'] = sys.executable
    players = config['players']

def substitute_vars(cmd):
    assert type(cmd) is list and all(type(y) is str for y in cmd)
    return [re.sub(r'\$(.*?)\$', lambda m: vars[m.group(1)], arg) for arg in cmd]

def get_player(name):
    conf = players[name]
    dir = os.path.join(players_dir, name)
    assert os.path.isdir(dir)
    assert type(conf) is dict
    assert set(conf) <= {'build', 'run'}
    if 'build' in conf:
        assert type(conf['build']) is list
        build = [substitute_vars(cmd) for cmd in conf['build']]
    else:
        build = []
    assert 'run' in conf
    run = substitute_vars(conf['run'])
    return Player(name, dir, build, run)

def start(player, color, seed):
    os.chdir(player.dir)
    return subprocess.Popen(player.run + [color, str(seed)],
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)

def line_to_moves(line):
    tokens = line.split()
    if len(tokens) not in (2, 3):
        return None
    if len(tokens) == 3:
        if tokens[2] not in [b'q', b'r', b'b', b'n']:
            return None
        promotion = tokens[2].decode('ascii')
    elif len(tokens) == 2:
        promotion = 'q'
    else:
        return None
    if not all(re.match(b'^[a-h][1-8]$', t) for t in tokens[:2]):
        return None
    move = (tokens[0] + tokens[1]).decode('ascii')
    return [move, move + promotion]

