import tkinter as tk
from tkinter import messagebox
import json
import random

class Card_Game:
    def __init__(self, filename):
        self.filename = filename
        self.categories = self.load_categories()

    def load_categories(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def add_category:

    def delete_category:

    def rename_category:

# categories functions end
# cards start.

    def add_card:

    def delete_card:

    def change_card:

    def pull_card:
# вписать кол-во?

