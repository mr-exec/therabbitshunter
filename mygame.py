# 1 Import Library ------------------------------------
import  pygame
import math
from pygame.locals import *
from random import randint
# 2 Bentuk Game ---------------------------------------

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TheRabbitsHunter')

#key mapping
keys = {
    "top": False,
    "bottom": False,
    "left": False,
    "right": False
}

running = True

playerpos = [100, 100] # Bentuk Posisi Player

# exit code for game over and win codition
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1

#score -
score = 0
health_point = 194 # darah point
countdown_timer = 60000 # 90 detik
arrows = []# list anak panah

enemy_timer = 100 # waktu kemunculan
enemies = [[width, 100]] # list yang menampung koordinat musuh

# 3 Game File Bentuk ----------------------------------
# 3.1 File Image
player = pygame.image.load("images/dude.png")
grass = pygame.image.load("images/lantai.jpg")
castle = pygame.image.load("images/castlee.jpg")
arrow = pygame.image.load("images/bullet.png")
enemy_img = pygame.image.load("images/badguy.png")
peledak = pygame.image.load("images/peledak.png")
healthbar = pygame.image.load("images/healthbar.png")
health = pygame.image.load("images/health.png")
gameover = pygame.image.load("images/gameover.png")
youwin = pygame.image.load("images/youwin.png")


# Sound -----------------------------------------------
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("audio/explode.wav")
enemy_hit_sound = pygame.mixer.Sound("audio/enemy.wav")
shoot_sound = pygame.mixer.Sound("audio/shoot.wav")
hit_sound.set_volume(0.50)
enemy_hit_sound.set_volume(0.50)
shoot_sound.set_volume(0.50)

# background music
pygame.mixer.music.load("audio/mario bros.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.50)

# 4 Game loop -----------------------------------------
while(running):
    # 5 Membersihkan layar ----------------------------
    screen.fill(0)

    # 6 Game object -----------------------------------
    # rumput ------------------------------------------
    for x in range(int(width/grass.get_width()+1)):
        for y in range(int(height/grass.get_height()+1)):
            screen.blit(grass, (x*100, y*100))


    # castil ------------------------------------------
    screen.blit(castle, (0, 0))
    screen.blit(castle, (0, 100))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))
    # gambar player -------------------------------------------
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (playerpos[1] + 32), mouse_position[0] - (playerpos[0] + 26))
    player_rotation = pygame.transform.rotate(player, 360 - angle * 60.00)
    new_playerpos = (
    playerpos[0] - player_rotation.get_rect().width / 2, playerpos[1] - player_rotation.get_rect().height / 2)
    screen.blit(player_rotation, new_playerpos)

    #6.1 gambar player --------------------------------
    for bullet in arrows:
        arrow_index = 0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            arrows.pop(arrow_index)
        arrow_index += 1
        # Gambar the arrow
        for projectile in arrows:
            new_arrow = pygame.transform.rotate(arrow, 360 - projectile[0] * 60.00)
            screen.blit(new_arrow, (projectile[1], projectile[2]))

    # 6.2 - Draw Enemy
    # waktu musuh akan muncul
    enemy_timer -= 1
    if enemy_timer == 0:
        # buat musuh baru
        enemies.append([width, randint(50, height - 32)])
        # reset enemy timer to random time
        enemy_timer = randint(1, 100)

    index = 0
    for enemy in enemies:
        # musuh bergerak dengan kecepatan 5 pixel ke kiri
        enemy[0] -= 2
        # hapus musuh saat mencapai batas layar sebelah kiri
        if enemy[0] < -64:
            enemies.pop(index)

    #6.2.1 benturan antara musuh dan castil
        enemy_rect = pygame.Rect(enemy_img.get_rect())
        enemy_rect.top = enemy[1]# titik y
        enemy_rect.left = enemy[0]# titik x
    #benturan musuh dengan castil
        if enemy_rect.left < 64:
            enemies.pop(index)
            screen.blit(peledak, enemy)
            health_point -= randint(5,20)
            # collision enemy dengan castil
            hit_sound.play()
            print("Oh no, we were attacked!!!")

    #6.2.2 memeriksa dari benturan antara musuh dan anak panah
        index_arrow = 0
        for bullet in arrows:
            bullet_rect = pygame.Rect(arrow.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            #benturan anak panah dengan musuh
            if enemy_rect.colliderect(bullet_rect):
                score += 1
                enemies.pop(index)
                arrows.pop(index_arrow)
                # collision anak panah dengan musuh
                enemy_hit_sound.play()
                print("Boom! Die you!")
                print("Score: {}".format(score))
            index_arrow += 1
        index += 1

    # gambar musuh ke layar
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    #6.3 Bar darah ------------------------------------
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))

    #6.4 gambar waktu ---------------------------------
    font = pygame.font.Font(None, 24)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000)# 60000 sama dengan 60 detik
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)
    # 7 update screen ---------------------------------
    pygame.display.flip()

    # 8 Event loop ------------------------------------
    for event in pygame.event.get():
        # event saat tombol exit diklik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Tembakan
        if event.type == pygame.MOUSEBUTTONDOWN:
            arrows.append([angle, new_playerpos[0]+32, new_playerpos[1]+32])


        # periksa keyword dan keyup
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_a:
                keys["left"] = True
            elif event.key == K_s:
                keys["bottom"] = True
            elif event.key == K_d:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_a:
                keys["left"] = False
            elif event.key == K_s:
                keys["bottom"] = False
            elif event.key == K_d:
                keys["right"] = False
        # Selesai dari event loop --------------------

    # 9. Bergerak ------------------------------------
    if keys["top"]:
        playerpos[1] -= 5 # kurangi nilai y
    elif keys["bottom"]:
        playerpos[1] += 5 # tambah nilai y
    if keys["left"]:
        playerpos[0] -= 5 # kurangi nilai x
    elif keys["right"]:
        playerpos[0] += 5 # tambah nilai x

    # 10. win/lose periksa -------------------------------
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER

    # Akhir dari game loop -------------------------------

    # 11. - Win/lose display -----------------------------
if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(youwin, (0, 0))

# Tampilkan score
text = font.render("Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.flip()


