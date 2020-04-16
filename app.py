#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request, escape, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send, emit
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
socketio = SocketIO(app)
import json
import random
import copy
import uuid
import pymongo

db_prefix = '/var/www/TeddyPoCards/'
myclient = pymongo.MongoClient(app.config["MONGOSTRING"])
mydb = myclient["dev_db"]

@app.route('/mon')
def mongo():
    rooms = mydb["room"]
    rooms.drop()

    rc = RC(rooms)
    random.seed(0)
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    rc.create_room('sk', 'p1', True, 'Spanish Flu')
    rc.join_room('sk', 'p2')
    rc.join_room('sk', 'p3')
    rc.join_room('sk', 'p4')
    rc.modify_room('sk', 'started')
    action_params = dict()
    action_params["user_name"] = "p2"
    action_params["action"] = "income"
    rc.modify_room('sk', 'play_action', action_params) # fail cuz not his turn
    action_params = dict()
    action_params["user_name"] = "p3"
    action_params["action"] = "income"
    rc.modify_room('sk', 'play_action', action_params)
    action_params = dict()
    action_params["user_name"] = "p4"
    action_params["action"] = "foreign_aid"
    rc.modify_room('sk', 'play_action', action_params)
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="allow"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="allow"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="allow"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="foreign_aid"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="block")) # rightful duke doing a righteous block
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="allow"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="allow"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="allow"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="foreign_aid"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="block")) # another rightful duke doing a righteous challenge
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="challenge")) # p2 makes an erroneous challenge
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="reveal0")) # p1 prooves he is the duke
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="discard0")) # gotta pay for your erroneous challenge
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="foreign_aid"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="block")) # p1 blocks but is no longer the duke
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="challenge")) # p3 makes a correct accusation p1 will have to pay
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="reveal1")) # p1 has to grave something
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="stealp2"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="stealp4"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="stealp4"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="block"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="stealp4"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="stealp4"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="assassinatep4"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="discard0"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="income")) # this was added in late when a bug was fixed
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="exchange"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="doublediscard0_2"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="income"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="infectp1"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p1", action="discard0"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="income"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="tax"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p4", action="tax")) # lets test out what happens when you have 10 coins
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="steamp3")) # he must infect
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="tax")) # fails
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="income")) # fails
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="foreign_aid")) # fails
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="assassinatep4")) # fails
    rc.modify_room('sk', 'play_action', params=dict(user_name="p2", action="infectp3"))
    rc.modify_room('sk', 'play_action', params=dict(user_name="p3", action="discard0"))

    myquery = dict()
    for item in rooms.find(myquery):
        pp.pprint(item)


    #x = mycoll.insert_one(dict(user_name='steve'))
    #print(x.inserted_id)
    #myquery = dict(user_name='steve')
    #for item in mycoll.find(myquery):
    #    print(item)
    #print(myclient.list_database_names())
    # game is one mongodb document and if two people access something at the same time their browser is just told to try again and it does
    # mycoll.drop()
    return jsonify(dict(hi=1))

