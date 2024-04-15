import json


class Data:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()
        self.main_menu = self.data['Main']  # For button Main_Menu and what to show at the start

        self.current_object = {}
        self.current_path = ['Main']  # For back function
        self.update_content()
    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            default_data = {'Main':{'name': 'Main Folder', 'type': 'folder', 'content': {}}}
            with open(self.filename, 'w') as file:
                json.dump(default_data, file)
            return default_data

    def save_data(self):
        # Save data

        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def create_folder(self, name):
        # Create folder
        if name not in self.current_object['content'] and self.current_object['type'] == 'folder':
            self.current_object['content'][name] = {
                                        'name': name,
                                        'type': 'folder',
                                        'content': {}
                                        }
            self.update_content()  # Update current object info and content
            self.save_data()

    def create_category(self, name):
        # Create category. In category you can not create folders, only cards.
        # Also in pool we show category and individual cards separately

        self.current_object['content'][name] = {
            'name': name,
            'type': 'category',
            'content': {}
        }
        self.update_content()  # Update window and content
        self.save_data()

    def create_card(self, name, chance, description):
        # Create category. In category you can not create folders, only cards.
        # Also in pool we show category and individual cards separately

        self.current_object[name] = {
            'name': name,
            'category': name if self.current_object['type'] == 'folder' else self.current_object['name'], # If created if folder category=name, if in category = category name
            'type': 'card',
            'chance': chance,
            'description': description
        }
        self.update_content()  # Update window and content
        self.save_data()

    def open_object(self, name):
        # Open folder

        self.current_path.append('content')
        self.current_path.append(name)
        self.update_content()  # Update window and content

    def back(self):
        # Back or up in hierarchy

        if len(self.current_path) >= 2:
            self.current_path = self.current_path[:-2]
            self.update_content()

    def update_content(self):
        current = self.data

        for step in self.current_path:
            current = current[step]
        self.current_object = current

    def delete_object(self, name):
        if name in self.current_object['content']:
            del self.current_object['content'][name]
            self.save_data()
            print(f"{name} deleted successfully.")
        else:
            print(f"{name} not found.")



    def display_data(self, data=None, indent=0):
        if data is None:
            data = self.data

        for key, value in data.items():
            if isinstance(value, dict):
                if key == 'content':
                    print("    " * indent + key, value.keys())
                else:
                    display_value = {
                        k: v for k, v in value.items() if k in ['name', 'type']
                    }
                    print("    " * indent + key, display_value)
                self.display_data(value, indent + 1)


test = Data('data.json')
test.create_folder('Food')
test.open_object('Food')
test.create_folder('Breakfast')
test.open_object('Breakfast')
test.create_category('Healthy')
test.open_object('Healthy')
test.create_card('Eggs','20%','Just boiled')
test.display_data()
test.back()
test.back()
test.delete_object('Breakfast')
test.display_data()