import pygame
import webbrowser,time,os,clipboard
import pyautogui as pag
#print(clipboard.paste())
fonts=[]
print("------------------------------------------\nFonts available :")
for i in os.listdir():
    if i.endswith(".ttf"):
        print(i)
        fonts.append(i)
print("------------------------------------------")
pygame.init()

# 0=Darkest; 1=Second Darkest; 2=Bright Accent Color; 3=Brightest;
colors=[((34, 40, 49)),((57, 62, 70)),((253, 112, 20)),((238, 238, 238))]
win=pygame.display.set_mode((900,650))
pygame.display.set_caption("TAC Engine")
pygame.display.set_icon(pygame.image.load("tac_logo.png").convert_alpha())


class edit_text():
    def __init__(self,x,y,w,h,colors,text,f_size=16,e_type='num',overflow=True):
        self.x,self.y=x,y
        self.w,self.h=w,h
        self.colors=colors
        self.text=text
        self.f_size=f_size
        self.rect=pygame.Rect((self.x,self.y),(self.w,self.h))
        self.editing=False
        self.edit_type=e_type
        self.overflow=overflow
        self.blinker_pos_inv=0
        self.textRect=None

    def edit(self,key,b):
        if not(key==None):
            if key=='left' and self.blinker_pos_inv<len(self.text):
                self.blinker_pos_inv+=1
            if key=='right' and self.blinker_pos_inv>0:
                self.blinker_pos_inv-=1
                
            #standard keyboard operations
            if self.blinker_pos_inv==0:
                if key=='backspace':
                    self.text=self.text[:-1]

                elif key=='`':
                    if self.edit_type=="num":
                        try:
                            self.text+=str(int(clipboard.paste()))
                        except:
                            pass
                    else:
                        self.text+=str(clipboard.paste())
                        
                elif key=='space':
                    self.text+=" "
                elif key=="enter":
                    self.editing=False
                    for e in b:
                        e.edit=False
                        
                #actual typing
                else:
                    if self.edit_type=='num':
                        try:
                            self.text+=str(int(key))
                        except:
                            if key[0]=="[":
                                try:
                                    key=str(int(key[1]))
                                    self.text+=str(int(key))
                                except:
                                    print(key)
                            else:
                                print(key)
                                
                    if self.edit_type=='text':
                        if len(str(key))==1:
                            self.text+=str(key)
                        else:
                            if len(key)==3 and key[0]=='[':
                                self.text+=str(key[1])
                            print(key)
                            
            

            else:
                if self.blinker_pos_inv==len(self.text):
                    #standard keyboard operations
                    if key=='delete':
                        self.text=self.text[1:]

                    elif key=='`':
                        if self.edit_type=="num":
                            try:
                                self.text=str(int(clipboard.paste()))+self.text
                            except:
                                pass
                        else:
                            self.text=str(clipboard.paste())+self.text
                            
                    elif key=='space':
                        self.text=" "+self.text
                    elif key=="enter":
                        self.editing=False
                        for e in b:
                            e.edit=False
                            
                    #actual typing
                    else:
                        if self.edit_type=='num':
                            try:
                                self.text=str(int(key))+self.text
                            except:
                                if key[0]=="[":
                                    try:
                                        key=str(int(key[1]))
                                        self.text=str(int(key))+self.text
                                    except:
                                        print(key)
                                else:
                                    print(key)
                                    
                        if self.edit_type=='text':
                            if len(str(key))==1:
                                self.text=str(key)+self.text
                            else:
                                if len(key)==3 and key[0]=='[':
                                    self.text=str(key[1])+self.text
                                print(key)

                else:
                    sep=-self.blinker_pos_inv
                    #standard keyboard operations
                    if key=='delete':
                        if sep==-1:
                            self.text=self.text[:sep]
                        else:
                            self.text=self.text[:sep]+self.text[sep+1:]
                        self.blinker_pos_inv-=1
                        sep+=1

                    elif key=='`':
                        if self.edit_type=="num":
                            try:
                                self.text=self.text[:sep]+str(int(clipboard.paste()))+self.text[sep:]
                            except:
                                pass
                        else:
                            self.text=self.text[:sep]+str(clipboard.paste())+self.text[sep:]
                    
                    elif key=='backspace':
                        self.text=self.text[:sep-1]+self.text[sep:]
                    elif key=='space':
                        self.text=self.text[:sep]+" "+self.text[sep:]
                    elif key=="enter":
                        self.editing=False
                        for e in b:
                            e.edit=False
                            
                    #actual typing
                    else:
                        if self.edit_type=='num':
                            try:
                                self.text=self.text[:sep]+str(int(key))+self.text[sep:]
                            except:
                                if key[0]=="[":
                                    try:
                                        key=str(int(key[1]))
                                        self.text=self.text[:sep]+str(int(key))+self.text[sep:]
                                    except:
                                        print(key)
                                else:
                                    print(key)
                                    
                        if self.edit_type=='text':
                            if len(str(key))==1:
                                self.text=self.text[:sep]+str(key)+self.text[sep:]
                            else:
                                if len(key)==3 and key[0]=='[':
                                    self.text=self.text[:sep]+str(key[1])+self.text[sep:]
                                print(key)

                                

    def edit_check(self,down,editing):
        if down:
            if not(editing==None):
                self.editing=False
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.editing=True
        '''if down:
            k=False
            for e in b:
                if e.edit:
                    k=True
            if k:
                self.editing=False
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.editing=True
        '''
        
    def draw(self,win,font,b,edting):
        pygame.draw.rect(win,colors[0],self.rect)
        self.display_text=str(self.text)
        
        dtext = font.render(str(self.display_text),False,self.colors[2])
        dtextRect=dtext.get_rect()
        if dtextRect[2]>self.w:
            if not(self.overflow):
                self.edit("backspace",b)
                self.display_text=self.text
            else:
                while dtextRect[2]>self.w:
                    self.display_text=self.display_text[1:]
                    dtext = font.render(str(self.display_text),False,self.colors[2])
                    dtextRect=dtext.get_rect()
                                
        text = font.render(str(self.display_text),False,self.colors[2])
        self.textRect=text.get_rect()
        self.textRect.center=self.x+2+(self.textRect[2]//2),self.y-2+(self.textRect[3]//2)
        if edting==None:
            self.editing=False

        n=False
        for e in b:
            if e.edit:
                n=True
                
        if n:
            win.blit(text,self.textRect)
            if self.editing:
                if int(time.time()%2)==1:
                    pygame.draw.rect(win,colors[3],((self.textRect[0]+self.textRect[2] - (self.blinker_pos_inv*8) , self.textRect[1]+3)  ,  (2 ,self.h-4)))
                
        
def color_image(surface, color):
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def draw_text(win,x,y,text,color,font):
    text = font.render(text,False,color)
    textRect=text.get_rect()
    textRect.center=x+(textRect[2]//2),y+(textRect[3]//2)
    win.blit(text,textRect)

class button():
    def __init__(self,x,y,w,h,icon,add_type,colors,b_r=10):
        self.x,self.y,self.w,self.h=x,y,w,h
        self.color=colors[0]
        self.icon=pygame.transform.scale(pygame.image.load(icon).convert_alpha(),(self.w-8,self.h-8))
        color_image(self.icon,colors[3])
        self.b_r=b_r
        self.rect=pygame.Rect((x,y),(w,h))
        self.add_type=add_type
        self.last_down=False
        
    def press_check(self,down):
        if down and not(self.last_down):
            self.last_down=down
            x,y=pygame.mouse.get_pos()
            if self.rect.collidepoint(x,y):
                if self.add_type=="text":
                    return element(x-20,y-20,"Text","text")
                if self.add_type=="image":
                    return element(x-20,y-20,"image.png","image")
        self.last_down=down
        return 0        
        
    def draw(self,win):
        pygame.draw.rect(win,self.color,self.rect,border_radius=self.b_r)
        win.blit(self.icon,(self.x+4,self.y+4))
        
class element():
    def __init__(self,x,y,holding,hold_type="text",w=40,h=40,color=((0,0,0)),b_r=10):
        self.w,self.h,self.b_r=w,h,b_r
        self.x,self.y=x,y
        self.color=color
        self.h_type=hold_type
        self.holding=holding
        self.dragging=False
        self.edit=True
        self.edit_pos=0,0
        self.rect=pygame.Rect((x,self.y),(self.w,self.h))
        self.font='ubuntu-mono.ttf'
        self.f_size=16
        if hold_type=="text":
            font = pygame.font.Font(self.font,self.f_size)
            self.text = font.render(holding,False,self.color)
            self.textRect=self.text.get_rect()
            self.textRect.center=self.x+(self.w//2),self.y+(self.h//2)
        if hold_type=="image":
            self.image=pygame.image.load(self.holding).convert_alpha()
            self.image=pygame.transform.scale(self.image,(w,h))
                        

    def update(self,ed):
        if self.edit:
            n=0
            for e in ed:
                if n==0:
                    if e.editing:
                        try:
                            self.x=int(e.text)
                        except:
                            self.x=0
                    else:
                        e.text=str(self.x)
                        
                if n==1:
                    if e.editing:
                        try:
                            self.y=int(e.text)+70
                        except:
                            self.y=70
                    else:
                        e.text=str(self.y-70)
                if n==2:
                    if e.editing:
                        self.holding=e.text
                    else:
                        e.text=self.holding


                if self.h_type=="text":
                    if n==3:
                        if e.editing:
                            self.font=e.text+".ttf"
                        else:
                            e.text=self.font[:-4]
                    if n==4:
                        if e.editing:
                            try:
                                self.f_size=int(e.text)
                            except:
                                pass
                        else:
                            e.text=str(self.f_size)
                else:
                    if n==3:
                        if e.editing:
                            try:
                                self.w=int(e.text)
                            except:
                                pass
                        else:
                            e.text=str(self.w)
                    if n==4:
                        if e.editing:
                            try:
                                self.h=int(e.text)
                            except:
                                pass
                        else:
                            e.text=str(self.h)
                        
                n+=1

            if self.h_type=="text":
                try:
                    font = pygame.font.Font(self.font,self.f_size)
                    self.text = font.render(self.holding,False,self.color)
                    self.textRect=self.text.get_rect()
                    self.textRect.center=self.x+(self.w//2),self.y+(self.h//2)
                    self.rect=self.textRect
                    self.x,self.y,self.w,self.h=self.rect
                    self.x-=2
                    self.w+=4
                except:
                    pass
                
            if self.h_type=="image":
                try:
                    self.image=pygame.image.load(self.holding).convert_alpha()                
                    self.image=pygame.transform.scale(self.image,(self.w,self.h))
                    self.rect=pygame.Rect((self.x,self.y),(self.w,self.h))
                except:
                    pass
            
    def draw(self,win):
        if self.edit:
            pygame.draw.line(win,((0,0,0)),(self.x,self.y),(self.x+self.w,self.y))
            pygame.draw.line(win,((0,0,0)),(self.x+self.w,self.y),(self.x+self.w,self.y+self.h))
            pygame.draw.line(win,((0,0,0)),(self.x+self.w,self.y+self.h),(self.x,self.y+self.h))
            pygame.draw.line(win,((0,0,0)),(self.x,self.y),(self.x,self.y+self.h))
                
        if self.h_type=="text":
            win.blit(self.text,self.textRect)
        if self.h_type=="image":
            win.blit(self.image,self.rect)

        
def edit_check(b,right_click,ld_r,edting):
    ignore=False
    if right_click and not(ld_r):
        m=0
        for item in b:
            if not(ignore):
                if item.rect.collidepoint(pygame.mouse.get_pos()):
                    item.edit=not(item.edit)
                    if item.edit:
                        edting=m
                    ignore=True
                    n=0
                    for e in b:
                        if not(n==m):
                            e.edit=False
                        n+=1
            m+=1
            
        if not(ignore):
            for e in b:
                e.edit=False
                
    ld_r=right_click
    return ld_r,edting


def drag(b,down,holding,last_d,off):
    over=[]
    if down:
        #newer but slower
        #check what is holdable
        n=0
        for item in b:
            #print(item)
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                if item.edit:
                    over.append(n)
            n+=1
            
        #print(over)
        if len(over)>0:
            #survival of the original (holding is original)
            if holding==-1:
                holding=over[0]
                
            #actuall draging part
            item=b[holding]
            item.dragging=True
            mx,my=pygame.mouse.get_pos()
            diff=mx-off[0],my-off[1]
            item.x+=diff[0]+(item.w//2)
            item.y+=diff[1]+(item.h//2)
            if item.h_type=="text":
                item.w,item.h=item.textRect[2],item.textRect[3]
            item.x-=item.w//2
            item.y-=item.h//2
            item.rect=pygame.Rect((item.x,item.y),(item.w,item.h))                    
            if item.h_type=="text":
                item.textRect.center=item.x+(item.w//2),item.y+(item.h//2)
            b[holding]=item
            
        
        else:
            #if not overlapping then no holding
            holding=-1
            
    else:
        #if not pressing mouse 1 , set all elements as "i ain't dragging u bruh"
        holding=-1
        for item in b:
            item.dragging=False
                

    #if any element is on top of the UI , re-adjust it's position
    for item in b:
        if item.y<70:
            if (holding==-1):
                item.y=70+(item.h//2)
                item.x+=item.w//2
                if item.h_type=="text":
                    item.w,item.h=item.textRect[2],item.textRect[3]
                item.x-=item.w//2
                item.y-=item.h//2
                item.rect=pygame.Rect((item.x,item.y),(item.w,item.h))                    
                if item.h_type=="text":
                    item.textRect.center=item.x+(item.w//2),item.y+(item.h//2)
                
    return holding

buttons=[button(10,25,40,40,"text.png","text",colors),button(60,25,40,40,"add-image.png","image",colors)]         
b=[]
#0=x; 1=y;
ed=[edit_text(480,25,48,18,colors,"00") ,edit_text(480,45,48,18,colors,"00"),
    edit_text(612,25,90,18,colors,"text",e_type='text',overflow=True),
    edit_text(765,25,90,18,colors,"ubuntu-mono",e_type='text',overflow=True),
    edit_text(765,45,90,18,colors,"16",overflow=True)]

run=True
down=False
right_click=False
ld_r=False
ld_l=False
off=(0,0)
holding=-1
editing=None
keypress=None
sans16 = pygame.font.Font("ubuntu-mono.ttf",16)
sans32 = pygame.font.Font("ubuntu-mono.ttf",32)

while run:
    if True:
        #Background
        win.fill(colors[3])
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    down=True
                    ld_l=False
                if event.button==3:
                    right_click=True
            if event.type==pygame.MOUSEBUTTONUP:
                down=False
                right_click=False
                ld_l=True

            if event.type==pygame.KEYDOWN and (keypress==None):
                keypress=pygame.key.name(event.key)

            if event.type==pygame.KEYUP:
                keypress=None
            
                
        #Top Pannel
        pygame.draw.rect(win,colors[1],((0,0),(900,70)))
        pygame.draw.rect(win,colors[0],((450,4),(445,62)),2,10)
        draw_text(win,460,5,"Transforms",colors[3],sans16)
        draw_text(win,460,22,"x: ",colors[3],sans16)
        draw_text(win,460,40,"y: ",colors[3],sans16)

        if not(editing==None) and b[editing].h_type=='image':
            draw_text(win,560,22,"Image: ",colors[3],sans16)
            draw_text(win,710,22,"Width: ",colors[3],sans16)
            draw_text(win,710,40,"Height: ",colors[3],sans16)
        else:
            draw_text(win,560,22,"Text: ",colors[3],sans16)
            draw_text(win,710,22,"Font: ",colors[3],sans16)
            draw_text(win,710,40,"Size: ",colors[3],sans16)

        
        
        
        
        #left/right click checks
        holding=drag(b,down,holding,ld_l,off)
        ld_r,editing=edit_check(b,right_click,ld_r,editing)
        
        #drawing buttons
        for e in buttons:
            e.draw(win)
            if (holding==-1):
                a=e.press_check(down)
                if not(a==0):
                    b.append(a)
                    n=0
                    editing=len(b)-1
                    for c in b:
                        n+=1
                        if n<len(b):
                            c.edit=False
               
                        
        #drawing edit texts
        n=0
        for e in ed:
            e.edit_check(down,editing)
            if e.editing:
                e.edit(keypress,b)
                keypress=None
            e.draw(win,sans16,b,editing)
            n+=1

        a=0
        for e in b:
            if e.edit:
                a=1
        if a==0:
            editing=None
            
        #drawing added elements
        n=0
        for e in b:
            e.update(ed)
            e.draw(win)
            n+=1

        #update
        off=pygame.mouse.get_pos()
        pygame.display.update()

           
    '''except Exception as e:
        print(e)
    '''
code="<html style='margin:0;padding:0;'>"

code+="\n<style>"
for i in fonts:
    code+="@font-face {font-family:"+str(i[:-4])+";src: url("+str(i)+");}"
code+="</style>"

code+="\n<body style='margin:0;padding:0;'> \n"
for ele in b:
    if ele.h_type=="image":
        code+="<img style=' position:absolute; top:"+str(ele.y-70)+"; left:"+str(ele.x)+"px; ' src='"+ele.holding+"' width='"+str(ele.w)+"' height='"+str(ele.h)+"'> \n"

for ele in b:
    if ele.h_type=="text":
        code+="<h1 style='position:absolute; font-family:"+str(ele.font[:-4])+"; top:"+str(ele.y-70-(ele.h//2))+"; left:"+str(ele.x)+"; font-size:"+str(ele.f_size)+"px; '>"+ele.holding+"</h1> \n"

code+="</body> \n </html>"
print(code)

open('generated.html','w').write(code)
webbrowser.open('generated.html')
pygame.quit()
