import tkinter as tk
from tkinter import messagebox
import json
import random


class CategoriesAndCards:
    """
    create/delete/rename a category
    create/delete/rename/change probability of a card
    """

    # categories functions start

    def __init__(self, filename):
        self.filename = filename
        self.categories = self.load_categories()

    def load_categories(self):
        # Load categories and cards
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_categories(self):
        # Save changes

        with open(self.filename, 'w') as file:
            json.dump(self.categories, file)
            messagebox.showinfo("Saved")

    def add_category(self, category_name):
        # Add a new category of cards

        if category_name in self.categories:
            messagebox.showerror("Error", f"Category '{category_name}' already exists.")
            return
        else:
            self.categories[category_name] = {}
            messagebox.showinfo("Done", f"Category '{category_name}' is successfully added.")

    def delete_category(self, category_name):
        # Delete a category

        if category_name in self.categories:
            del self.categories[category_name]
            self.save_categories()
            messagebox.showinfo("Done", f"Category name '{category_name}' is successfully deleted.")
            return
        else:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")

    def rename_category(self, category_name, new_name):
        # Rename a category

        if category_name in self.categories:
            self.categories[new_name] = self.categories.pop(category_name)
            self.save_categories()
            messagebox.showinfo("Done", f"Category name '{category_name}' is successfully renamed.")
            return
        else:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")

    # categories functions end
    # cards start.

    def add_card(self, category_name, card_name, probability):
        # Add a card into a category

        if probability < 0 or probability > 100:
            messagebox.showerror("Error", f"Probability should be between 0 and 100")
            return
        elif category_name not in self.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return
        elif card_name in self.categories[category_name]:
            messagebox.showerror("Error", f"This '{card_name}' already exists.")
            return
        else:
            self.categories[category_name][card_name] = probability / 100
            self.save_categories()
            messagebox.showinfo("Done", f"Card '{card_name}' is successfully added.")

    def delete_card(self, category_name, card_name):
        # Delete a card
        if category_name not in self.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return
        elif card_name not in self.categories[category_name]:
            messagebox.showerror("Error", f"Card '{card_name}' does not exist.")
            return
        else:
            del self.categories[category_name][card_name]
            self.save_categories()
            messagebox.showinfo("Done", f"Card '{card_name}' is successfully deleted.")

    def change_probability(self, category_name, card_name, new_probability):

        # Change probability of a card

        if category_name not in self.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return
        elif card_name not in self.categories[category_name]:
            messagebox.showerror("Error", f"Card '{card_name}' does not exist.")
            return
        else:
            self.categories[category_name][card_name] = new_probability
            self.save_categories()
            messagebox.showinfo("Done", f"Probability to get '{card_name}' is successfully changed.")

    def rename_card(self, category_name, card_name, new_name):
        # Rename a card

        if category_name not in self.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return
        elif card_name not in self.categories[category_name]:
            messagebox.showerror("Error", f"Card '{card_name}' does not exist.")
            return
        else:
            self.categories[category_name][new_name] = self.categories.pop(category_name[card_name])
            messagebox.showinfo("Done", f"Card name '{card_name}' is successfully renamed.")

    def pull_card(self, category_name, n):
        # Pull card(s)

        if category_name not in self.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return
        else:
            choices_dict = self.categories[category_name]
            choice = random.choices(list(choices_dict.keys()), weights=list(choices_dict.values()), k=n)[0]
            return choice

class Profiles:
    """
    create/delete/copy/rename/switch Profile
    """


class GUI:
    """
    Interface
    """
