#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request, escape, jsonify
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
import json
import random
import copy
import uuid
import pymongo

db_prefix = '/var/www/TeddyPoCards/'

@app.route('/mon')
def mongo():
    myclient = pymongo.MongoClient(app.config["MONGOSTRING"])
    mydb = myclient["dev_db"]
    rooms = mydb["room"]
    rooms.drop()

    random.seed(0)
    def create_room(room_name, game_master, is_private=False, game_name=''):
        if rooms.find({"room_name": room_name}).count() > 0:
            # If the room exists, join the room
            return join_room(room_name, game_master)
        game_params = dict()
        if game_name == 'Overthrown':
            game_params["approval_timer"] = "disabled"
            # game_params["approval_timer"] = "infinite"
        return rooms.insert_one(dict(room_name=room_name,
            game_master=game_master,
            is_private=is_private,
            game_name=game_name,
            players=[game_master],
            game_state='waiting',
            game_data=dict(),
            game_params=game_params))
    def delete_room(room_name):
        query={"room_name": room_name}
        rooms.delete_many(query)
    def join_room(room_name, user_name):
        if rooms.find({"room_name": room_name}).count() == 0:
            room = create_room(room_name, user_name)
        room = rooms.find_one({"room_name": room_name})
        myquery={"room_name": room_name}
        players = []
        if "players" in room:
            players = room["players"]
        if user_name not in players:
            players.append(user_name)
            newvalues = {"$set": {"players": players}}
            rooms.update_one(myquery, newvalues)
    def modify_room(room_name, action, params=dict()):
        query={"room_name": room_name}
        if action == 'waiting':
            query={"room_name": room_name}
            newvalues = {"$set": {"game_state": "waiting"}}
            rooms.update_one(query, newvalues)
        elif action == 'started':
            query={"room_name": room_name, "game_state": "waiting",
                    "game_name": "Overthrown"}
            room = rooms.find_one(query);
            if room is not None:
                newvalues = {"$set": {
                    "game_state": "started",
                    "game_data": create_game(room)}
                }
                rooms.update_one(query, newvalues)
        elif action == 'play_action':
            query={"room_name": room_name, "game_state": "started",
                    "game_name": "Overthrown"}
            room = rooms.find_one(query);
            if room is not None:
                game_data = action_game(room, params) 
                if game_data is not None:
                    newvalues = {"$set": {
                        "game_data": game_data}
                    }
                    rooms.update_one(query, newvalues)

    def get_next_player_name(game_data, last_player):
        players = game_data["players"]
        found_last = False
        for i in range(len(players)*2):
            player = players[i % len(players)]
            if found_last == True and len(player["cards"]) > 0:
                return player["user_name"]
            if player["user_name"] == last_player:
                found_last = True
        return 'this should never happen maybe increase you loop length'

    def create_game(room):
        deck = []
        for item in ["Duke", "Cantessa", "Assassin", "Ambassador", "Captain"]:
            for i in range(3):
                deck.append(item)
        random.shuffle(deck)
        players = []
        for item in room["players"]:
            player = dict(user_name=item, coins=2, cards = [])
            for i in range(2):
                if len(deck) > 0:
                    player["cards"].append(deck.pop())
            players.append(player)
        grave_yard = []
        action_log = []
        if len(players) > 0:
            waiting_for = [dict(kind='turn', user_name=random.choice(players)["user_name"])]
        else:
            waiting_for = []
        return dict(deck=deck,
            players=players,
            prev_players=copy.deepcopy(players),
            grave_yard=grave_yard,
            action_log=action_log,
            waiting_for=waiting_for)
    def action_game(room, params):
        # Read some params
        user_name = params["user_name"]
        action = params["action"]

        # Check if action is allowed and expire appropriate waiting_for actions
        allowed = False
        for item in room["game_data"]["waiting_for"]:
            if action == "income" and item["kind"] == "turn" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action == "foreign_aid" and item["kind"] == "turn" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action == "allow" and item["kind"] == "block" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"].remove(dict(kind="block", user_name=user_name))
                allowed = True
            elif action == "allow" and item["kind"] == "challenge" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"].remove(dict(kind="challenge", user_name=user_name))
                allowed = True
            elif action == "block" and item["kind"] == "block" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"] = []
                allowed = True
        if not allowed:
            return None

        # Add the allowed action to the log
        room["game_data"]["action_log"].append(params)

        # Backup the game state (for potential blocks)
        if action != "allow":
            # harmless for income to do a backup
            # required for foreign aid to do a backup
            # required for a block to do a backup
            temp_backup = copy.deepcopy(room["game_data"]["prev_players"])
            room["game_data"]["prev_players"] = copy.deepcopy(room["game_data"]["players"])

        # Modify cards and coins with the turn actions
        players = room["game_data"]["players"]
        for item in players:
            if action == "income" and item["user_name"] == user_name:
                item["coins"] += 1
            elif action == "foreign_aid" and item["user_name"] == user_name:
                item["coins"] += 2
            elif action == "block" and item["user_name"] == user_name:
                room["game_data"]["players"] = temp_backup

        # Add next actions game can wait for
        if action == 'income':
            next_player = get_next_player_name(room["game_data"], user_name)
            room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
        elif action == 'foreign_aid':
            if room["game_params"]["approval_timer"] == "disabled":
                next_player = get_next_player_name(room["game_data"], user_name)
                room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='block', user_name=item["user_name"]))
        elif action == "allow" and len(room["game_data"]["waiting_for"]) == 0:
            for item in reversed(room["game_data"]["action_log"]):
                if item["action"] in ["income", "foreign_aid", "tax", "steal", "assassin", "exchange", "coup"]:
                    next_player = get_next_player_name(room["game_data"], item["user_name"])
                    break
            room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
        elif action == "block":
            if room["game_params"]["approval_timer"] == "disabled":
                for item in reversed(room["game_data"]["action_log"]):
                    if item["action"] in ["income", "foreign_aid", "tax", "steal", "assassin", "exchange", "coup"]:
                        next_player = get_next_player_name(room["game_data"], item["user_name"])
                        break
                room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='challenge', user_name=item["user_name"]))


        return room["game_data"]




    create_room('sk', 'p1', True, 'Overthrown')
    join_room('sk', 'p2')
    join_room('sk', 'p3')
    join_room('sk', 'p4')
    modify_room('sk', 'started')
    action_params = dict()
    action_params["user_name"] = "p2"
    action_params["action"] = "income"
    modify_room('sk', 'play_action', action_params) # fail cuz not his turn
    action_params = dict()
    action_params["user_name"] = "p3"
    action_params["action"] = "income"
    modify_room('sk', 'play_action', action_params)
    action_params = dict()
    action_params["user_name"] = "p4"
    action_params["action"] = "foreign_aid"
    modify_room('sk', 'play_action', action_params)
    modify_room('sk', 'play_action', params=dict(user_name="p1", action="allow"))
    modify_room('sk', 'play_action', params=dict(user_name="p2", action="allow"))
    modify_room('sk', 'play_action', params=dict(user_name="p3", action="allow"))
    modify_room('sk', 'play_action', params=dict(user_name="p1", action="foreign_aid"))
    modify_room('sk', 'play_action', params=dict(user_name="p2", action="block")) # rightful duke doing a righteous block
    modify_room('sk', 'play_action', params=dict(user_name="p1", action="allow"))
    modify_room('sk', 'play_action', params=dict(user_name="p3", action="allow"))
    modify_room('sk', 'play_action', params=dict(user_name="p4", action="allow"))
    myquery = dict()
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    for item in rooms.find(myquery):
        pp.pprint(item)
    rooms.drop()


    #x = mycoll.insert_one(dict(user_name='steve'))
    #print(x.inserted_id)
    #myquery = dict(user_name='steve')
    #for item in mycoll.find(myquery):
    #    print(item)
    #print(myclient.list_database_names())
    # game is one mongodb document and if two people access something at the same time their browser is just told to try again and it does
    # mycoll.drop()
    return jsonify(dict(hi=1))

