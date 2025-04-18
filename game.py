import pygame
import random
scr_wid = 600
scr_hei = 600

class Snake :
    def __init__(self, screen) :
        self.screen = screen
        self.body = []   #长度
        self.fx = pygame.K_RIGHT   #方向
        self.init_body()
    
    def init_body(self, length = 3) :
        left, top = (0, 0)
        for i in range(5) :
            if self.body :
                left, top = self.body[0].left, self.body[0].top
                node = pygame.Rect(left+20, top, 20, 20)
            else :
                node = pygame.Rect(0, 0, 20, 20)
            self.body.insert(0, node)
    
    def draw_snake(self) :
        for i in self.body :
            pygame.draw.rect(self.screen, (255, 50, 50), i, 0)
    
    def add_node(self) :
        if self.body :
            left, top = self.body[0].left, self.body[0].top
            if self.fx == pygame.K_RIGHT :
                left += 20
            elif self.fx == pygame.K_LEFT :
                left -= 20
            elif self.fx == pygame.K_UP :
                top -= 20
            else :
                top += 20
            node = pygame.Rect(left, top, 20, 20)
            self.body.insert(0, node)

    def del_node(self) :
        self.body.pop()

    def move(self) :
        self.add_node()
        self.del_node()
    
    def change_fx(self, fx) :
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if fx in LR or UD :
            if (fx in LR and self.fx in LR) or (fx in UD and self.fx in UD) :
                return
            self.fx = fx

    def is_dead(self) :
        if self.body[0].left not in range(scr_wid) :
            return True
        if self.body[0].top not in range(scr_hei) :
            return True
        if self.body[0] in self.body[1:] :
            return True

class Food :
    def __init__(self) :
        self.node = pygame.Rect(60, 80, 20, 20)
        self.flag = False
    
    def set(self) :
        all_x_points = range(20, scr_wid - 20, 20)
        all_y_points = range(20, scr_hei - 20, 20)
        left = random.choice(all_x_points)
        top = random.choice(all_y_points)
        self.node = pygame.Rect(left, top, 20, 20)
        self.flag = False

    def reset(self) :
        self.flag = True

def show_text(screen, text, left, top) :
    font = pygame.font.SysFont('隶书', 30)
    text = font.render(text, True, (255, 0, 0))
    screen.blit(text, (left, top))

def main() :
    pygame.init()
    screen = pygame.display.set_mode([scr_wid, scr_hei])  #创建窗口
    sk = Snake(screen)   
    fd = Food()
    clock = pygame.time.Clock()
    dead = False    #蛇是否死亡的标识，False则没死

    while True :
        for i in pygame.event.get() :
            if i.type == pygame.QUIT :
                pygame.quit()
            if i.type == pygame.KEYDOWN :
                sk.change_fx(i.key)
                if i.key == pygame.K_SPACE :
                    sk = Snake(screen)   
                    fd = Food()
                    dead = False

        screen.fill((255,255,255))
        sk.draw_snake()   #画蛇
        if not dead:
            sk.move()     #蛇移动

        if sk.is_dead() :   #判断是否死亡, True则死
            show_text(screen, '已死亡', 230, 250)
            show_text(screen, '按下空格重新开始', 150, 280)
            dead = True

        if fd.flag :
            fd.set()   #放食物

        pygame.draw.rect(screen, (50, 255, 50), fd.node, 0)

        if sk.body[0] == fd.node :   #吃食物
            sk.add_node()
            fd.reset()

        pygame.display.update()
        clock.tick(20)

if __name__ == "__main__" :
    main()