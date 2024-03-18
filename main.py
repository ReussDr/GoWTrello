import argparse
import configparser
import datetime
import json
import os
import shutil
import sys
import pytz
import wget
import trello
import gow_class
import gow_kingdom_stats
import gow_pet
import gow_traitstones
import gow_troop
import gow_weapon


def patched_fetch_json(self,
                       uri_path,
                       http_method='GET',
                       headers=None,
                       query_params=None,
                       post_args=None,
                       files=None):
    """ Fetch some JSON from Trello """

    # explicit values here to avoid mutable default values
    if headers is None:
        headers = {}
    if query_params is None:
        query_params = {}
    if post_args is None:
        post_args = {}

    # if files specified, we don't want any data
    data = None
    if files is None and post_args != {}:
        data = json.dumps(post_args)

    # set content type and accept headers to handle JSON
    if http_method in ("POST", "PUT", "DELETE") and not files:
        headers['Content-Type'] = 'application/json; charset=utf-8'

    headers['Accept'] = 'application/json'

    # construct the full URL without query parameters
    if uri_path[0] == '/':
        uri_path = uri_path[1:]
    url = 'https://api.trello.com/1/%s' % uri_path

    if self.oauth is None:
        query_params['key'] = self.api_key
        query_params['token'] = self.api_secret

    # perform the HTTP requests, if possible uses OAuth authentication
    response = self.http_service.request(http_method, url, params=query_params,
                                         headers=headers, data=data,
                                         auth=self.oauth, files=files,
                                         proxies=self.proxies)

    if response.status_code == 401:
        raise trello.Unauthorized("%s at %s" % (response.text, url), response)
    if response.status_code != 200:
        raise trello.ResourceUnavailable("%s at %s" % (response.text, url), response)

    return response.json()


def create_arg_parser():
    parser = argparse.ArgumentParser()

    # Arguments which are applicable for the whole script / top-level args
    parser.add_argument('--verbose', help='Common top-level parameter',
                        action='store_true', required=False)

    # Define Subparsers
    subparsers = parser.add_subparsers(help='Desired action to perform',
                                       dest='action', required=True)

    # Usual subparsers not using common options
    # parser_other = subparsers.add_parser("extra-action", help='Do something without db')

    # Create parent subparser. Note `add_help=False` and creation via `argparse.`
    parent_parser = argparse.ArgumentParser(add_help=False)
    #parent_parser.add_argument('-p', help='add db parameter', required=True)

    # Subparsers based on parent
    parser_create = subparsers.add_parser("tasks", parents=[parent_parser],
                                          help='Update Trello Tasks')
    # Note: Add additional create options here

    parser_update = subparsers.add_parser("inventory", parents=[parent_parser],
                                          help='Pull and process gowdb inventory file')
    parser_update.add_argument('-no_update', action='store_true',
                               help="Don't update the file from gowdb.com")


    # Note: Add additional update options here
    return parser


def load_config_properties():
    """
    Read trello connection properties from the config file or environment variables

    :return: Dictionary with trello connection parameters
    """
    # Read properties from trello_config.ini if it is available
    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'Trello API Keys' not in config:
        config['Trello API Keys'] = {}
    if 'Trello Board Settings' not in config:
        config['Trello Board Settings'] = {}

    # If Environment variables are set, they override the trello_config.json
    if os.environ.get('TRELLO_API_KEY') is not None:
        config['Trello API Keys']['trello_api_key'] = os.environ.get('TRELLO_API_KEY')
    if os.environ.get('TRELLO_API_SECRET') is not None:
        config['Trello API Keys']['trello_api_secret'] = os.environ.get('TRELLO_API_SECRET')
    if os.environ.get('TRELLO_BOARD_ID') is not None:
        config['Trello Board Settings']['trello_board_id'] = os.environ.get('TRELLO_BOARD_ID')

    return config


def get_gow_board(client, config):
    for board in client.list_boards():
        if board.name == config['Trello Board Settings']['trello_board_id']:
            return board
    return client.add_board(config['Trello Board Settings']['trello_board_id'])


def get_gow_list_todo(gow_board, config):
    for trello_list in gow_board.list_lists():
        if trello_list.name == config['Trello Board Settings']['trello_list_todo']:
            return trello_list
    return gow_board.add_list(config['Trello Board Settings']['trello_list_todo'])