class RC:
    def __init__(self, rooms):
        self.rooms = rooms
    def create_room(self, room_name, game_master, is_private=False, game_name=''):
        if self.rooms.find({"room_name": room_name}).count() > 0:
            # If the room exists, join the room
            return self.join_room(room_name, game_master)
        game_params = dict()
        if game_name == 'Spanish Flu':
            game_params["approval_timer"] = "disabled"
            # game_params["approval_timer"] = "infinite"
            game_params["keep_grave_sorted"] = True
        return self.rooms.insert_one(dict(room_name=room_name,
            game_master=game_master,
            is_private=is_private,
            game_name=game_name,
            players=[game_master],
            game_state='waiting',
            game_data=dict(),
            game_params=game_params))
    def delete_room(self, room_name):
        query={"room_name": room_name}
        self.rooms.delete_many(query)
    def join_room(self, room_name, user_name):
        if self.rooms.find({"room_name": room_name}).count() == 0:
            room = self.create_room(room_name, user_name)
        room = self.rooms.find_one({"room_name": room_name})
        myquery={"room_name": room_name}
        players = []
        if "players" in room:
            players = room["players"]
        if user_name not in players:
            players.append(user_name)
            newvalues = {"$set": {"players": players}}
            self.rooms.update_one(myquery, newvalues)
        print(room)
        return room is not None
    def modify_room(self, room_name, action, params=dict()):
        changed = False
        query={"room_name": room_name}
        if action == 'waiting':
            query={"room_name": room_name}
            newvalues = {"$set": {"game_state": "waiting"}}
            self.rooms.update_one(query, newvalues)
            changed = True
        elif action == 'started':
            query={"room_name": room_name, "game_state": "waiting",
                    "game_name": "Spanish Flu"}
            room = self.rooms.find_one(query);
            if room is not None:
                newvalues = {"$set": {
                    "game_state": "started",
                    "game_data": RC.create_game(room)}
                }
                self.rooms.update_one(query, newvalues)
                changed=True
        elif action == 'play_action':
            query={"room_name": room_name, "game_state": "started",
                    "game_name": "Spanish Flu"}
            room = self.rooms.find_one(query);
            if room is not None:
                game_data = RC.action_game(room, params) 
                if game_data is not None:
                    newvalues = {"$set": {
                        "game_data": game_data}
                    }
                    self.rooms.update_one(query, newvalues)
                    changed = True
        return changed

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
        for item in ["Duke", "Contessa", "Assassin", "Ambassador", "Captain"]:
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
        action_log = [dict(user_name=room["game_master"], action="started")]
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
        coins = 0
        for item in room["game_data"]["players"]:
            if item["user_name"] == user_name:
                coins = item["coins"]

        # Check if action is allowed and expire appropriate waiting_for actions
        # TODO MORE ALLOWED VALIDATION IN HERE LIKE DOES THAT PERSON EXIST OR DO YOU HAVE THE CARDS TO DISCARD
        allowed = False
        for item in room["game_data"]["waiting_for"]:
            if action == "income" and item["kind"] == "turn" and item["user_name"] == user_name and coins < 10:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action == "foreign_aid" and item["kind"] == "turn" and item["user_name"] == user_name and coins < 10:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action == "tax" and item["kind"] == "turn" and item["user_name"] == user_name and coins < 10:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action.startswith("steal") and item["kind"] == "turn" and item["user_name"] == user_name and coins < 10:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action.startswith("assassinate") and item["kind"] == "turn" and item["user_name"] == user_name and coins < 10 and coins >= 3:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action == "exchange" and item["kind"] == "turn" and item["user_name"] == user_name and coins < 10:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action.startswith("doublediscard") and item["kind"] == "doublediscard" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action.startswith("infect") and item["kind"] == "turn" and item["user_name"] == user_name:
                if coins >= 7:
                    room["game_data"]["waiting_for"] = []
                    allowed=True
            elif action == "allow" and item["kind"] == "block" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"].remove(dict(kind="block", user_name=user_name))
                allowed = True
            elif action == "allow" and item["kind"] == "challenge" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"].remove(dict(kind="challenge", user_name=user_name))
                allowed = True
            elif action == "block" and item["kind"] == "block" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action == "challenge" and item["kind"] == "challenge" and item["user_name"] == user_name:
                room["game_data"]["waiting_for"] = []
                allowed = True
            elif action.startswith("reveal") and item["kind"] == "reveal" and item["user_name"] == user_name:
                reveal_index = int(action.replace("reveal", ""))
                for player in room["game_data"]["players"]:
                    if player["user_name"] == user_name:
                        if reveal_index >= len(player["cards"]):
                            allowed=False
                        else:
                            room["game_data"]["waiting_for"] = []
                            allowed = True
                        break
            elif action.startswith("discard") and item["kind"] == "discard" and item["user_name"] == user_name:
                discard_index = int(action.replace("discard", ""))
                for player in room["game_data"]["players"]:
                    if player["user_name"] == user_name:
                        if discard_index >= len(player["cards"]):
                            allowed=False
                        else:
                            room["game_data"]["waiting_for"] = []
                            allowed = True
                        break
        if not allowed:
            return None

        # Add the allowed action to the log
        room["game_data"]["action_log"].append(params)

        # Modify cards and coins with turn actions that cant be undone
        players = room["game_data"]["players"]
        for item in players:
            if action.startswith("assassinate") and item["user_name"] == user_name:
                item["coins"] -= 3

        # Backup the game state (for potential blocks)
        if action != "allow" and action != "challenge" and not action.startswith("reveal") and not action.startswith('discard') and not action.startswith('doublediscard'):
            # action and challenge dont change game state and shouldnt blow away valuable saved backup
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
            elif action == "tax" and item["user_name"] == user_name:
                item["coins"] += 3
            elif action == "exchange" and item["user_name"] == user_name:
                room["game_data"]["pre_exchange_cards"] = copy.deepcopy(item["cards"])
                deck = room["game_data"]["deck"]
                if len(deck) > 0:
                    random.shuffle(deck)
                    item["cards"].append(deck.pop())
                if len(deck) > 0:
                    random.shuffle(deck)
                    item["cards"].append(deck.pop())
            elif action.startswith('doublediscard') and item["user_name"] == user_name:
                tmp = action.replace("doublediscard", "")
                idxes = sorted(list(int(i) for i in tmp.split("_")))
                # do sorting then back to front for indexing issues
                room["game_data"]["deck"].append(item["cards"].pop(idxes[1]))
                room["game_data"]["deck"].append(item["cards"].pop(idxes[0]))
            elif action.startswith('infect') and item["user_name"] == user_name:
                item["coins"] -= 7
            elif action.startswith('discard') and item["user_name"] == user_name:
                discard_index = int(action.replace("discard", ""))
                for player in room["game_data"]["players"]:
                    if player["user_name"] == user_name:
                        card = player["cards"].pop(discard_index)
                        room["game_data"]["grave_yard"].append(card)
                        break
        for item in players:
            if action.replace("steal", "") == item["user_name"]:
                stolen = min(2, item["coins"])
                item["coins"] -= stolen
        for item in players:
            if action.startswith("steal") and item["user_name"] == user_name:
                item["coins"] += stolen

        if action == "block":
            room["game_data"]["players"] = temp_backup
        elif action.startswith("reveal"):
            # check legitimacy
            reveal_index = int(action.replace("reveal", ""))
            for item in reversed(room["game_data"]["action_log"]):
                if item["action"] in ["tax", "exchange", "block"] or item["action"].startswith("steal") or item["action"].startswith("assassinate"):
                    challenged_action = item["action"]
                    break
            for item in reversed(room["game_data"]["action_log"]):
                if item["action"] in ["foreign_aid", "exchange"] or item["action"].startswith("steal") or item["action"].startswith("assassinate"):
                    preblock_action = item["action"]
                    break
            for item in room["game_data"]["players"]:
                if user_name == item["user_name"]:
                    revealed_card = item["cards"].pop(reveal_index)
                    break
            if challenged_action == 'exchange':
                revealed_card = room["game_data"]["pre_exchange_cards"][reveal_index]
            claim_prooved = False
            if challenged_action == 'block':
                if preblock_action == 'foreign_aid':
                    if revealed_card == 'Duke':
                        claim_prooved = True
                elif preblock_action.startswith('steal'):
                    if revealed_card == 'Captain' or revealed_card == "Ambassador":
                        claim_prooved = True
                elif preblock_action.startswith('assassinate'):
                    if revealed_card == 'Contessa':
                        claim_prooved = True
            elif challenged_action == 'tax':
                if revealed_card == 'Duke':
                    claim_prooved = True
            elif challenged_action.startswith('steal'):
                if revealed_card == 'Captain':
                    claim_prooved = True
            elif challenged_action.startswith('assassinate'):
                if revealed_card == "Assassin":
                    claim_prooved = True
            elif challenged_action == 'exchange':
                if revealed_card == 'Ambassador':
                    claim_prooved = True
            if claim_prooved:
                # player that just did the reveal gets their card sent to the deck and they get a new one
                room["game_data"]["deck"].append(revealed_card)
                random.shuffle(room["game_data"]["deck"])
                for item in room["game_data"]["players"]:
                    if user_name == item["user_name"]:
                        if len(room["game_data"]["deck"]) > 0:
                            item["cards"].append(room["game_data"]["deck"].pop())
                # the challenger must be punished
                print('claim prooved - punish the challenger at the end of this function')
            else:
                # Restore game state to before the saved (challenged) action
                room["game_data"]["players"] = copy.deepcopy(room["game_data"]["prev_players"])
                # Punish the challenged player by graveyarding the card they just revealed
                for item in room["game_data"]["players"]:
                    if user_name == item["user_name"]:
                        # gotta redo the pop here because the deepcopy above will undo it
                        revealed_card = item["cards"].pop(reveal_index)
                        break
                room["game_data"]["grave_yard"].append(revealed_card)

        # Add next actions game can wait for
        if action == 'income':
            next_player = RC.get_next_player_name(room["game_data"], user_name)
            room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
        elif action == 'foreign_aid':
            if room["game_params"]["approval_timer"] == "disabled":
                next_player = RC.get_next_player_name(room["game_data"], user_name)
                room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='block', user_name=item["user_name"]))
        elif action == "tax" or action.startswith("steal"):
            if room["game_params"]["approval_timer"] == "disabled":
                next_player = RC.get_next_player_name(room["game_data"], user_name)
                room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='block', user_name=item["user_name"]))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='challenge', user_name=item["user_name"]))
        elif action == "allow" and len(room["game_data"]["waiting_for"]) == 0:
            for item in reversed(room["game_data"]["action_log"]):
                if item["action"] in ["income", "foreign_aid", "tax", "exchange"] or item["action"].startswith("steal") or item["action"].startswith("assassinate") or item["action"].startswith("infect"):
                    next_player = RC.get_next_player_name(room["game_data"], item["user_name"])
                    break
            room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
        elif action.startswith('assassinate'):
            room["game_data"]["waiting_for"].append(dict(kind='discard', user_name=action.replace("assassinate", "")))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='block', user_name=item["user_name"]))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='challenge', user_name=item["user_name"]))
        elif action == "exchange":
            room["game_data"]["waiting_for"].append(dict(kind='doublediscard', user_name=user_name))
        elif action.startswith("doublediscard"):
            if room["game_params"]["approval_timer"] == "disabled":
                next_player = RC.get_next_player_name(room["game_data"], user_name)
                room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='challenge', user_name=item["user_name"]))
        elif action.startswith('infect'):
            victim = action.replace('infect', '')
            room["game_data"]["waiting_for"].append(dict(kind='discard', user_name=victim))
        elif action == "block":
            if room["game_params"]["approval_timer"] == "disabled":
                for item in reversed(room["game_data"]["action_log"]):
                    if item["action"] in ["income", "foreign_aid", "tax", "exchange"] or item["action"].startswith("steal") or item["action"].startswith("assassinate") or item["action"].startswith("infect"):
                        next_player = RC.get_next_player_name(room["game_data"], item["user_name"])
                        break
                room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
            for item in room["game_data"]["players"]:
                if item["user_name"] != user_name:
                    room["game_data"]["waiting_for"].append(dict(kind='challenge', user_name=item["user_name"]))
        elif action == "challenge":
            for item in reversed(room["game_data"]["action_log"]):
                if item["action"] in ["income", "foreign_aid", "tax", "exchange", "block"] or item["action"].startswith("steal") or item["action"].startswith("assassinate") or item["action"].startswith("infect"):
                    challenged_user = item["user_name"]
                    break
            room["game_data"]["waiting_for"].append(dict(kind='reveal', user_name=challenged_user))
        elif action.startswith("reveal"):
            if claim_prooved:
                # next action must be challenger penalized
                for item in reversed(room["game_data"]["action_log"]):
                    if item["action"] == "challenge":
                        challenger = item["user_name"]
                        break
                room["game_data"]["waiting_for"].append(dict(kind='discard', user_name=challenger))
            else:
                # Challenge is over - the pretender was caught lets move the game along to the next turn
                for item in reversed(room["game_data"]["action_log"]):
                    if item["action"] in ["income", "foreign_aid", "tax", "exchange"] or item["action"].startswith("steal") or item["action"].startswith("assassinate") or item["action"].startswith("infect"):
                        next_player = RC.get_next_player_name(room["game_data"], item["user_name"])
                        break
                room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))
        elif action.startswith("discard"):
            # Challenge is over - the false accuser was punished lets move the game along
            for item in reversed(room["game_data"]["action_log"]):
                if item["action"] in ["income", "foreign_aid", "tax", "exchange"] or item["action"].startswith("steal") or item["action"].startswith("assassinate") or item["action"].startswith("infect"):
                    next_player = RC.get_next_player_name(room["game_data"], item["user_name"])
                    break
            room["game_data"]["waiting_for"].append(dict(kind='turn', user_name=next_player))


        return room["game_data"]

