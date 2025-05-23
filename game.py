import pygame
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import PIL for image handling
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # replace with your MySQL username
        password="",  # replace with your MySQL password
        database="users.db"
    )

# Register function
def register():
    username = entry_username.get()
    password = entry_password.get()
    
    if username and password:
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username and password:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        
        if result:
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()  # Close the login window
            main_menu()  # Call the main menu function
        else:
            messagebox.showerror("Error", "Invalid username or password.")
        
        cursor.close()
        conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

# Main menu function
def main_menu():
    menu_root = tk.Tk()
    menu_root.geometry("700x500")
    menu_root.title("Main Menu")
    
    # Center the window on the screen
    screen_width = menu_root.winfo_screenwidth()
    screen_height = menu_root.winfo_screenheight()
    x = (screen_width // 2) - (700 // 2)
    y = (screen_height // 2) - (500 // 2)
    menu_root.geometry(f"700x500+{x}+{y}")

    # Load background image
    background_image = Image.open("pics\\back1.png")  # Update with your image path
    background_image = background_image.resize((700, 500))
    bg_image = ImageTk.PhotoImage(background_image)

    # Create a label for the background image
    bg_label = tk.Label(menu_root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Title Label
    title_label = tk.Label(menu_root, text="Welcome to the Game!", bg='black', fg='#FFFFFF', font=("Arial", 30))
    title_label.pack(pady=20)

    # Start Game Button
    btn_start_game = tk.Button(menu_root, text="Start Game", font=("Arial", 20), bg="#FF3399", fg="#FFFFFF", command=start_game)
    btn_start_game.pack(pady=10)

    # Options Button
    btn_options = tk.Button(menu_root, text="Options", font=("Arial", 20), bg="#FF3399", fg="#FFFFFF", command=lambda: print("Options clicked"))  # Placeholder for options
    btn_options.pack(pady=10)

    # Exit Button
    btn_exit = tk.Button(menu_root, text="Exit", font=("Arial", 20), bg="#FF3399", fg="#FFFFFF", command=menu_root.quit)
    btn_exit.pack(pady=10)

    menu_root.mainloop()

# Function to start the game
def start_game():
    pygame.init()

    win = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Naruto vs Sasuke")

    walkRight = [pygame.image.load('pics\\NR2.png'), pygame.image.load('pics\\NR3.png'), pygame.image.load('pics\\NR1.png')]
    walkLeft = [pygame.image.load('pics\\NL2.png'), pygame.image.load('pics\\NL3.png'), pygame.image.load('pics\\NL1.png')]

    bg = pygame.image.load('pics\\bg.png')
    stan = pygame.image.load('pics\\Nstanding.png')

    Nh = pygame.image.load('pics\\Nh.png')
    Sh = pygame.image.load('pics\\Sh.png')

    hitSound = pygame.mixer.Sound('pics\\hit.wav')

    Clock = pygame.time.Clock()

    class Player():
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.speed = 10
            self.isjump = False
            self.jumpheight = 10
            self.right = False
            self.left = False
            self.walkCount = 0
            self.standing = True
            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
            self.health = 200
            self.score = 0  # Initialize score

        def draw(self, win):
            if self.health > 0:
                if self.walkCount + 1 > 6:
                    self.walkCount = 0

                if not self.standing:
                    if self.left:
                        win.blit(walkLeft[self.walkCount // 2], (self.x, self.y))
                        self.walkCount += 1
                    elif self.right:
                        win.blit(walkRight[self.walkCount // 2], (self.x, self.y))
                        self.walkCount += 1
                else:
                    if self.right:
                        win.blit(pygame.image.load('pics\\NR1.png'), (self.x, self.y))
                    else:
                        win.blit(pygame.image.load('pics\\NL1.png'), (self.x, self.y))

                self.hitbox = (self.x + 10, self.y + 5, 80, 80)
                Nbar2 = pygame.draw.rect(win, (255, 0, 0), (80, 40, 210, 25))
                Nbar = pygame.draw.rect(win, (255, 255, 0), (80, 45, self.health, 15))

                # Display score
                score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
                win.blit(score_text, (300, 60))

            else:
                # Display Game Over message
                text = font.render('Game Over: Sasuke Wins', True, (0, 0, 0), (255, 100, 10))
                win.blit(text, (180, 200))
                win.blit(pygame.image.load('pics\\Nd.png'), (self.x, self.y))

        def hit(self):
            if self.health > 0:
                self.health -= 5
            else:
                print("Naruto died")

    class Weapons():
        def __init__(self, x, y, width, height, facing):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.facing = facing
            self.vel = 8 * facing
            self.hitbox = (self.x, self.y, 40, 40)

        def draw(self, win):
            win.blit(pygame.image.load('pics\\shur.png'), (self.x, self.y))
            self.hitbox = (self.x, self.y, 40, 40)

    class Enemy():
        walkRightS = [pygame.image.load('pics\\SR2.png'), pygame.image.load('pics\\SR3.png'), pygame.image.load('pics\\SR1.png')]
        walkLeftS = [pygame.image.load('pics\\SL2.png'), pygame.image.load('pics\\SL3.png'), pygame.image.load('pics\\SL1.png')]

        def __init__(self, x, y, width, height, end):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.end = end
            self.path = [self.x, self.end]
            self.speed = 8
            self.walkCount = 0
            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
            self.health = 200
            self.score = 0

        def draw(self, win):
            self.move()

            if self.health > 0:
                if self.walkCount + 1 >= 6:
                    self.walkCount = 0

                if self.speed > 0:
                    win.blit(self.walkRightS[self.walkCount // 2], (self.x, self.y))
                    self.walkCount += 1
                else:
                    win.blit(self.walkLeftS[self.walkCount // 2], (self.x, self.y))
                    self.walkCount += 1

                self.hitbox = (self.x + 10, self.y + 5, 80, 80)
                Sbar2 = pygame.draw.rect(win, (255, 0, 0), (390, 35, 210, 25))
                Sbar = pygame.draw.rect(win, (255, 255, 0), (400, 40, self.health, 15))

            else:
                self.speed = 0
                # Display Game Over message
                text = font.render('Game Over: Naruto Wins', True, (0, 0, 0), (255, 255, 255))
                win.blit(text, (180, 200))
                win.blit(pygame.image.load('pics\\Sd.png'), (self.x, self.y))

        def move(self):
            if self.speed > 0:
                if self.x + self.speed < self.end:
                    self.x += self.speed
                else:
                    self.speed = self.speed * -1
                    self.walkCount = 0
            else:
                if self.x - self.speed > self.path[0]:
                    self.x += self.speed
                else:
                    self.speed = self.speed * -1
                    self.walkCount = 0

        def hit(self):
            if self.health > 0:
                self.health -= 10
            else:
                print("Sasuke died")

    run = True
    game_over = False  # Track game over state

    def redraw_game_window():
        win.blit(bg, (0, 0))
        naruto.draw(win)
        sasuke.draw(win)
        win.blit(Nh, (10, 10))
        win.blit(Sh, (600, 10))

        for shuriken in shurikens:
            shuriken.draw(win)

        if game_over:
            # Display Game Over message
            game_over_text = font.render('Game Over', True, (0, 0, 0))
            win.blit(game_over_text, (250, 150))


        pygame.display.update()

    font = pygame.font.SysFont('comicsans', 30, True)
    naruto = Player(30, 400, 100, 100)
    sasuke = Enemy(100, 400, 100, 100, 600)
    shurikens = []
    throwSpeed = 0

    while run:
        Clock.tick(25)

        if throwSpeed > 0:
            throwSpeed += 1

        if throwSpeed > 3:
            throwSpeed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not game_over:
            if naruto.health > 0 and sasuke.health > 0:
                if naruto.hitbox[1] < sasuke.hitbox[1] + sasuke.hitbox[3] and naruto.hitbox[1] + naruto.hitbox[3] > sasuke.hitbox[1]:
                    if naruto.hitbox[0] + naruto.hitbox[2] > sasuke.hitbox[0] and naruto.hitbox[0] < sasuke.hitbox[0] + sasuke.hitbox[2]:
                        naruto.hit()
                        hitSound.play()

            else:
                if naruto.health == 0:
                    game_over = True  # Set game over state

            for shuriken in shurikens:
                if sasuke.health > 0:
                    if shuriken.hitbox[1] + round(shuriken.hitbox[3] / 2) > sasuke.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3] / 2) < sasuke.hitbox[1] + sasuke.hitbox[3]:
                        if shuriken.hitbox[0] + shuriken.hitbox[2] > sasuke.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < sasuke.hitbox[0] + sasuke.hitbox[2]:
                            sasuke.hit()
                            naruto.score += 1  # Increment score when Sasuke is hit
                            hitSound.play()
                            shurikens.pop(shurikens.index(shuriken))
                    else:
                        sasuke.speed = 0

                if shuriken.x < 699 and shuriken.x > 0:
                    shuriken.x += shuriken.vel
                else:
                    shurikens.pop(shurikens.index(shuriken))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and throwSpeed == 0:
                if naruto.left:
                    facing = -1
                else:
                    facing = 1

                if len(shurikens) < 5:
                    shurikens.append(Weapons(round(naruto.x + 60), round(naruto.y + 30), 40, 40, facing))
                    throwSpeed = 1

            if keys[pygame.K_LEFT] and naruto.x > naruto.speed:
                naruto.x -= naruto.speed
                naruto.left = True
                naruto.right = False
                naruto.standing = False
            elif keys[pygame.K_RIGHT] and naruto.x < 690 - naruto.width - naruto.speed:
                naruto.x += naruto.speed
                naruto.left = False
                naruto.right = True
                naruto.standing = False
            else:
                naruto.standing = True
                naruto.walkCount = 0

            if not naruto.isjump:
                if keys[pygame.K_UP]:
                    naruto.isjump = True
                    naruto.left = False
                    naruto.right = False
                    naruto.walkCount = 0
            else:
                if naruto.jumpheight >= -10:
                    neg = 1
                    if naruto.jumpheight < 0:
                        neg = -1
                    naruto.y -= (naruto.jumpheight ** 2) * 0.5 * neg
                    naruto.jumpheight -= 1
                else:
                    naruto.isjump = False
                    naruto.jumpheight = 10

        else:
            # Check for restart key
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                restart_game()  # Restart the game

        redraw_game_window()

    pygame.quit()

def restart_game():
    global naruto, sasuke, game_over
    naruto = Player(30, 400, 100, 100)
    sasuke = Enemy(100, 400, 100, 100, 600)
    naruto.health = 200
    sasuke.health = 200
    naruto.score = 0
    game_over = False

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("700x500")

root.configure(bg='#333333')

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (700 // 2)
y = (screen_height // 2) - (500 // 2)
root.geometry(f"700x500+{x}+{y}")

# Create a frame to hold the login elements
frame = tk.Frame(root, bg='#333333')
frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame in the window

# Create and place the labels and entries
tk.Label(frame, text="Username", bg='#333333', fg='#FFFFFF', font=("Arial", 20)).grid(row=0, column=0, padx=10, pady=10)  # Centered
entry_username = tk.Entry(frame, font=("Arial", 16))
entry_username.grid(row=0, column=1, padx=10, pady=10)  # Centered

tk.Label(frame, text="Password", bg='#333333', fg='#FFFFFF', font=("Arial", 20)).grid(row=1, column=0, padx=10, pady=10)  # Centered
entry_password = tk.Entry(frame, show="*", font=("Arial", 16))
entry_password.grid(row=1, column=1, padx=10, pady=10)  # Centered

# Create and place the buttons
btn_login = tk.Button(frame, text="Login", font=("Arial", 20), bg="#FF3399", fg="#FFFFFF", command=login)
btn_login.grid(row=2, column=0, padx=10, pady=10)  # Centered

btn_register = tk.Button(frame, text="Register", font=("Arial", 20), bg="#FF3399", fg="#FFFFFF", command=register)
btn_register.grid(row=2, column=1, padx=10, pady=10)  # Centered

# Run the application
root.mainloop()
