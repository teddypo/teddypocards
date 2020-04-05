#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)
import json
import random

@app.route('/')
def hello():
    return redirect(url_for('join_page'))

@app.route('/action/<user_name>/<action_string>')
def action(user_name, action_string):
    with open('/var/www/TeddyPoCards/state.json', "r") as statef:
        state = json.load(statef)
    state['activity_log'] = state.get('activity_log', [])
    act_split = action_string.split('_')
    print(act_split)
    if act_split[0] == "increase":
        for item in state.get('players', []):
            if item.get('user_name', '') == act_split[1]:
                item['n_coins'] += 1
    if act_split[0] == "decrease":
        for item in state.get('players'):
            if item.get('user_name', '') == act_split[1]:
                print('dec steve')
                item['n_coins'] -= 1
    if act_split[0] == "reveal":
        for player in state.get('players', []):
            if player['user_name'] == user_name:
                for card in player.get('cards', []):
                    if str(card['id']) == act_split[1]:
                        card['hidden'] = False
    if act_split[0] == "hide":
        for player in state.get('players', []):
            if player['user_name'] == user_name:
                for card in player.get('cards', []):
                    if str(card['id']) == act_split[1]:
                        card['hidden'] = True
    if act_split[0] == "grave":
        for player in state.get('players', []):
            if player['user_name'] == user_name:
                hand = []
                for card in player.get('cards', []):
                    if str(card['id']) == act_split[1]:
                        state['graveyard'].append(card)
                    else:
                        hand.append(card)
                player['cards'] = hand
    if act_split[0] == "deck":
        for player in state.get('players', []):
            if player['user_name'] == user_name:
                hand = []
                for card in player.get('cards', []):
                    if str(card['id']) == act_split[1]:
                        state['deck'].append(card)
                    else:
                        hand.append(card)
                player['cards'] = hand
    if act_split[0] == 'claim':
        # idx = random.randint(0,len(state['deck']))
        # card = state['deck'].pop(idx)
        if len(state['deck']) > 0:
            random.shuffle(state['deck'])
            card = state['deck'].pop()
            card['hidden'] = True
            for player in state.get('players', []):
                if player['user_name'] == user_name:
                    player['cards'].append(card)
    if act_split[0] == 'reset':
        with open('/var/www/TeddyPoCards/state_base.json', "r") as statef:
            state = json.load(statef)
        for item in range(int(act_split[1])):
            state['players'].append(dict(user_name = "player" + str(item+1), n_coins = 2, cards = []))

    print(state)
    state['activity_log'].append(f"{user_name} did {action_string}")
    print (state['players'])
    with open('/var/www/TeddyPoCards/state.json', "w") as statef:
        json.dump(state, statef)
    return redirect(url_for('play_page', user_name=user_name))

@app.route('/play_page/<user_name>')
def play_page(user_name):
    n_coins = 0
    players = []
    with open('/var/www/TeddyPoCards/state.json') as statef:
        state = json.load(statef)
    players = state.get('players', [])
    graveyard = state.get('graveyard', [])
    deck = state.get('deck', [])
    deck_size = len(deck)
    activity_log = state.get('activity_log', [])
    return render_template("play_page.html", players=players, graveyard=graveyard, deck_size = deck_size, user_name=user_name, activity_log=activity_log)

@app.route('/join_page')
def join_page():
    return render_template("join_page.html")
@app.route('/join', methods=["GET", "POST"])
def join():
    user_name = str(request.values['user_name'])
    with open('/var/www/TeddyPoCards/state.json', "r") as statef:
        state = json.load(statef)
    players = state.get('players', [])
    def user_exists():
        for item in state.get('players', []):
            if item['user_name'] == user_name:
                return True
        return False

    if not user_exists():
        players.append(dict(user_name = user_name, n_coins = 2, cards = []))
        state['players'] = players
        if len(state['deck']) > 0:
            random.shuffle(state['deck'])
            card = state['deck'].pop()
            card['hidden'] = True
            for player in state.get('players', []):
                if player['user_name'] == user_name:
                    player['cards'].append(card)
        if len(state['deck']) > 0:
            random.shuffle(state['deck'])
            card = state['deck'].pop()
            card['hidden'] = True
            for player in state.get('players', []):
                if player['user_name'] == user_name:
                    player['cards'].append(card)
        with open('/var/www/TeddyPoCards/state.json', "w") as statef:
            json.dump(state, statef)
    return redirect(url_for('play_page', user_name=user_name))


if __name__ == "__main__":
    app.run(host='0.0.0.0')