@app.route('/')
def hello():
    return render_template('landing_page.html')
    #return redirect(url_for('join_page'))

@app.route('/action/<user_name>/<action_string>/<room_name>')
def action(user_name, action_string, room_name):
    is_ajax = False
    with open(db_prefix+'state.json', "r") as statef:
        state = json.load(statef)
    room = state.get('rooms', dict(room_name=None)).get(room_name, None)
    if room is None:
        return "Room Not Found" # TODO
    game_data = room.get("game_data", dict())
    room["game_data"] = game_data
    game_data['activity_log'] = game_data.get('activity_log', [])
    act_split = action_string.split('_')
    print(act_split)
    if act_split[0] == "increase":
        for item in game_data.get('players', []):
            if item.get('user_name', '') == act_split[1]:
                item['n_coins'] += 1
    if act_split[0] == "decrease":
        for item in game_data.get('players'):
            if item.get('user_name', '') == act_split[1]:
                print('dec steve')
                item['n_coins'] -= 1
    if act_split[0] == "reveal":
        for player in game_data.get('players', []):
            if player['user_name'] == user_name:
                for card in player.get('cards', []):
                    if str(card['id']) == act_split[1]:
                        card['hidden'] = False
    if act_split[0] == "hide":
        for player in game_data.get('players', []):
            if player['user_name'] == user_name:
                for card in player.get('cards', []):
                    if str(card['id']) == act_split[1]:
                        card['hidden'] = True
    if act_split[0] == "grave":
        for player in game_data.get('players', []):
            if player['user_name'] == user_name:
                hand = []
                for card in player.get('cards', []):
                    if str(card['id']) == act_split[1]:
                        game_data['graveyard'].append(card)
                    else:
                        hand.append(card)
                player['cards'] = hand
    if act_split[0] == "deck":
        for player in game_data.get('players', []):
            if player['user_name'] == user_name:
                hand = []
                for card in player.get('cards', []):
                    if str(card['id']) == act_split[1]:
                        game_data['deck'].append(card)
                    else:
                        hand.append(card)
                player['cards'] = hand
    if act_split[0] == 'claim':
        # idx = random.randint(0,len(state['deck']))
        # card = state['deck'].pop(idx)
        if len(game_data['deck']) > 0:
            random.shuffle(game_data['deck'])
            card = game_data['deck'].pop()
            card['hidden'] = True
            for player in game_data.get('players', []):
                if player['user_name'] == user_name:
                    player['cards'].append(card)
    if act_split[0] == 'reset':
        #with open(db_prefix+'state_base.json', "r") as statef:
        #    state = json.load(statef)
        #for item in range(int(act_split[1])):
        #    game_data['players'].append(dict(user_name = "player" + str(item+1), n_coins = 2, cards = []))
        room["game_data"] = room["game_init"]
        room["game_init"] = copy.deepcopy(room["game_init"])
    if act_split[0] == 'takeincome':
        is_ajax = True
        game_data = room["game_data"]
        for player in game_data.get("players", []):
            if player.get('user_name', '') == user_name:
                player['n_coins'] += 1
                game_data['turn'] += 1
                if game_data['turn'] >= len(game_data["players"]):
                    game_data['turn'] = 0
    if act_split[0] == 'takeforeignaid':
        is_ajax = True
        game_data = room["game_data"]
        for player in game_data.get("players", []):
            if player.get('user_name', '') == user_name:
                game_data['turn'] += 1
                if game_data['turn'] >= len(game_data["players"]):
                    game_data['turn'] = 0
                game_data['block_state'] = dict()
                game_data['block_state'] = copy.deepcopy(game_data)
                player['n_coins'] += 2
    if act_split[0] == 'block':
        is_ajax = True
        if request.values['desired_block'] == game_data["activity_log"][-1]:
            activity_log = copy.deepcopy(game_data["activity_log"])
            bs = copy.deepcopy(game_data)
            game_data = copy.deepcopy(game_data['block_state'])
            game_data["activity_log"] = activity_log
            game_data["block_state"] = bs
            def is_duke(player_name):
                for item in game_data["players"]:
                    if item["user_name"] == player_name:
                        for card in item["cards"]:
                            if card["name"] == "Duke":
                                return True
                return False
            if ("foreignaid" in game_data["activity_log"][0] and is_duke(user_name)):
                game_data["claim_legit"] = True
                game_data["claim_maker"] = user_name
            else:
                game_data["claim_legit"] = False
                game_data["claim_maker"] = user_name
            room["game_data"] = game_data
    if act_split[0] == 'challenge':
        is_ajax = True
        if request.values['desired_challenge'] == game_data["activity_log"][-1]:
            if game_data["claim_legit"] == False:
                claim_maker = game_data["claim_maker"]
                activity_log = copy.deepcopy(game_data["activity_log"])
                game_data = copy.deepcopy(game_data['block_state'])
                game_data["activity_log"] = activity_log
                game_data["penalize"] = claim_maker
                room["game_data"] = game_data
            else:
                game_data["penalize"] = user_name
    if act_split[0] == "discard":
        is_ajax = True
        for player in game_data.get('players', []):
            if player['user_name'] == user_name:
                hand = []
                for i, card in enumerate(player.get('cards', [])):
                    if str(i) == act_split[1]:
                        game_data['graveyard'].append(card)
                    else:
                        hand.append(card)
                player['cards'] = hand
                game_data["penalize"] = ''




    game_data['activity_log'].append(f"{user_name} did {action_string}")
    with open(db_prefix+'state.json', "w") as statef:
        json.dump(state, statef)
    if is_ajax:
        # TODO sanitize state so we arent sending private hand info and deck info out to all players
        return jsonify(dict(game_data=game_data))
    else:
        return redirect(url_for('play_page', user_name=user_name, room_name=room_name))

