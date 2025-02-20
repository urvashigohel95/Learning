import tkinter as tk
from tkinter import messagebox
import sqlite3
import pygame


conn = sqlite3.connect('users.db')

# Create a cursor
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL)''')

conn.commit()

# Function to register a new user
def register():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "" or password == "":
        messagebox.showwarning("Warning", "Please fill in all fields")
        return
    
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        messagebox.showwarning("Warning", "Username already exists")
    else:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        display_users()  # Call to display users after registration

# Function to login a user
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if c.fetchone():
        messagebox.showinfo("Success", "Login successful")
    else:
        messagebox.showwarning("Warning", "Invalid username or password")

# Function to display all users
def display_users():
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    if users:
        user_list = "\n".join([f"ID: {user[0]}, Username: {user[1]}" for user in users])
        messagebox.showinfo("Registered Users", user_list)
    else:
        messagebox.showinfo("Registered Users", "No users found")

# Create the main window
root = tk.Tk()
root.title("Login System")

# Create and place the labels and entries
label_username = tk.Label(root, text="Username")
label_username.pack(pady=5)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Password")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show='*')
entry_password.pack(pady=5)

# Create and place the buttons
button_login = tk.Button(root, text="Login", command=login)
button_login.pack(pady=5)

button_register = tk.Button(root, text="Register", command=register)
button_register.pack(pady=5)

# Run the application
root.mainloop()

# Close the connection when the application is closed
conn.close()



pygame.init()

win=pygame.display.set_mode((700,500))
pygame.display.set_caption("Naruto vs Sasuke")

walkRight=[pygame.image.load('pics\\NR2.png'),pygame.image.load('pics\\NR3.png'),pygame.image.load('pics\\NR1.png')]
walkLeft=[pygame.image.load('pics\\NL2.png'),pygame.image.load('pics\\NL3.png'),pygame.image.load('pics\\NL1.png')]

bg=pygame.image.load('pics\\bg.png')
stan=pygame.image.load('pics\\Nstanding.png')

Nh=pygame.image.load('pics\\Nh.png')
Sh=pygame.image.load('pics\\Sh.png')

hitSound=pygame.mixer.Sound('pics\\hit.wav')




Clock=pygame.time.Clock()

class player():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.speed=10
        self.isjump=False
        self.jumpheight=10
        self.right=False
        self.left=False
        self.walkCount=0
        self.standing=True
        self.hitbox=(self.x +10,self.y +5,80,80)
        self.health=200



    def draw(self,win):
        
        if self.health >0:

        
           if self.walkCount +1 >6:
              self.walkCount=0


           if not(self.standing):
   

              if self.left:
                 win.blit(walkLeft[self.walkCount//2],(self.x,self.y))
                 self.walkCount +=1

              elif self.right:
                   win.blit(walkRight[self.walkCount//2],(self.x,self.y))
                   self.walkCount +=1

           else:
               if self.right:
                  win.blit(pygame.image.load('pics\\NR1.png'),(self.x,self.y))

               else:
                   win.blit(pygame.image.load('pics\\NL1.png'),(self.x,self.y))

           self.hitbox=(self.x +10,self.y +5,80,80)
           Nbar2 = pygame.draw.rect(win,(255,0,0),(80,40,210,25))
           Nbar = pygame.draw.rect(win,(255,255,0),(80,45,self.health,15))
                # pygame.draw.rect(win,(255,0,0),self.hitbox,2)


        else:
            text=font.render('Sasuke wins',True,(255,100,10),(0,0,100))
            win.blit(text,(180,200))
            win.blit(pygame.image.load('pics\\Nd.png'),(self.x,self.y))

    def hit(self):
        if self.health >0:
            self.health -=5
        else:
            print("Naruto died")
                 




class weapons():
    def __init__(self,x,y,width,height,facing):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.facing= facing
        self.vel=8*facing
        self.hitbox=(self.x,self.y,40,40)


    def draw(self,win):
        win.blit(pygame.image.load('pics\\shur.png'),(self.x,self.y))
        self.hitbox=(self.x,self.y,40,40)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)


                 



class enemy():
    walkRightS=[pygame.image.load('pics\\SR2.png'),pygame.image.load('pics\\SR3.png'),pygame.image.load('pics\\SR1.png')]
    walkLeftS=[pygame.image.load('pics\\SL2.png'),pygame.image.load('pics\\SL3.png'),pygame.image.load('pics\\SL1.png')]


    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.speed=8
        self.walkCount=0
        self.hitbox=(self.x +10,self.y +5,80,80)
        self.health=200



    def draw(self,win):
        self.move()

        if self.health >0:
            if self.walkCount +1 >=6:
               self.walkCount=0

            if self.speed >0:
               win.blit(self.walkRightS[self.walkCount//2],(self.x,self.y))
               self.walkCount +=1

            else:
               win.blit(self.walkLeftS[self.walkCount//2],(self.x,self.y))
               self.walkCount +=1
            
            self.hitbox=(self.x +10,self.y +5,80,80)
            Sbar2 = pygame.draw.rect(win,(255,0,0),(390,35,210,25))
            Sbar = pygame.draw.rect(win,(255,255,0),(400,40,self.health,15))

            
        else:
            self.speed = 0
            text=font.render('Naruto wins',True,(255,255,255),(0,0,100))
            win.blit(text,(180,200))
            win.blit(pygame.image.load('pics\\Sd.png'),(self.x,self.y))
       # pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
        
        
        
    def move(self):
        if self.speed >0:

            if self.x + self.speed < self.end:
                self.x += self.speed

            else:
                self.speed=self.speed * -1
                self.walkCount=0

        else:
            if self.x - self.speed > self.path[0]:
                self.x +=self.speed

            else:
                self.speed=self.speed * -1
                self.walkCount=0

        
    def hit(self):
        if self.health >0:
            self.health -=10

        else:
            print("Sasuke died")

    
run=True

def redrawgamewindow():
    
    win.blit(bg,(0,0))
    naruto.draw(win)
    sasuke.draw(win)
    win.blit(Nh,(10,10))
    win.blit(Sh,(600,10))         

    for shuriken in shurikens:
        shuriken.draw(win)




    
    pygame.display.update()


font=pygame.font.SysFont('comicsans',30,True)    
naruto=player(30,400,100,100)
sasuke=enemy(100,400,100,100,600)
shurikens=[]
throwSpeed=0


while run:

    Clock.tick(25)

    if throwSpeed >0:
        throwSpeed +=1

        
    if throwSpeed >3:
        throwSpeed=0
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    if naruto.health >0 and sasuke.health >0:
         if naruto.hitbox[1] < sasuke.hitbox[1] + sasuke.hitbox[3] and naruto.hitbox[1] + naruto.hitbox[3] > sasuke.hitbox[1]:
             if naruto.hitbox[0] + naruto.hitbox[2] > sasuke.hitbox[0] and naruto.hitbox[0] < sasuke.hitbox[0] + sasuke.hitbox[2]:
                 naruto.hit()
                 hitSound.play()

    else:
        if naruto.health ==0:
            naruto.speed=0


    for shuriken in shurikens:

        if sasuke.health >0:

           if shuriken.hitbox[1]+ round(shuriken.hitbox[3]/2) > sasuke.hitbox[1] and shuriken.hitbox[1]+ round(shuriken.hitbox[3]/2) < sasuke.hitbox[1] + sasuke.hitbox[3]:
               if shuriken.hitbox[0] + shuriken.hitbox[2] > sasuke.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < sasuke.hitbox[0]+ sasuke.hitbox[2]:
                  sasuke.hit()
                  hitSound.play()
                  shurikens.pop(shurikens.index(shuriken))

           else:
               sasuke.speed=0


        
        if shuriken.x <699 and shuriken.x>0:
            shuriken.x +=shuriken.vel

        else:
            shurikens.pop(shurikens.index(shuriken))
        


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and throwSpeed ==0:
        if naruto.left==True:
            facing=-1

        else:
            facing=1

        if len(shurikens)<5:
            shurikens.append(weapons(round(naruto.x+60),round(naruto.y+30),40,40,facing))
            throwSpeed=1
        
    

    if keys[pygame.K_LEFT] and naruto.x >naruto.speed:
        naruto.x-=naruto.speed
        naruto.left=True
        naruto.right=False
        naruto.standing=False
        

    elif keys[pygame.K_RIGHT] and naruto.x <690-naruto.width-naruto.speed:
        naruto.x+=naruto.speed
        naruto.left=False
        naruto.right=True
        naruto.standing=False


    else:
        naruto.standing=True
        naruto.walkCount=0

    if naruto.isjump == False:
        if keys[pygame.K_UP]:
            naruto.isjump=True
            naruto.left=False
            naruto.right=False
            naruto.walkCount=0

    else:
        if naruto.jumpheight >= -10:
            neg =1

            if naruto.jumpheight < 0:
                neg= -1

            naruto.y-=(naruto.jumpheight **2)*0.5*neg
            naruto.jumpheight -=1

        else:
            
            naruto.isjump=False
            naruto.jumpheight=10



    redrawgamewindow()

pygame.quit()    