@socketio.on('load play page')
def load_play_page(json):
    print('rx msg '  + str(json))
    join_room(json['room_name']) # this is a socketio function that i happen to have a name collision with
    emit('update', get_game_state(json["user_name"], json["room_name"], to_jsonify=False))

@socketio.on('play action')
def play_action(json):
    print('rx msg '  + str(json))
    rooms = mydb["room"]
    rc = RC(rooms)

    print(json["action"])
    if "action" in json and json["action"] == "reset_game" and "room_name" in json:
        rc.modify_room(json["room_name"], 'waiting')
        rc.modify_room(json["room_name"], 'started')


    if "room_name" in json and "user_name"  in json and "action" in json:
        truth = rc.modify_room(json["room_name"], 'play_action', params=dict(user_name=json["user_name"], action=json["action"]))
        print (truth)
        emit('update', get_game_state(json["user_name"], json["room_name"], to_jsonify=False), room=json["room_name"])


@app.route('/get_game_state/<user_name>/<room_name>')
def get_game_state(user_name, room_name, to_jsonify=True):
    myclient = pymongo.MongoClient(app.config["MONGOSTRING"])
    mydb = myclient["dev_db"]
    rooms = mydb["room"]
    room = rooms.find_one({"room_name": room_name})
    game_data = room["game_data"]
    game_data["game_master"] = room["game_master"]
    #for item in game_data["players"]: # commend this out for now, we'd prefer to have cards totally hidden from web clients but i want the game to work first
    #    if item["user_name"] != user_name:
    #        for i, card in enumerate(item["cards"]):
    #            item["cards"][i] = "hidden"
    for i, item in enumerate(game_data["deck"]):
        game_data["deck"][i] = "hidden"
    if room["game_params"]["keep_grave_sorted"]:
        game_data["grave_yard"] = sorted(game_data["grave_yard"])
    del game_data["prev_players"]
    if to_jsonify:
        return jsonify(room["game_data"])
    else:
        return room["game_data"]

