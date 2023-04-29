from math import sin, cos, radians, degrees, atan2
import os
import random
import pygame
import pygame.font


##################################################################
#玩家設置
class Player(object):
    # 初始化資料
    def __init__(self):
        #self.rect 為玩家本身的圖塊
        self.rect = pygame.Rect(32, 32, 16, 16) #玩家位置、圖格大小

    def move(self, dx, dy):

        # 確保在單一軸上移動. 兩個if是為了同時檢查兩者
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy): #設定函數:在單一軸上移動

        # 移動單位
        self.rect.x += dx
        self.rect.y += dy

        # 如果你碰到了牆壁，玩家的圖格會被卡住(讓你不要跨越牆壁)
        for wall in walls:
            if self.rect.colliderect(wall.rect): #如果玩家撞到了牆壁
                if dx > 0: # 當你撞到左邊的牆壁，使你的圖格右邊變成牆壁的左邊。
                    self.rect.right = wall.rect.left
                if dx < 0: # 當你撞到右邊的牆壁，使你的圖格左邊變成牆壁的右邊。
                    self.rect.left = wall.rect.right
                if dy > 0: # 當你撞到上方的牆壁，使你的圖格下邊變成牆壁的上邊。
                    self.rect.bottom = wall.rect.top
                if dy < 0: # 當你撞到下方的牆壁，使你的圖格上邊變成牆壁的下邊。
                    self.rect.top = wall.rect.bottom

#第一部分牆壁設置
class Wall(object):
    # 初始化資料
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 15, 15)

#第一部分怪物設置
class Monster(object):
    # 初始化資料
    def __init__(self, pos):
        monsters.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

#第一部分通關門設置
class Winblock(object):
    # 初始化資料
    def __init__(self):
        self.rect = pygame.Rect(375, 320, 16, 32)

##############################################################


##################################################################
#第二部分射擊器設置
class Shooter(object):
    # 初始化資料
    def __init__(self):
        self.rect = pygame.Rect(376, 600, 16, 16)
        self.bullets = []
        self.direction = radians(3.14*1.5)

    def shoot(self):
        # 如果沒有子彈，就建立新子彈
        if not self.bullets:
            shooter.bullets.append(Bullet(self.rect.center, self.direction))  # 建立新的子彈
            global all_bullets
            all_bullets += 1
    # 變更射擊器角度
    def change_direction(self, angle):
        self.direction = radians(angle)

#第二部分計量條設置
class Square(object):
    # 初始化資料
    def __init__(self):
        self.rect = pygame.Rect(376, 704, 16, 16)

#第二部分子彈設置
class Bullet(object):
    # 初始化資料
    def __init__(self, pos, angle):
        self.rect = pygame.Rect(pos[0]-4, pos[1]-4, 16, 16) # 建立子彈的矩形
        self.speed = 10 # 子彈的速度
        self.angle = angle # 子彈的飛行角度
    def update(self):
        # 子彈的移動
        self.rect.x += self.speed * cos(self.angle)
        self.rect.y += self.speed * sin(self.angle)
        # 如果子彈撞到屏障，消除子彈
        for barrier in barriers:
            if self.rect.colliderect(barrier.rect):
                shooter.bullets.remove(self)
                global bullet_count
                bullet_count -= 1
                return
        # 如果子彈碰到BOSS，消除BOSS並重新創建BOSS
        for boss in bosses:
            if self.rect.colliderect(boss.rect):
                bosses.remove(boss)
                boss = Boss()
                global Boss_HP
                Boss_HP -= 1
                bullet_count -= 1
                shooter.bullets.remove(self)
                return

#第二部分屏障設置
class Barrier(object): #地圖設置
    # 初始化資料
    def __init__(self, pos):
        barriers.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

#第二部分怪物設置
class Boss(object):
    # 初始化資料
    def __init__(self):
        bosses.append(self)
        self.rect = pygame.Rect(random.randint(100,600), 150, 100, 100)

##################################################################
#初始化pygame
os.environ["SDL_VIDEO_CENTERED"] = "1" #設置pygame視窗居中顯示
pygame.init()
# 設置地圖的視窗大小
pygame.display.set_caption("Gotcha")
screen = pygame.display.set_mode((1024, 768))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
#設置字體
font = pygame.font.Font(None,50)
font2 = pygame.font.Font(None,100)
##################################################################
# 右邊螢幕資訊與結束畫面資訊
monster_number = int(8)
Win_number = int(0)
Fail_number =int(0)

bullet_count = int()
Boss_HP = int()

all_bullets =int()

#第一部分的元素
walls = [] # 保存牆壁的陣列
monsters = [] #保存怪物的陣列
player = Player() # 創建玩家

############################
#第二部分的元素

square_speed_x = 3
angle = float(270)
angle_change = float(1.46)