def get_cards_to_create(day_to_create):
    daily_due = day_to_create + datetime.timedelta(days=1)
    cards = {"Daily Delve": [day_to_create, daily_due],
             "Daily Honor": [day_to_create, daily_due],
             "Daily Adventure Board": [day_to_create, daily_due],
             "Daily Dungeon": [day_to_create, daily_due],
             "Daily PvP Battle": [day_to_create, daily_due],
             "Daily Guild Wars Battle": [day_to_create, daily_due],
             "Daily Underspire": [day_to_create, daily_due],
             "Daily XBox GamePass Rewards": [day_to_create, daily_due],
             "Daily Microsoft Rewards Set": [day_to_create, daily_due],
             "Daily Mass Effect Missions": [day_to_create, daily_due],
             "Walk Dog #1": [day_to_create, daily_due],
             "Walk Dog #2": [day_to_create, daily_due],
             "Exercise": [day_to_create, daily_due],
             }
    if day_to_create.weekday() == 0:
        cards["Calculate Weekly Req"] = [day_to_create, daily_due]
    if day_to_create.weekday() == 1:
        cards["Faction Assault"] = [day_to_create, daily_due]
    if day_to_create.weekday() == 2:
        cards["Pet Rescue"] = [day_to_create, daily_due]
    if day_to_create.weekday() == 3:
        cards["Class Challenge"] = [day_to_create, daily_due]
        cards["Update Traitstone Inventory"] = [day_to_create, daily_due]
    if day_to_create.weekday() == 6:
        cards["Update Honor Circle"] = [day_to_create, daily_due]

    beginning_of_week = day_to_create - datetime.timedelta(days=day_to_create.weekday())
    weekly_due = beginning_of_week + datetime.timedelta(days=7)
    cards["Review XBox Sales"] = [beginning_of_week, weekly_due]
    cards["Epic Trial"] = [beginning_of_week, weekly_due]
    cards["Weekly PvP Tier 1"] = [beginning_of_week, weekly_due]
    cards["Weekly Campaign"] = [beginning_of_week, weekly_due]
    cards["Weekly World Event"] = [beginning_of_week, weekly_due]
    cards["Weekly Guild Donation"] = [beginning_of_week, weekly_due]
    cards["Weekly Seal Collection"] = [beginning_of_week, weekly_due]
    cards["Weekly Shop (Troop and Event Keys)"] = [beginning_of_week, weekly_due]
    cards["Weekly Crafting (Troops and Weapons)"] = [beginning_of_week, weekly_due]
    return cards


def print_cards_list(cards):
    for card in cards:
        print(card, cards[card])
        for date in cards[card]:
            print(date)


def calculate_day():
    now_time = datetime.datetime.now().astimezone()
    reset_today = datetime.datetime.combine(datetime.date.today(),
                                            datetime.time(7, 0, 0, 0),
                                            pytz.UTC)
    day_to_populate = datetime.date.today()
    # now_time -= datetime.timedelta(hours=20)
    if now_time <= reset_today:
        day_to_populate -= datetime.timedelta(days=1)
    return day_to_populate


def update_tasks(config):
    day = calculate_day()
    cards = get_cards_to_create(day)
    print_cards_list(cards)

    # Connect to Trello Client, and get gow board and list
    trello.TrelloClient.fetch_json = patched_fetch_json
    client = trello.TrelloClient(api_key=config['Trello API Keys']['trello_api_key'],
                                 token=config['Trello API Keys']['trello_token'])
    gow_board = get_gow_board(client, config)

    # Remove cards with expired due dates, and build a list of existing cards
    existing_cards = []
    for card in gow_board.all_cards():
        if card.due_date != "" and card.due_date < datetime.datetime.now().astimezone():
            card.delete()
        else:
            existing_cards.append(card.name)
    # print(existing_cards)

    # Get GoW to do list
    todo_list = get_gow_list_todo(gow_board, config)
    # print(todo_list)

    # Add new cards, if they aren't already in the list
    for card in cards:
        card_name = card + " [" + str(cards[card][0]) + "]"
        print(card_name)
        if card_name not in existing_cards:
            due_date = datetime.datetime.combine(cards[card][1],
                                                 datetime.time(7, 0, 0, 0),
                                                 pytz.UTC)
            print(due_date)
            todo_list.add_card(card + " [" + str(cards[card][0]) + "]",
                               due=due_date.isoformat())


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    print(args)

    config = load_config_properties()

    if args.action == "tasks":
        update_tasks(config)

    if args.action == "inventory":
        if not args.no_update:
            if os.path.exists('inventory.json'):
                shutil.copyfile('inventory.json', 'inventory.json_backup')
                os.remove('inventory.json')
            wget.download(config['GoWDB Settings']['json_inventory'], 'inventory.json', bar=None)
        with open("inventory.json", "r") as read_file:
            print("Converting JSON encoded data into Python dictionary")
            developer = json.load(read_file)

            print("Decoded JSON Data From File")
            ts = gow_traitstones.Traitstones()
            for stone in developer['traitstones']:
                if 'count' not in stone:
                    stone['count'] = 0
                ts.add_traitstone(stone['name'], stone['count'])
            ts.print_csv("traitstones.csv")

            pets = []
            for jsonpet in developer['pets']:
                pets.append(gow_pet.Pet.gen_pet_from_json(jsonpet))
            gow_pet.Pet.print_pet_csv("pets.csv", pets)

            troops = []
            for jsontroop in developer['troops']:
                troops.append(gow_troop.Troop.gen_troop_from_json(jsontroop))
            gow_troop.Troop.print_troop_csv("troops.csv", troops)

            classes = []
            for jsonclass in developer['classes']:
                classes.append(gow_class.Class.gen_class_from_json(jsonclass))
            gow_class.Class.print_class_csv("classes.csv", classes)

            weapons = []
            for jsonweapon in developer['weapons']:
                weapons.append(gow_weapon.Weapon.gen_weapon_from_json(jsonweapon))
            gow_weapon.Weapon.print_weapon_csv("weapons.csv", weapons)

            #TODO Max Levels based on pulled stats

            stats = gow_kingdom_stats.KingdomStats()
            for troop in troops:
                stats.add_troop(troop)
            for pet in pets:
                stats.add_pet(pet)
            for gw_class in classes:
                stats.add_class(gw_class)
            for weapon in weapons:
                stats.add_weapon(weapon)
            stats.add_missing_weapons()
            stats.add_missing_pets()
            stats.print_csv("kingdom_stats.csv")


if __name__ == '__main__':
    sys.exit(main())
