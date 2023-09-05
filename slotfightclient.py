import pygame
import threading
import time
import random
import slotfightnetwork

#TODO: add ranged weapon functionality and walls/platforms

player_square_size=30
FPS=60
FPS_S=1./600
width=1000
height=600
floor=height-10-player_square_size
screen=pygame.display.set_mode((width,height))
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
pygame.init()
font_start=pygame.font.SysFont(None,72)
font_timer=pygame.font.SysFont(None,110)
font_hp=pygame.font.SysFont(None,36)


class wall():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.rect=[x,y,width,height]
        self.blocking=False

class weapon():
    def __init__(self,weapon_stats):
        self.last_attack=-100
        self.damage=weapon_stats[0]
        self.can_block=weapon_stats[4]
        if self.can_block:
            self.block_multiplier=weapon_stats[6]  #reductive multiplier like .75
        else:
            self.block_multiplier=1
        self.projectile=weapon_stats[3]
        if self.projectile:
            self.magazine=weapon_stats[1]
            self.cooldown=weapon_stats[2]
            if self.magazine==1:
                self.penetrating=False
            else:
                self.penetrating=True
            self.xrange=None
            self.yrange=None
            self.block_multiplier=None
        else:
            self.xrange=weapon_stats[1]
            self.yrange=weapon_stats[2]
            self.magazine=None
            self.cooldown=weapon_stats[5]
            self.penetrating=None
        

