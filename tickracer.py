import tkinter as tk
import threading
import time
import random

WIDTH = 320
HEIGHT = 500

LANES = [70, 160, 250]

LEVELS = [
    "levels/level1.tick",
    "levels/level2.tick",
    "levels/level3.tick"
]

current_level = 0

player_lane = 1
enemy_cars = []

game_started = False
game_over = False
level_running = False

# Tick-controlled timing
level_speed = 1.0

root = tk.Tk()
root.title("Tick Racer")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)
canvas.pack()

# --------------------------
# ROAD
# --------------------------
for x in [110, 210]:
    canvas.create_line(x, 0, x, HEIGHT, fill="white", dash=(10, 10))


# --------------------------
# PLAYER
# --------------------------
player_parts = []

def draw_player():
    global player_parts

    for p in player_parts:
        canvas.delete(p)

    x = LANES[player_lane]

    body = canvas.create_rectangle(
        x - 18, 420,
        x + 18, 470,
        fill="cyan",
        outline=""
    )

    roof = canvas.create_rectangle(
        x - 10, 430,
        x + 10, 445,
        fill="white",
        outline=""
    )

    player_parts = [body, roof]


# --------------------------
# ENEMY
# --------------------------
def spawn_enemy(lane):
    x = LANES[lane]

    body = canvas.create_rectangle(
        x - 18, -50,
        x + 18, 0,
        fill="red",
        outline=""
    )

    roof = canvas.create_rectangle(
        x - 10, -40,
        x + 10, -25,
        fill="white",
        outline=""
    )

    enemy_cars.append({
        "lane": lane,
        "parts": [body, roof]
    })


# --------------------------
# UI
# --------------------------
title_text = canvas.create_text(
    WIDTH // 2,
    HEIGHT // 2 - 40,
    text="TICK RACER",
    fill="white",
    font=("Courier", 24, "bold")
)

start_text = canvas.create_text(
    WIDTH // 2,
    HEIGHT // 2 + 20,
    text="PRESS SPACE",
    fill="yellow",
    font=("Courier", 14)
)

overlay = None

def show_overlay(text):
    global overlay

    if overlay:
        canvas.delete(overlay)

    overlay = canvas.create_text(
        WIDTH // 2,
        100,
        text=text,
        fill="yellow",
        font=("Courier", 18, "bold")
    )

    root.after(1200, lambda: canvas.delete(overlay))


# --------------------------
# LEVEL SYSTEM
# --------------------------
def next_level():
    global current_level

    current_level += 1

    if current_level >= len(LEVELS):
        show_overlay("YOU WIN")
        return

    start_level()


def run_tick_file(path):
    global level_running, level_speed

    with open(path) as f:
        lines = f.readlines()

    for line in lines:

        if game_over:
            return

        parts = line.strip().split()
        if not parts:
            continue

        cmd = parts[0]

        # --------------------------
        # SPEED CONTROL (WAIT)
        # --------------------------
        if cmd == "wait":
            level_speed = float(parts[1])

        # --------------------------
        # TIME STEP (PING)
        # --------------------------
        elif cmd == "ping":
            time.sleep(level_speed)

        # --------------------------
        # GAME EVENTS
        # --------------------------
        elif cmd == "signal":
            sig = int(parts[1])

            # normal lanes
            if sig in [1, 2, 3]:
                spawn_enemy(sig - 1)

            # level start center car behavior
            elif sig == 2:
                spawn_enemy(1)

            elif sig == 100:
                show_overlay("LEVEL 1")

            elif sig == 101:
                show_overlay("LEVEL 2")

            elif sig == 200:
                level_running = False
                root.after(1500, next_level)

    level_running = False


def start_level():
    global level_running, level_speed

    level_running = True

    # baseline difficulty scaling per level
    level_speed = 1.0 - (current_level * 0.2)
    if level_speed < 0.3:
        level_speed = 0.3

    threading.Thread(
        target=run_tick_file,
        args=(LEVELS[current_level],),
        daemon=True
    ).start()


# --------------------------
# RESET GAME
# --------------------------
def reset_game():
    global enemy_cars, player_lane, game_over, current_level, game_started, level_running

    enemy_cars = []
    player_lane = 1
    game_over = False
    game_started = True
    level_running = False
    current_level = 0

    canvas.delete("all")

    for x in [110, 210]:
        canvas.create_line(x, 0, x, HEIGHT, fill="white", dash=(10, 10))

    draw_player()
    start_level()


# --------------------------
# CONTROLS
# --------------------------
def move_left(event):
    global player_lane

    if game_started and not game_over and player_lane > 0:
        player_lane -= 1
        draw_player()


def move_right(event):
    global player_lane

    if game_started and not game_over and player_lane < 2:
        player_lane += 1
        draw_player()


def start_game(event):
    global game_started

    if not game_started:
        game_started = True
        canvas.delete(title_text)
        canvas.delete(start_text)
        draw_player()
        start_level()


def restart(event):
    if game_over:
        reset_game()


root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<space>", start_game)
root.bind("r", restart)


# --------------------------
# GAME LOOP
# --------------------------
def game_loop():
    global game_over

    if not game_over:

        for car in enemy_cars[:]:

            for part in car["parts"]:
                canvas.move(part, 0, 5)

            x1, y1, x2, y2 = canvas.coords(car["parts"][0])

            # cleanup
            if y1 > HEIGHT:
                for p in car["parts"]:
                    canvas.delete(p)
                enemy_cars.remove(car)
                continue

            # collision
            PLAYER_Y = 430

            if (
                car["lane"] == player_lane and
                y2 > PLAYER_Y and
                y1 < PLAYER_Y + 40
            ):
                game_over = True

                canvas.create_text(
                    WIDTH // 2,
                    HEIGHT // 2 - 20,
                    text="GAME OVER",
                    fill="red",
                    font=("Courier", 24, "bold")
                )

                canvas.create_text(
                    WIDTH // 2,
                    HEIGHT // 2 + 20,
                    text="Press R to Retry",
                    fill="white",
                    font=("Courier", 14)
                )

    root.after(16, game_loop)


draw_player()
game_loop()

root.mainloop()