@app.route('/mongo_play_page/<user_name>/<room_name>')
def mongo_play_page(user_name, room_name):
    game_data = get_game_state(user_name, room_name, to_jsonify=False)
    kwargs = dict(user_name=user_name,
            room_name=room_name,
            game_master=game_data["game_master"],
            players=game_data["players"],
            activity_log=game_data["action_log"],
            waiting_for = game_data["waiting_for"],
            deck_size = len(game_data["deck"]),
            grave_yard = game_data["grave_yard"],
            alternate_js=True)
    return render_template('mongo_play_page.html', **kwargs)

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
    game_names = ["Spanish Flu"]
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
    #if game_name == "Spanish Flu":
    #    with open(db_prefix+'state_base.json', "r") as statef:
    #        game_data = json.load(statef)
    #    game_init = copy.deepcopy(game_data)
    #    players=game_data.get('players', [])
    #    players.append(dict(user_name = user_name, n_coins = 2, cards = []))
    #    game_data['players'] = players
    #    if len(game_data['deck']) > 0:
    #        random.shuffle(game_data['deck'])
    #        card = game_data['deck'].pop()
    #        card['hidden'] = True
    #        for player in game_data.get('players', []):
    #            if player['user_name'] == user_name:
    #                player['cards'].append(card)
    #    if len(game_data['deck']) > 0:
    #        random.shuffle(game_data['deck'])
    #        card = game_data['deck'].pop()
    #        card['hidden'] = True
    #        for player in game_data.get('players', []):
    #            if player['user_name'] == user_name:
    #                player['cards'].append(card)
    #else:
    #    game_data = dict()
    #if "turn" not in game_data:
    #    game_data["turn"] = 0
    #room = dict(room_name = room_name,
    #            game_master = user_name,
    #            is_private = is_private,
    #            game_name = game_name,
    #            game_data = game_data,
    #            game_init = game_init)
    #with open(db_prefix+'state.json', "r") as statef:
    #    state = json.load(statef)
    #rooms = state.get('rooms', dict())
    #rooms[room_name] = room # Note duplicate rooms get clobbered fix that TODO
    #state['rooms'] = rooms
    #with open(db_prefix+'state.json', "w") as statef:
    #    json.dump(state, statef)
    rooms = mydb["room"]
    rc = RC(rooms)
    room = rc.create_room(room_name, user_name, is_private, game_name)
    rc.modify_room(room_name, 'waiting')
    rc.modify_room(room_name, 'started')
    print(room)
    return redirect(url_for('mongo_play_page', user_name=user_name, room_name=room_name))
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

    rooms = mydb["room"]
    rc = RC(rooms)
    room = rc.join_room(room_name, user_name)
    print(room)

    #with open(db_prefix+'state.json', "r") as statef:
    #    state = json.load(statef)
    #room = state.get('rooms', dict(room_name=None)).get(room_name, None)
    if room == False:
        return "Room Not Found" # TODO
    #game_data = room.get("game_data", dict())
    #players = game_data.get('players', [])
    #def user_exists():
    #    for item in game_data.get('players', []):
    #        if item['user_name'] == user_name:
    #            return True
    #    return False

    #print('join')
    #if not user_exists():
    #    print('join')
    #    players.append(dict(user_name = user_name, n_coins = 2, cards = []))
    #    game_data['players'] = players
    #    if len(game_data['deck']) > 0:
    #        random.shuffle(game_data['deck'])
    #        card = game_data['deck'].pop()
    #        card['hidden'] = True
    #        for player in game_data.get('players', []):
    #            if player['user_name'] == user_name:
    #                player['cards'].append(card)
    #    if len(game_data['deck']) > 0:
    #        random.shuffle(game_data['deck'])
    #        card = game_data['deck'].pop()
    #        card['hidden'] = True
    #        for player in game_data.get('players', []):
    #            if player['user_name'] == user_name:
    #                player['cards'].append(card)
    #if "turn" not in game_data:
    #    game_data["turn"] = 0
    #with open(db_prefix+'state.json', "w") as statef:
    #    print('c')
    #    json.dump(state, statef)
    return redirect(url_for('mongo_play_page', user_name=user_name, room_name=room_name))

def main():
    global db_prefix
    db_prefix = ''
    # app.run(host='0.0.0.0', debug=True)
    socketio.run(app)

if __name__ == "__main__":
    main()