barriers = [] # 保存屏障的陣列
bosses = [] #保存怪物的陣列
square = Square() #創建計量條
shooter = Shooter() #創建發射器
boss = Boss() #創建怪物



##################################################################
# 將地圖資訊以字串保存在level中
#第一部分地圖設置
level1 = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W              P                               W",
    "W              P                               W",
    "W              P                               W",
    "W              P                               W",
    "W              P                               W",
    "W              P                               W",
    "W              P                        M      W",
    "W         WWWWWWW              WWWWWWW         W",
    "W         W                          W         W",
    "W         W                          W         W",
    "W     M   W       M                  W         W",
    "W         W                          W         W",
    "W         W                          W         W",
    "WPPPPPPPPPW                          WPPPPPPPPPW",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                       M      W",
    "W                                              W",
    "W                                              W",
    "W       M                                      W",
    "W                                              W",
    "W                                              W",
    "W         W                          W         W",
    "W         W                          W         W",
    "W         W                          W         W",
    "W         W                          W         W",
    "W         W                    M     W         W",
    "W         W                          W         W",
    "W         WWWWWWW              WWWWWWW         W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W            W                    W            W",
    "W            W                    W            W",
    "W       M                               M      W",
    "W                    W    W                    W",
    "W                     W  W                     W",
    "W                      WW                      W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",

]
# 將level中的文字縮寫. W = 牆壁, M = 怪物
x = y = 0
for row in level1:
    for col in row:
        if col == "W":
            Wall((x, y)) #帶入上面的class Wall
        if col == "M":
            Monster((x, y)) #設置怪物的圖格
        x += 16
    y += 16
    x = 0
##################################################################
#第二部分地圖
level2 = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W          WWWWWWWWWWWWWWWWWWWWWWWWWW          W",
    "W          W                        W          W",
    "W          WWWWWWWWWWWWWWWWWWWWWWWWWW          W",
    "W                                              W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",

]

# 將level中的文字縮寫. W = 牆壁 = Barrier, B = 怪物
x = y = 0
for row in level2:
    for col in row:
        if col == "W":
            Barrier((x, y)) #帶入上面的class barrier
        if col == "B":
            Boss((x, y)) #設置怪物的圖格

        x += 16
    y += 16
    x = 0
##################################################################
#遊戲執行
running = True
#設置第一畫面到第三畫面的背景
first_surface = pygame.Surface(screen.get_size())
second_surface =pygame.Surface(screen.get_size())
third_surface = pygame.Surface(screen.get_size())
second_surface.fill((0, 0, 0))
third_surface.fill((0, 0, 0))
current_surface = first_surface

while running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

########################################################################################
# 第一部分程式
    if current_surface == first_surface:
        # 進入第一部分時，重置第二部分的資料
        bullet_count = int(10) #設定子彈數量
        Boss_HP = random.randint(3, 7) #設定怪物血量
        # 如果玩家按下方向鍵，就使玩家移動
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-2, 0)
        if key[pygame.K_RIGHT]:
            player.move(2, 0)
        if key[pygame.K_UP]:
            player.move(0, -2)
        if key[pygame.K_DOWN]:
            player.move(0, 2)
        # 如果玩家碰撞怪物，消除怪物並減少怪物數量，同時進入第二部分
        for monster in monsters:
            if player.rect.colliderect(monster.rect):
                monsters.remove(monster)
                monster_number -= 1
                current_surface = second_surface

        first_surface.fill((0, 0, 0))
        for wall in walls:
            pygame.draw.rect(first_surface, (255, 255, 255), wall.rect) #為牆壁塗上顏色
        for monster in monsters:
            pygame.draw.rect(first_surface, (255, 0, 0), monster.rect)  # 為怪物塗上顏色
        pygame.draw.rect(first_surface, (255, 200, 0), player.rect) #為玩家塗上顏色

        #第一部分文本設置
        text_monster = font.render("Monsters: {}".format(monster_number), True, (255, 255, 255))
        first_surface.blit(text_monster, (800, 200))
        text_Win = font.render("Win: {}".format(Win_number), True, (255, 255, 255))
        first_surface.blit(text_Win, (820, 300))
        text_Fail = font.render("Fail: {}".format(Fail_number), True, (255, 255, 255))
        first_surface.blit(text_Fail, (820, 400))
        #如果清除怪物達X隻，將文本顯示並建立通關門
        if Win_number >= 5:
            winblock = Winblock()
            pygame.draw.rect(first_surface, (255, 200, 255), (winblock.rect.x, winblock.rect.y, 16 ,32 ),5)
            text_Door1 = font.render(("The door is"), True, (255, 255, 255))
            first_surface.blit(text_Door1, (800, 500))
            text_Door2 = font.render(("OPEN!!!!!!!"), True, (255, 255, 255))
            first_surface.blit(text_Door2, (800, 550))
            text_go = font.render(("You can leave"), True, (255, 255, 255))
            first_surface.blit(text_go, (780, 600))
            text_fight = font.render(("or fighting"), True, (255, 255, 255))
            first_surface.blit(text_fight, (800, 650))
            # 如過碰到通關門，進入結束畫面
            if player.rect.colliderect(winblock.rect):
                current_surface = third_surface