@app.route('/play_page/<user_name>/<room_name>')
def play_page(user_name, room_name):
    n_coins = 0
    players = []
    with open(db_prefix+'state.json') as statef:
        state = json.load(statef)
    game_data = state.get('rooms', dict()).get(room_name, dict()).get('game_data', dict())
    players = game_data.get('players', [])
    graveyard = game_data.get('graveyard', [])
    deck = game_data.get('deck', [])
    deck_size = len(deck)
    activity_log = game_data.get('activity_log', [])
    return render_template("play_page.html", players=players, graveyard=graveyard, deck_size = deck_size, user_name=user_name, activity_log=activity_log, room_name=room_name)

@app.route('/play_page2/<user_name>/<room_name>')
def play_page2(user_name, room_name):
    n_coins = 0
    players = []
    with open(db_prefix+'state.json') as statef:
        state = json.load(statef)
    game_data = state.get('rooms', dict()).get(room_name, dict()).get('game_data', dict())
    turn = game_data.get('turn')
    players = game_data.get('players', [])
    whose_turn = ''
    for i, item in enumerate(players):
        if i == turn:
            whose_turn = item.get('user_name', '')
    graveyard = game_data.get('graveyard', [])
    deck = game_data.get('deck', [])
    deck_size = len(deck)
    penalize = game_data.get('penalize', '')
    activity_log = game_data.get('activity_log', [])
    return render_template("play_page2.html", players=players, graveyard=graveyard, deck_size = deck_size, user_name=user_name, activity_log=activity_log, room_name=room_name, turn=turn, whose_turn=whose_turn, penalize=penalize)

