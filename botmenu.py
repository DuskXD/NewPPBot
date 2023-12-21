class BotMenu:
    def __init__(self):
        self.menu_stack = []

    def show_menu(self, menu_items):
        # Отображение меню с переданными пунктами
        pass

    def handle_button_click(self, button):
        if button == "назад":
            if len(self.menu_stack) > 0:
                previous_menu = self.menu_stack.pop()
                self.show_menu(previous_menu)
        else:
            # Обработка нажатия других кнопок и отображение нового меню
            new_menu = self.get_menu_for_button(button)
            self.menu_stack.append(new_menu)
            self.show_menu(new_menu)

    def get_menu_for_button(self, button):
        # Возвращает меню для выбранной кнопки
        pass