########################################################################################
# 第二部分程式
    elif current_surface == second_surface:
        square.rect.x -= square_speed_x
        for barrier in barriers:
            if square.rect.colliderect(barrier.rect):
                square_speed_x *= -1  # 如果量條的方塊撞到了牆壁

        key = pygame.key.get_pressed()
        # 如果王的血量歸零或是子彈歸零，就無法射擊
        if not Boss_HP ==0:
            if not bullet_count ==0:
                if key[pygame.K_SPACE]:
                    shooter.shoot()
        #控制發射器的角度，使隨時間變化
        angle -= angle_change
        if angle < 180:
            angle_change *= -1
        elif angle > 360:
            angle_change *= -1
        shooter.change_direction(angle)

        second_surface.fill((0, 0, 0))  # 將背景塗成黑色
        for barrier in barriers:
            pygame.draw.rect(second_surface, (255, 255, 255), barrier.rect)  # 為牆壁塗上顏色
        for boss in bosses:
            pygame.draw.rect(second_surface, (255, 0, 0), boss.rect)  # 為怪物塗上顏色
        pygame.draw.circle(second_surface, (255, 255, 0), (shooter.rect.x, shooter.rect.y), 16, 0)
        pygame.draw.rect(second_surface, (255, 0, 255), square.rect)

        #第二部分文本設置
        text_Boss_HP = font.render("Boss HP: {}".format(Boss_HP), True, (255, 255, 255))
        second_surface.blit(text_Boss_HP, (800, 200))
        text_bullets = font.render("bullets: {}".format(bullet_count), True, (255, 255, 255))
        second_surface.blit(text_bullets, (800, 300))
        text_factor = font.render(("Don't Lose"), True, (255, 255, 255))
        second_surface.blit(text_factor, (800, 550))
        text_factor2 = font.render(("Fight 4 Times"), True, (255, 255, 255))
        second_surface.blit(text_factor2, (800, 600))
        text_factor3 = font.render(("Press Space"), True, (255, 255, 255))
        second_surface.blit(text_factor3, (800, 650))
        text_factor4 = font.render(("To Shoot"), True, (255, 255, 255))
        second_surface.blit(text_factor4, (800, 700))
        #如果怪物血量歸零，清除怪物並顯示文本
        if Boss_HP == 0:
            for boss in bosses:
                bosses.remove(boss)
            text_PASS = font2.render(("PASS"), True, (255, 255, 255))
            second_surface.blit(text_PASS, (290, 300))
            text_Next = font.render("press c to continue", True, (255, 255, 255))
            second_surface.blit(text_Next, (220, 400))
            #按下C回到第一部分
            if key[pygame.K_c]:
                current_surface = first_surface
                Boss()
                Win_number += 1
        #如果子彈歸零，清除怪物並顯示文本
        elif bullet_count == 0 or bullet_count < Boss_HP:
            for boss in bosses:
                bosses.remove(boss)
            text_FAIL = font2.render(("FAIL"), True, (255, 255, 255))
            second_surface.blit(text_FAIL, (290, 300))
            text_Next = font.render("press c to continue", True, (255, 255, 255))
            second_surface.blit(text_Next, (210, 400))
            if key[pygame.K_c]:
                current_surface = first_surface
                Boss()
                Fail_number +=1
            if Fail_number >= 4:
                current_surface = third_surface
        #繪畫子彈
        for bullet in shooter.bullets:
            bullet.update()
            pygame.draw.circle(second_surface, (255, 255, 0), (bullet.rect.x, bullet.rect.y), 16, 0)
########################################################################################
# 結束畫面
    else:
        if Fail_number >= 4:
            text_You_LOSE = font2.render(("YOU are Loser"), True, (255, 255, 255))
            third_surface.blit(text_You_LOSE, (270, 250))
        else:
            text_congratulation = font2.render(("Congratulation"), True, (255, 255, 255))
            third_surface.blit(text_congratulation, (270, 250))
        text_kill_monster = font.render("Kill Monster: {}".format(Win_number), True, (255, 255, 255))
        third_surface.blit(text_kill_monster, (290, 400))
        text_escape_monster = font.render("Escape Monster: {}".format(Fail_number), True, (255, 255, 255))
        third_surface.blit(text_escape_monster, (290, 500))
        text_All_bullet = font.render("Bullets use: {}".format(all_bullets), True, (255, 255, 255))
        third_surface.blit(text_All_bullet, (290, 600))

    screen.blit((current_surface), (0, 0))
    pygame.display.flip() #畫面更新
    clock.tick(60)

pygame.quit()