@app.route('/join_page')
def join_page():
    with open(db_prefix+'state.json', "r") as statef:
        state = json.load(statef)
    public_rooms = []
    rooms = state.get('rooms', [])
    for item in rooms:
        print(rooms[item].get('is_private'))
        if len(rooms[item].get('is_private', "on")) == 0:
            public_rooms.append(item)
    return render_template("join_page.html", public_rooms=public_rooms)
@app.route('/create_page')
def create_page():
    game_names = ["Overthrown"]
    return render_template("create_page.html", game_names=game_names)
@app.route('/create', methods=["GET", "POST"])
def create():
    user_name = escape(request.form.get('user_name', ''))
    user_name = user_name.replace(' ', '')
    if len(user_name) == 0:
        # TODO improve - prevent collisions with db checking
        user_name = 'player'+str(uuid.uuid4().hex)[0:8]
    room_name = escape(request.form.get('room_name', ''))
    room_name = room_name.replace(' ', '')
    if len(room_name) == 0:
        # TODO improve - prevent collisions with db checking
        room_name = 'room'+str(uuid.uuid4().hex)[0:8]
    is_private = escape(request.form.get('is_private', ''))
    game_name = escape(request.form.get('game_name', ''))
    if game_name == "Overthrown":
        with open(db_prefix+'state_base.json', "r") as statef:
            game_data = json.load(statef)
        game_init = copy.deepcopy(game_data)
        players=game_data.get('players', [])
        players.append(dict(user_name = user_name, n_coins = 2, cards = []))
        game_data['players'] = players
        if len(game_data['deck']) > 0:
            random.shuffle(game_data['deck'])
            card = game_data['deck'].pop()
            card['hidden'] = True
            for player in game_data.get('players', []):
                if player['user_name'] == user_name:
                    player['cards'].append(card)
        if len(game_data['deck']) > 0:
            random.shuffle(game_data['deck'])
            card = game_data['deck'].pop()
            card['hidden'] = True
            for player in game_data.get('players', []):
                if player['user_name'] == user_name:
                    player['cards'].append(card)
    else:
        game_data = dict()
    if "turn" not in game_data:
        game_data["turn"] = 0
    room = dict(room_name = room_name,
                game_master = user_name,
                is_private = is_private,
                game_name = game_name,
                game_data = game_data,
                game_init = game_init)
    with open(db_prefix+'state.json', "r") as statef:
        state = json.load(statef)
    rooms = state.get('rooms', dict())
    rooms[room_name] = room # Note duplicate rooms get clobbered fix that TODO
    state['rooms'] = rooms
    with open(db_prefix+'state.json', "w") as statef:
        json.dump(state, statef)
    return redirect(url_for('play_page', user_name=user_name, room_name=room_name))
