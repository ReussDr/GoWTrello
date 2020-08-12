import configparser
import datetime
import pytz
import os
import sys
from trello import TrelloClient


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


def get_gow_board(client):
    for board in client.list_boards():
        if board.name == "Gems of War Tasks":
            return board
    return client.add_board("Gems of War Tasks")


def get_gow_list_todo(gow_board):
    for trello_list in gow_board.list_lists():
        if trello_list.name == "To Do":
            return trello_list
    return gow_board.add_list("To Do")


def get_cards_to_create(day_to_create):
    daily_due = day_to_create + datetime.timedelta(days=1)
    cards = {"Daily Delve": [day_to_create, daily_due],
             "Daily Honor": [day_to_create, daily_due],
             "Daily Adventure Board": [day_to_create, daily_due],
             "Daily Dungeon": [day_to_create, daily_due],
             "Daily PvP Battle": [day_to_create, daily_due],
             }
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


def main():
    config = load_config_properties()
    #for area in config:
    #    print("[", area, "]")
    #    for item in config[area]:
    #        print(" ", item, config[area][item])

    # Calculate the day, and retrieve a list of cards to add
    day = calculate_day()
    cards = get_cards_to_create(day)
    print_cards_list(cards)

    # Connect to Trello Client, and get gow board and list
    client = TrelloClient(api_key=config['Trello API Keys']['trello_api_key'],
                          api_secret=config['Trello API Keys']['trello_api_secret'])
    gow_board = get_gow_board(client)

    # Remove cards with expired due dates, and build a list of existing cards
    existing_cards = []
    for card in gow_board.all_cards():
        if card.due_date < datetime.datetime.now().astimezone():
            card.delete()
        else:
            existing_cards.append(card.name)
    #print(existing_cards)

    # Get GoW to do list
    todo_list = get_gow_list_todo(gow_board)
    #print(todo_list)

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


if __name__ == '__main__':
    sys.exit(main())
