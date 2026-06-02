import tkinter as tk
import random
from PIL import Image, ImageTk

# =========================
# WINDOW SETTINGS
# =========================
WIDTH = 900
HEIGHT = 350
GROUND_Y = 280

root = tk.Tk()
root.title("Dino Game")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="white"
)
canvas.pack()

# =========================
# LOAD IMAGES
# =========================

# Background
bg_image = Image.open("bg.png")
bg_image = bg_image.resize((WIDTH, HEIGHT))
bg_img = ImageTk.PhotoImage(bg_image)

# Dino
dino_image = Image.open("dino.png").convert("RGBA")
dino_image = dino_image.resize((70, 70))
dino_img = ImageTk.PhotoImage(dino_image)

# Cactus
cactus_image = Image.open("cactus.png").convert("RGBA")
cactus_image = cactus_image.resize((50, 70))
cactus_img = ImageTk.PhotoImage(cactus_image)

# =========================
# DRAW BACKGROUND
# =========================
canvas.create_image(
    0,
    0,
    image=bg_img,
    anchor="nw"
)

# Ground
canvas.create_line(
    0,
    GROUND_Y,
    WIDTH,
    GROUND_Y,
    width=3
)

# =========================
# DINO
# =========================
dino_x = 100
dino_y = GROUND_Y - 70

dino = canvas.create_image(
    dino_x,
    dino_y,
    image=dino_img,
    anchor="nw"
)

# Physics
velocity_y = 0
gravity = 1
jump_power = -18
jumping = False

# =========================
# GAME VARIABLES
# =========================
obstacles = []
game_speed = 10
score = 0
game_running = True

score_text = canvas.create_text(
    760,
    30,
    text="Score: 0",
    font=("Arial", 20, "bold"),
    fill="black"
)

# =========================
# JUMP
# =========================
def jump(event):
    global velocity_y
    global jumping

    if not jumping and game_running:
        velocity_y = jump_power
        jumping = True


root.bind("<space>", jump)

# =========================
# CREATE OBSTACLE
# =========================
def create_obstacle():

    obstacle = canvas.create_image(
        WIDTH,
        GROUND_Y - 70,
        image=cactus_img,
        anchor="nw"
    )

    obstacles.append(obstacle)

# =========================
# MOVE OBSTACLES
# =========================
def move_obstacles():
    global score
    global game_running

    dino_coords = canvas.bbox(dino)

    for obstacle in obstacles[:]:

        canvas.move(obstacle, -game_speed, 0)

        obstacle_coords = canvas.bbox(obstacle)

        # Remove obstacle
        if obstacle_coords[2] < 0:

            canvas.delete(obstacle)
            obstacles.remove(obstacle)

            score += 1

            canvas.itemconfig(
                score_text,
                text=f"Score: {score}"
            )

        # Collision
        overlap = not (
            dino_coords[2] < obstacle_coords[0]
            or dino_coords[0] > obstacle_coords[2]
            or dino_coords[3] < obstacle_coords[1]
            or dino_coords[1] > obstacle_coords[3]
        )

        if overlap:
            game_over()

# =========================
# UPDATE DINO
# =========================
def update_dino():
    global velocity_y
    global jumping

    canvas.move(dino, 0, velocity_y)

    velocity_y += gravity

    coords = canvas.coords(dino)

    if coords[1] >= GROUND_Y - 70:

        canvas.coords(
            dino,
            dino_x,
            GROUND_Y - 70
        )

        velocity_y = 0
        jumping = False

# =========================
# GAME OVER
# =========================
def game_over():
    global game_running

    game_running = False

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text="GAME OVER",
        fill="red",
        font=("Arial", 40, "bold"),
        tags="gameover"
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 50,
        text="Press R to Restart",
        fill="black",
        font=("Arial", 20),
        tags="gameover"
    )

# =========================
# RESTART
# =========================
def restart(event):

    global obstacles
    global score
    global game_running
    global velocity_y
    global jumping
    global game_speed

    for obstacle in obstacles:
        canvas.delete(obstacle)

    obstacles.clear()

    canvas.delete("gameover")

    canvas.coords(
        dino,
        dino_x,
        GROUND_Y - 70
    )

    velocity_y = 0
    jumping = False

    score = 0

    canvas.itemconfig(
        score_text,
        text="Score: 0"
    )

    game_speed = 10

    game_running = True

    game_loop()


root.bind("r", restart)

# =========================
# GAME LOOP
# =========================
spawn_timer = 0

def game_loop():
    global spawn_timer
    global game_speed

    if game_running:

        update_dino()

        move_obstacles()

        spawn_timer += 1

        # Spawn obstacle
        if spawn_timer > random.randint(40, 70):

            create_obstacle()

            spawn_timer = 0

        # Increase difficulty
        game_speed = 10 + score // 5

        root.after(30, game_loop)

# =========================
# START GAME
# =========================
game_loop()

root.mainloop()