@app.route('/join', methods=["GET", "POST"])
def join():
    user_name = str(escape(request.values['user_name']))
    user_name = user_name.replace(' ', '')
    if len(user_name) == 0:
        # TODO improve - prevent collisions with db checking
        user_name = 'player'+str(uuid.uuid4().hex)[0:8]
    if 'private_join' in request.values:
        room_name = str(escape(request.values['private_room_name']))
    elif 'public_join' in request.values:
        room_name = str(escape(request.values['public_room_name']))
    else:
        room_name = str(escape(request.values['room_name']))
    with open(db_prefix+'state.json', "r") as statef:
        state = json.load(statef)
    room = state.get('rooms', dict(room_name=None)).get(room_name, None)
    if room is None:
        return "Room Not Found" # TODO
    game_data = room.get("game_data", dict())
    players = game_data.get('players', [])
    def user_exists():
        for item in game_data.get('players', []):
            if item['user_name'] == user_name:
                return True
        return False

    print('join')
    if not user_exists():
        print('join')
        players.append(dict(user_name = user_name, n_coins = 2, cards = []))
        game_data['players'] = players
        if len(game_data['deck']) > 0:
            random.shuffle(game_data['deck'])
            card = game_data['deck'].pop()
            card['hidden'] = True
            for player in game_data.get('players', []):
                if player['user_name'] == user_name:
                    player['cards'].append(card)
        if len(game_data['deck']) > 0:
            random.shuffle(game_data['deck'])
            card = game_data['deck'].pop()
            card['hidden'] = True
            for player in game_data.get('players', []):
                if player['user_name'] == user_name:
                    player['cards'].append(card)
    if "turn" not in game_data:
        game_data["turn"] = 0
    with open(db_prefix+'state.json', "w") as statef:
        print('c')
        json.dump(state, statef)
    return redirect(url_for('play_page', user_name=user_name, room_name=room_name))

def main():
    global db_prefix
    db_prefix = ''
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()


