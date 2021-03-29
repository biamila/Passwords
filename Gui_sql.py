import pygame, sqlite3


class Input_text:
    def __init__(self, x, y, w, h):
        self.name = pygame.Rect(x, y, w, h)
        self.active = False
        self.text = ""
        self.colour = (225, 225, 225)

    def check_collision(self, event):
        if self.name.collidepoint(event.pos[0], event.pos[1]):
            self.active = not self.active
        else:
            self.active = False

        if self.active:
            self.colour = (0, 0, 255)
        else:
            self.colour = (255, 255, 255)

    def writting(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def printscreen(self, new_screen, font):
        surface = font.render(self.text, True, (0, 0, 0))
        new_screen.blit(surface, (self.name.x + 5, self.name.y + 5))
        pygame.draw.rect(new_screen, self.colour, self.name, 2)

    def boxfilled(self):
        if self.text != "":
            return True
        else:
            return False

    def get_values(self):
        return self.text

def gui_inputs(*args):
    answers = []
    new_screen = pygame.display.set_mode((400, 300))
    font = pygame.font.Font(None, 28)

    length = len(args)
    first_input = Input_text(60, 60, 140, 35)
    second_input = Input_text(60, 135, 140, 35)
    if length == 3:
        third_input = Input_text(60, 210, 140, 35)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                if mousex >= 310 and mousex <= 310 + 80 and mousey >= 265 and mousey <= 265 + 30:
                    return answers

                if mousex >= 310 and mousex <=310+80 and mousey >= 225 and mousey <= 225+30:
                    if first_input.boxfilled() and second_input.boxfilled():
                        if length == 3 and third_input.boxfilled():
                            answers.append(first_input.get_values())
                            answers.append(second_input.get_values())
                            answers.append(third_input.get_values())
                            return answers

                        elif length == 2:
                            answers.append(first_input.get_values())
                            answers.append(second_input.get_values())
                            return answers

                first_input.check_collision(event)
                second_input.check_collision(event)
                if length == 3:
                    third_input.check_collision(event)

            if event.type == pygame.KEYDOWN:
                first_input.writting(event)
                second_input.writting(event)
                if length == 3:
                    third_input.writting(event)

        new_screen.fill((135, 206, 235))
        first_input.printscreen(new_screen, font)
        second_input.printscreen(new_screen, font)
        if length == 3:
            third_input.printscreen(new_screen, font)

        pygame.time.Clock().tick(30)

        pygame.draw.rect(new_screen, (95, 166, 195), (310, 265, 80, 30))
        new_screen.blit(font.render("Back", True, (0, 0, 0)), (325, 270))

        pygame.draw.rect(new_screen, (95, 166, 195), (310, 225, 80, 30))
        new_screen.blit(font.render("Done", True, (0, 0, 0)), (325, 230))

        new_screen.blit(font.render(args[0], True, (0, 0, 0)), (50, 40))
        new_screen.blit(font.render(args[1], True, (0, 0, 0)), (50, 115))
        if length == 3:
            new_screen.blit(font.render(args[2], True, (0, 0, 0)), (50, 190))

        pygame.display.update()

def error_message(text, login=False):
    pop_screen = pygame.display.set_mode((400, 100))
    font = pygame.font.Font(None, 28)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if login:
            pop_screen.fill((195, 225, 225))
            pop_screen.blit(font.render(text, True, (46, 109, 225)), (30, 10))
            pop_screen.blit(font.render("Have a nice day :)", True, (112, 155, 225)), (120, 50))
        else:
            pop_screen.fill((50, 50, 50))
            pop_screen.blit(font.render(text, True, (225, 225, 225)), (10, 10))
        pygame.display.update()


def add_new():
    done = False
    while not done:
        answers = gui_inputs("Name", "User", "Password")
        print(answers)
        if answers != []:
            name = answers[0]
            user = answers[1]
            password = answers[2]
            c.execute("""SELECT * FROM Passwords
                        WHERE user = ?""", (user,))
            results = c.fetchall()
            if len(results) == 0:
                c.execute("""INSERT INTO Passwords VALUES(?, ?, ?)""", (user, name, password,))
                print("item added")
                break
            else:
                print("username used")
                error_message("Sorry this username is taken")
        else:
            break
    db.commit()

def update():
    password = ""
    checkpasssword = " "
    while password != checkpasssword:
        answers = gui_inputs("User", "Password", "Password Again")
        if answers != []:
            print(answers)
            user = answers[0]
            password = answers[1]
            checkpasssword = answers[2]
            if password != checkpasssword:
                error_message("Sorry, password incorrectly typed")
            else:
                c.execute("""UPDATE Passwords
                        SET password = ?
                        WHERE user = ? """, (password, user,))
                db.commit()
        else:
            break


def delete():
    done = False
    while not done:
        answers = gui_inputs("User", "Password")
        if answers != []:
            user = answers[0]
            password = answers[1]
            try:
                c.execute("""DELETE FROM Passwords WHERE user = ? and password = ?""", (user, password,))
                db.commit()
                done = True
            except:
                error_message("No account found with such details")
        else:
            done = True

def log_in():
    done = False
    while not done:
        answers = gui_inputs("User", "Password")
        if answers != []:
            user = answers[0]
            password = answers[1]
            c.execute("""SELECT password from Passwords WHERE user = ?""", (user,))
            result = c.fetchone()
            try:
                for i in result:
                    if i == password:
                        error_message("You've have successfully logged in!", True)
                    else:
                        error_message("Log in has failed!")
            except:
                error_message("User not recognized")
        else:
            done = True


def button(screen, x, y, w, h, font, text, func):
    xpos, ypos = pygame.mouse.get_pos()
    light = (240, 248, 255)
    dark = (255, 0, 0)
    click = pygame.mouse.get_pressed()

    if xpos >= x and xpos <= x + w and ypos >= y and ypos <= y + h:
        pygame.draw.rect(screen, dark, (x, y, w, h))
        if click[0] == 1:
            func()
    else:
        pygame.draw.rect(screen, light, (x, y, w, h))
    screen.blit(font.render(text, True, (0, 0, 0)), (x + 10, y + 10))


def main_window():
    global c, db
    db = sqlite3.connect("passwords.db")
    c = db.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS Passwords
                (user text,
                name text, 
                password text)""")

    screen = pygame.display.set_mode((400, 300))
    font = pygame.font.SysFont('Arial', 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((135, 206, 235))

        screen.blit(font.render("What would you like to do", True, (0, 0, 0)), (100, 30))
        button(screen, 60, 70, 80, 70, font, "Register", add_new)
        button(screen, 160, 70, 80, 70, font, "Update", update)
        button(screen, 260, 70, 80, 70, font, "Delete", delete)
        button(screen, 160, 160, 80, 70, font, "Log in", log_in)
        pygame.display.update()

    db.close()


if __name__ == "__main__":
    pygame.init()
    main_window()
    pygame.quit()