class player():
    def __init__(self,x,y,width,height,color,id,facing):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.rect=[x,y,width,height]
        self.weapons=[]
        self.xvelocity=0
        self.yvelocity=0
        self.jump_held=False
        self.hp=100
        self.held=None
        self.id=id
        self.facing=facing #True=right, False=left
        self.outgoing_dmg=0
        self.blocking=False
        self.incoming_damage=0

    def display(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
    
    def position_update(self,x,y,width,height):
        self.rect=[x,y,width,height]

    def xmove(self):
        while running:
            x_time=time.time()
            draw_scrn()
            d=move_keys[pygame.K_d]
            a=move_keys[pygame.K_a]
            if d:
                self.facing=True
                if self.blocking and self.held.can_block:
                    self.x+=2
                else:
                    self.x+=12
                
                if self.x>width-(self.width//2):
                    self.x=width-(self.width//2)
                self.rect[0]=self.x

            if a:
                self.facing=False
                if self.blocking and self.held.can_block:
                    self.x-=2
                else:
                    self.x-=12
                
                if self.x<0-(self.width//2):
                    self.x=0-(self.width//2)
                self.rect[0]=self.x
            x_time=time.time()-x_time
            x_slp=FPS_S-x_time
            #print(x_slp)
            if x_slp>0:
                time.sleep(x_slp)
            
        return

    def ymove(self):
        while running:
            y_time=time.time()
            draw_scrn()
            w=move_keys[pygame.K_w]
            s=move_keys[pygame.K_s]
            if w and (self.y==floor or self.jump_held):
                if self.blocking and self.held.can_block:
                    self.y-=3
                else:
                    self.y-=18
                self.jump_held=True
                
                self.rect[1]=self.y
                if self.y<=100 or (self.blocking and self.held.can_block and self.y<=500):
                    self.jump_held=False
                    
            else:
                self.jump_held=False
                

            if not self.jump_held and self.y<floor:
                self.y+=6
                if s:
                    self.y+=15

                if self.y>=floor:
                    self.y=floor
                    
                self.rect[1]=self.y

            y_time=time.time()-y_time
            y_slp=FPS_S-y_time
            #print(y_slp)
            if y_slp>0:
                time.sleep(y_slp)      
        return

    def attacks(self):
        while running:
            atk=move_keys[pygame.K_e]
            blk=move_keys[pygame.K_q]
            if atk:
                self.blocking=False
                if damage_check():
                    self.outgoing_dmg=self.held.damage
            elif blk:
                self.blocking=True
            else:
                self.blocking=False
        return

    def weapon_txt(self):
        weapon_dict={1:'Unarmed',2:'Sword',3:'Shield',4:'Railgun',5:'Spear',6:'Golden Gun',7:'Mace'}
    
        return weapon_dict[self.wep_id]

    def equip(self,weapon_id):
        weapon_info_dict={1:[0,0,0,False,False,0],2:[10,10,10,False,True,1,.75],3:[0,0,0,False,True,0,0],4:[10,5,2,True,False],5:[10,20,20,False,True,3,.9],6:[50,1,1000,True,False],7:[20,10,10,False,False,3]}
        # 1:'Unarmed',2:'Sword',3:'Shield',4:'Railgun',5:'Spear',6:'Golden Gun',7:'Mace'
        #[name,damage,xrange,yrange,projectile,can_block,cooldown(seconds)]
        #[name,damage,magazine,cooldown(seconds),projectile,can_block,cooldown(seconds)]
        self.held=weapon(weapon_info_dict[weapon_id])
        self.wep_id=weapon_id

def damage_check():
        if p1.held.last_attack+p1.held.cooldown<=time.time():
            p1.held.last_attack=time.time()
            if not p1.held.projectile:
                if p1.facing:
                    atk_rect=[p1.x+p1.width,p1.y+(p1.height//2),p1.held.xrange*2,p1.held.yrange]
                else:
                    atk_rect=[p1.x,p1.y+(p1.height//2),p1.held.xrange*2,p1.held.yrange]
                if inside(atk_rect,p2,p1.facing):
                    print('hit')
                    return True
            else:
                #pass
                print('miss')
        return False
#FIX INSIDE FUNCTION TOMORROW
def inside(rect,player,right):
    #[x,y,width,height] (x,y from topleft corner)
    #player is the player class object in this function
    if right:
        rect_tl=(rect[0],rect[1])
        rect_br=(rect[0]+rect[2],rect[1]+rect[3])
    else:
        rect_br=(rect[0],rect[1])
        rect_tl=(rect[0]+rect[2],rect[1]+rect[3])
    p_tl=(player.x,player.y)
    p_br=(player.x+player.width,player.y+player.height)
    if rect_br[1]<p_tl[1] or p_br[1]<rect_tl[1]:
        print('a')
        return False
    if rect_br[0]<p_tl[0] or p_br[0]<rect_tl[0]:
        print(rect_br[0],p_tl[0],p_br[0],rect_tl[0])
        print('b')
        return False

    return True

def draw_scrn():
    screen.fill((0,0,0))
    p1.display(screen)
    p2.display(screen)
    timer=font_timer.render(str(timeleft),True,(255,255,255))
    p1hp=font_hp.render('You: '+str(p1.hp),True,(255,255,255))
    p2hp=font_hp.render('Opponent: '+str(p2.hp),True,(255,255,255))
    screen.blit(p1hp,(0,0))
    screen.blit(p2hp,(width-p2hp.get_width(),0))
    screen.blit(timer,timer.get_rect(centerx=screen.get_rect().centerx))

    pygame.display.update()

def update_move_keys():
    while running:
        global move_keys;move_keys=pygame.key.get_pressed()
    return

def update_screen():
    while running:
        draw_scrn()
    return

def starting_match():
    screen.fill((128,128,128))
    pygame.display.update()
    seen_dict={}
    disp_str=''
    time_cnt=2
    waiting=True
    while len(p1.weapons)<3:
        weapon=random.randint(1,7)
        if weapon not in seen_dict:
            p1.weapons.append(weapon)
            seen_dict[weapon]=True
            disp_str+=weapon_txt(weapon)+'     '
    disp_str=disp_str.strip()
    header_str='Your Weapons: '
    p1.held=p1.weapons[0]

    while waiting:
        screen.fill((128,128,128))
        header=font_start.render(header_str,True,(0,0,0))
        disp=font_start.render(disp_str,True,(0,0,0))
        timer=font_start.render('Waiting for Opponent',True,(255,0,0))
        screen.blit(timer,timer.get_rect(center=screen.get_rect().center))
        screen.blit(header,(header.get_rect(centerx=screen.get_rect().centerx,centery=screen.get_rect().centery-100)))
        screen.blit(disp,(disp.get_rect(centerx=screen.get_rect().centerx,centery=screen.get_rect().centery+100)))
        pygame.display.update()
        waitcheck=net.send(make_data([p1.x,p1.y,p1.hp,p1.outgoing_dmg]))
        if waitcheck=='GO':
            waiting=False
        else:
            time.sleep(.05)
    while time_cnt>0:
        screen.fill((128,128,128))
        header=font_start.render(header_str,True,(0,0,0))
        disp=font_start.render(disp_str,True,(0,0,0))
        timer=font_start.render('Match Starts In: '+str(time_cnt),True,(255,0,0))
        screen.blit(timer,timer.get_rect(center=screen.get_rect().center))
        screen.blit(header,(header.get_rect(centerx=screen.get_rect().centerx,centery=screen.get_rect().centery-100)))
        screen.blit(disp,(disp.get_rect(centerx=screen.get_rect().centerx,centery=screen.get_rect().centery+100)))
        pygame.display.update()
        time_cnt-=1
        time.sleep(1)

def make_data(player):
    #print(player)
    return str(player[0])+','+str(player[1])+','+str(player[2])+','+str(player[3])

def read_data(player):
    print(player)
    player_lst=player.split(',')
    return int(player_lst[0]),int(player_lst[1]),int(player_lst[2]),int(player_lst[3])


def weapon_txt(weapon):
    weapon_dict={1:'Unarmed',2:'Sword',3:'Shield',4:'Railgun',5:'Spear',6:'Golden Gun',7:'Mace'}
    
    return weapon_dict[weapon]

def damage_calcs():
    while running:
        if p1.blocking and p1.held.can_block:
            p1.hp-=int(p1.incoming_damage*p1.held.block_multiplier)
        else:
            p1.hp-=p1.incoming_damage
        p1.incoming_damage=0
        if p1.hp<0:
            p1.hp=0
        #print(p1.outgoing_dmg)
        #p1.outgoing_dmg=0
        #time.sleep(1/FPS)
    return

def multiplayer():
    skip_first=False #first p2update sends the outgoing damage as the x value for some reason <-easy fix
    while running:
        p2update=read_data(net.send(make_data([p1.x,p1.y,p1.hp,p1.outgoing_dmg])))
        if p1.outgoing_dmg>0:
            p1.outgoing_dmg=0
        if p2update:
            p2.x,p2.y,p2.hp=p2update[0],p2update[1],p2update[2]
            p2.rect[0],p2.rect[1]=p2update[0],p2update[1]
            
            if not skip_first:
                skip_first=True
            else:
                p1.incoming_damage=p2update[3]
    return

def round_screen(rond):
    p1.equip(p1.weapons[rond])
    screen.fill((0,0,0))
    rondy=font_start.render('Round: '+str(rond+1),True,(255,0,0))
    screen.blit(rondy,rondy.get_rect(center=screen.get_rect().center))
    pygame.display.update()
    time.sleep(1)
    screen.fill((0,0,0))
    rondy=font_start.render('Weapon: '+p1.weapon_txt(),True,(255,0,0))
    screen.blit(rondy,rondy.get_rect(center=screen.get_rect().center))
    pygame.display.update()
    time.sleep(1)
    return time.time()+15

def end_screen(text):
    if text=='You Win!':
        color=(0,255,0)
    elif text=='You Lose':
        color=(255,0,0)
    else:
        color=(255,255,255)
    screen.fill((0,0,0))
    result=font_timer.render(text,True,color)
    screen.blit(result,result.get_rect(center=screen.get_rect().center))
    pygame.display.update()
    time.sleep(2)

def main():
    global running;running=True
    global net;net=slotfightnetwork.network()
    global rnd;rnd=0
    global timeleft;timeleft=15

    start_pos=read_data(net.get_pos()) #[x,y,hp]

    if start_pos[0]==50:
        start_facing_direction=True
    else:
        start_facing_direction=False

    global p1;p1=player(start_pos[0],floor,player_square_size,player_square_size,(0,0,255),1,start_facing_direction)
    global p2;p2=player(start_pos[0],floor,player_square_size,player_square_size,(255,0,0),2,start_facing_direction)

    global move_keys;move_keys=move_keys=pygame.key.get_pressed()
    
    starting_match()

    while rnd<3:
        round_time=round_screen(rnd)
        running=True
        threading.Thread(target=update_screen).start()
        threading.Thread(target=update_move_keys).start()
        threading.Thread(target=p1.xmove).start()
        threading.Thread(target=p1.ymove).start()
        threading.Thread(target=multiplayer).start()
        threading.Thread(target=p1.attacks).start()
        threading.Thread(target=damage_calcs).start()
        #print(slotfightserver.get_players())
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                    rnd=4
                    pygame.quit()
                    break
            if time.time()>round_time:
                running=False
            else:
                timeleft=int(round_time)-int(time.time())
            if p1.hp<=0 or p2.hp<=0:
                running=False
                rnd=4
        rnd+=1
    if p1.hp>p2.hp:
        end_screen('You Win!')
    elif p1.hp<p2.hp:
        end_screen('You Lose')
    else:
        end_screen('Tie')
main()