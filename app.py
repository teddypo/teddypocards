#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request, escape
app = Flask(__name__)
import json
import random
import copy

db_prefix = '/var/www/TeddyPoCards/'

@app.route('/')
def hello():
    return render_template('landing_page.html')
    #return redirect(url_for('join_page'))

@app.route('/action/<user_name>/<action_string>/<room_name>')
def action(user_name, action_string, room_name):
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

    game_data['activity_log'].append(f"{user_name} did {action_string}")
    with open(db_prefix+'state.json', "w") as statef:
        json.dump(state, statef)
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

@app.route('/join_page')
def join_page():
    return render_template("join_page.html")
@app.route('/create_page')
def create_page():
    game_names = ["Overthrown"]
    return render_template("create_page.html", game_names=game_names)
@app.route('/create', methods=["GET", "POST"])
def create():
    user_name = escape(request.form.get('user_name', ''))
    room_name = escape(request.form.get('room_name', ''))
    is_private = escape(request.form.get('is_private', ''))
    game_name = escape(request.form.get('game_name', ''))
    if game_name == "Overthrown":
        with open(db_prefix+'state_base.json', "r") as statef:
            game_data = json.load(statef)
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
    room = dict(room_name = room_name,
                game_master = user_name,
                is_private = is_private,
                game_name = game_name,
                game_data = game_data,
                game_init = copy.deepcopy(game_data))
    with open(db_prefix+'state.json', "r") as statef:
        state = json.load(statef)
    rooms = state.get('rooms', dict())
    rooms[room_name] = room # Note duplicate rooms get clobbered fix that TODO
    state['rooms'] = rooms
    with open(db_prefix+'state.json', "w") as statef:
        json.dump(state, statef)
    return (state)
@app.route('/join', methods=["GET", "POST"])
def join():
    user_name = str(escape(request.values['user_name']))
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
        state["rooms"]["room_name"] = room
        print(state)
        with open(db_prefix+'state.json', "w") as statef:
            json.dump(state, statef)
    return redirect(url_for('play_page', user_name=user_name, room_name=room_name))

def main():
    global db_prefix
    db_prefix = ''
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()


