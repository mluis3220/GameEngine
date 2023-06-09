import pygame

pygame.init()

#Screen Size
width = 640
height = 480
#Store Screen Size
z = [width, height]
#Screen Attributes
TITLE = "GAME ENGINE"
screen_display = pygame.display
surface = screen_display.set_mode(z)

bg_img = pygame.image.load('city.png')
bg_img = pygame.transform.scale(bg_img,(width,height))


#Timer
clock = pygame.time.Clock()
#Colors
white = (255, 255, 255)
black = (0,0,0)
#Font
TITLE_FONT = None
DEFAULT_FONT = None
# Load assets
font_sm = pygame.font.Font(DEFAULT_FONT, 24)
font_md = pygame.font.Font(DEFAULT_FONT, 24)
font_xl = pygame.font.Font(TITLE_FONT, 24)


#Sprite Class
class Player(pygame.sprite.Sprite):
    def __init__(self, img_path, position_x, position_y):
        #load image from requested destination
        self.image = pygame.Surface((0,0))
        self.image = pygame.image.load(img_path).convert()
        #Place Rect over image 
        self.rect = self.image.get_rect()
        #Set rectangle coordinates
        self.rect.centerx = position_x
        self.rect.centery = position_y
      
    #Set the size of the rectangle  
    def setImageSize(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect.width = width
        self.rect.height = height

    #Set the dx and dy values
    def setDxDy(self, dx, dy):
        self.dx = dx
        self.dy = dy

    #Update rect position
    def update(self):
        #Update rect according to dx & dy values
        self.rect.centerx += self.dx
        if self.rect.right > surface.get_width():
            self.rect.left = 0

    #Draw image to screen
    def drawRect(self, surface):
        surface.blit(self.image, (self.rect.centerx, self.rect.centery))

    #Set image angle
    def setImgAngle(self, angle):
      self.image = pygame.transform.rotate(self.image, angle)

    #Check if two sprites collide with each other
    def checkCollision(self, object1, object2):
      collide = pygame.Rect.colliderect(object1, object2)
      if(collide):
        collision = True
        
player = Player('superdog.png', 200, 200)
player.setImageSize(25,25)
player.setDxDy(10, 0)
player.setImgAngle(180)
player.drawRect(surface)




# Scenes
class Scene():
  def __init__(self):
    self.next_scene = self
  
  def process_input(self, events, pressed_keys):
    raise NotImplementedError
    
  def update(self):
    raise NotImplementedError
    
  def render(self):
    raise NotImplementedError

  def terminate(self):
    self.next_scene = None


class TitleScene(Scene):
  def __init__(self):
    super().__init__()
  
  def process_input(self, events, pressed_keys):
    for event in events:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          self.next_scene = PlayScene()
    
  def update(self):
    pass
    
  def render(self):
    surface.fill((0,0,0))
    text = font_xl.render(TITLE, 1, white)
    rect = text.get_rect()
    rect.centerx = width // 2
    rect.centery = height // 2
    surface.blit(text, rect)


class PlayScene(Scene):
  def __init__(self):
    super().__init__()
   
  def process_input(self, events, pressed_keys):
    for event in events:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          self.next_scene = EndScene()
    
  def update(self):
    pass
    
  def render(self):
    surface.fill(black)
    text = font_xl.render("Playing", 1, white)
    rect = text.get_rect()
    rect.centerx = width // 2
    rect.centery = height // 2
    surface.blit(text, rect)


class EndScene(Scene):
  def __init__(self):
    super().__init__()

  def process_input(self, events, pressed_keys):
    for event in events:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          self.next_scene = TitleScene()
    
  def update(self):
    pass
    
  def render(self):
    surface.fill(black)
    text = font_xl.render("Game Over", 1, white)
    rect = text.get_rect()
    rect.centerx = width // 2
    rect.centery = height // 2
    surface.blit(text, rect)

# Main game class
class Game():
  def __init__(self):
    self.active_scene = TitleScene()
   
  def is_quit_event(self, event, pressed_keys):
    x_out = event.type == pygame.QUIT
    ctrl = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
    q = pressed_keys[pygame.K_q]

    return x_out or (ctrl and q)
  def run(self): 
      while self.active_scene != None:
          # Get user input
          pressed_keys = pygame.key.get_pressed()
          filtered_events = []

          for event in pygame.event.get():
              if self.is_quit_event(event, pressed_keys):
                  self.active_scene.terminate()
              else:
                  filtered_events.append(event)

          # Manage scene
          self.active_scene.process_input(filtered_events, pressed_keys)
          self.active_scene.update()
          self.active_scene.render()
          self.active_scene = self.active_scene.next_scene


        
  
player = Player('superdog.png', 200, 200)
player.setImageSize(50,50)
player.setDxDy(10, 0)
player.setImgAngle(180)
player.drawRect(surface)
window = True
while window:
  surface.blit(bg_img,(0,0))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      window = False
      
  player.drawRect(surface)
  player.setDxDy(10, 0)
  player.update()
  # draw on image onto another
  screen_display.update()
  clock.tick(25)

pygame.quit()



