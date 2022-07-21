import froggerlib
import pygame

STAGE1 = 10
STAGE2 = 5
ROAD1 = 9
ROAD2 = 8
ROAD3 = 7
ROAD4 = 6
WATER1 = 4
WATER2 = 3
WATER3 = 2
WATER4 = 1

HALF_GAP = 5
LANE_SIZE = 50
OBJECT_HEIGHT = 40
FROG_SPEED = 20

class Frogger:
    def __init__( self, width, height ):
        self.width = width
        self.height = height
        self.gameover = False
        x, y = width/2, STAGE1*LANE_SIZE+HALF_GAP
        
        self.obj_list = []
        self.left_vehicles = []
        self.right_vehicles = []
        self.grass = []
        self.homes = []
        
        self.frog = froggerlib.Frog(x, y, OBJECT_HEIGHT, 40, x, y, FROG_SPEED, LANE_SIZE, LANE_SIZE)
        
        self.stage1 = froggerlib.Stage(0, STAGE1*LANE_SIZE, width, LANE_SIZE*2)
        self.stage2 = froggerlib.Stage(0, STAGE2*LANE_SIZE, width, LANE_SIZE)
        
        self.road1 = froggerlib.Road(0, ROAD1*LANE_SIZE, width, LANE_SIZE)
        for i in range(2):
            self.left_vehicles.append(froggerlib.Car(i*width/2, ROAD1*LANE_SIZE+HALF_GAP, 60, OBJECT_HEIGHT, -width, ROAD1*LANE_SIZE+HALF_GAP, 20))
        
        self.road2 = froggerlib.Road(0, ROAD2*LANE_SIZE, width, LANE_SIZE)
        for i in range(2):
            self.right_vehicles.append(froggerlib.Dozer(-i*width/2, ROAD2*LANE_SIZE+HALF_GAP, 70, OBJECT_HEIGHT, width, ROAD2*LANE_SIZE+HALF_GAP, 10))
        
        self.road3 = froggerlib.Road(0, ROAD3*LANE_SIZE, width, LANE_SIZE)
        for i in range(2):
           self.left_vehicles.append(froggerlib.Car(i*width/2, ROAD3*LANE_SIZE+HALF_GAP, 40, OBJECT_HEIGHT, -width, ROAD3*LANE_SIZE+HALF_GAP, 15)) 
        
        self.road4 = froggerlib.Road(0, ROAD4*LANE_SIZE, width, LANE_SIZE)
        for i in range(2):
            self.right_vehicles.append(froggerlib.Truck(-i*width/2, ROAD4*LANE_SIZE+HALF_GAP, 100, OBJECT_HEIGHT, width, ROAD4*LANE_SIZE+HALF_GAP, 5))
        
        self.water1 = froggerlib.Water(0, WATER1*LANE_SIZE, width, LANE_SIZE)
        for i in range(2):
            self.left_vehicles.append(froggerlib.Log(i*width/2, WATER1*LANE_SIZE+HALF_GAP, 100, OBJECT_HEIGHT, -width, WATER1*LANE_SIZE+HALF_GAP, 8))
        
        self.water2 = froggerlib.Water(0, WATER2*LANE_SIZE, width, LANE_SIZE)
        for i in range(2):
            self.right_vehicles.append(froggerlib.Log(-i*width/2, WATER2*LANE_SIZE+HALF_GAP, 80, OBJECT_HEIGHT, width, WATER2*LANE_SIZE+HALF_GAP, 3))
        
        self.water3 = froggerlib.Water(0, WATER3*LANE_SIZE, width, LANE_SIZE)
        for i in range(2):
            self.left_vehicles.append(froggerlib.Log(i*width/2, WATER3*LANE_SIZE+HALF_GAP, 120, OBJECT_HEIGHT, -width, WATER3*LANE_SIZE+HALF_GAP, 7))
        
        self.water4 = froggerlib.Water(0, WATER4*LANE_SIZE, width, LANE_SIZE)
        for i in range(2):
            self.right_vehicles.append(froggerlib.Log(-i*width/2, WATER4*LANE_SIZE+HALF_GAP, 90, OBJECT_HEIGHT, width, WATER4*LANE_SIZE+HALF_GAP, 9))

        self.grass1 = froggerlib.Grass(0, 0, 100, LANE_SIZE)
        self.grass2 = froggerlib.Grass(200, 0, 100, LANE_SIZE)
        self.grass3 = froggerlib.Grass(400, 0, 100, LANE_SIZE)
        self.grass4 = froggerlib.Grass(600, 0, 100, LANE_SIZE)
        self.grass.append(self.grass1)
        self.grass.append(self.grass2)
        self.grass.append(self.grass3)
        self.grass.append(self.grass4)
        
        self.home1 = froggerlib.Home(100, 0, 100, LANE_SIZE)
        self.home2 = froggerlib.Home(300, 0, 100, LANE_SIZE)
        self.home3 = froggerlib.Home(500, 0, 100, LANE_SIZE)
        self.home4 = froggerlib.Home(700, 0, 100, LANE_SIZE)
        self.homes.append(self.home1)
        self.homes.append(self.home2)
        self.homes.append(self.home3)
        self.homes.append(self.home4)

        self.obj_list.append(self.frog)
        self.obj_list += self.left_vehicles
        self.obj_list += self.right_vehicles
        
        self.Font = pygame.font.SysFont("Arial", 150)
        
    def evolve( self, dt ):
        if self.gameover:#(first check that you do each frame)
            return
        
        for obj in self.obj_list:
            obj.move()
            if obj.supports(self.frog):
                self.gameover = False
        
        for left_vehicle in self.left_vehicles:
            if left_vehicle.atDesiredLocation():
                left_vehicle.setX(self.width - 1)
            if left_vehicle.hits(self.frog):
                self.gameover = True
                
        for right_vehicle in self.right_vehicles:
            if right_vehicle.atDesiredLocation():
                right_vehicle.setX(-self.width - 1)
            if right_vehicle.hits(self.frog):
                self.gameover = True

        if self.frog.outOfBounds( self.width, self.height ):
            self.gameover = True
            
        for grass in self.grass:
            if grass.hits(self.frog):
                self.gameover = True
    
        if self.water1.hits(self.frog):
            self.gameover = True
        if self.water2.hits(self.frog):
            self.gameover = True
        if self.water3.hits(self.frog):
            self.gameover = True
        if self.water4.hits(self.frog):
            self.gameover = True
        return
    
    def draw( self, surface ):
        #Draw the stages
        self.draw_rect(surface, self.stage1, (170, 100, 170))
        self.draw_rect(surface, self.stage2, (170, 100, 170))
        
        #Draw roads
        self.draw_rect(surface, self.road1, (100, 100, 100))
        self.draw_rect(surface, self.road2, (150, 150, 150))
        self.draw_rect(surface, self.road3, (100, 100, 100))
        self.draw_rect(surface, self.road4, (150, 150, 150))
            
        #Draw water lanes
        self.draw_rect(surface, self.water1, (0, 0, 255))
        self.draw_rect(surface, self.water2, (0, 0, 200))
        self.draw_rect(surface, self.water3, (0, 0, 255))
        self.draw_rect(surface, self.water4, (0, 0, 200))
        
        #Draw grass
        for grass in self.grass:
            self.draw_rect(surface, grass, (0, 200, 0))
            
        #Draw homes
        for home in self.homes:
            self.draw_rect(surface, home, (50, 0, 100))
        
        #Draw left vehicles
        for vehicle in self.left_vehicles:
            if type(vehicle) == froggerlib.Log:
                self.draw_rect(surface, vehicle, (94, 45, 12))
            elif type(vehicle) == froggerlib.Car:
                self.draw_rect(surface, vehicle, (90, 100, 255))
            else:
                self.draw_rect(surface, vehicle, (0, 200, 50))
        
        #Draw right vehicles
        for vehicle in self.right_vehicles:
            if type(vehicle) == froggerlib.Log:
                self.draw_rect(surface, vehicle, (94, 45, 12))
            elif type(vehicle) == froggerlib.Dozer:
                self.draw_rect(surface, vehicle, (255, 80, 20))
            else:
                self.draw_rect(surface, vehicle, (100, 180, 50))

        #Draw the frog
        self.draw_rect(surface, self.frog, (0, 255, 0))
        
        #Win text
        for home in self.homes:
            if home.hits(self.frog):
                self.text(surface, 'You Win!', (255,0,0))
                self.gameover = True
        return
                
    def act_on_pressUP( self ):
        self.frog.up()
        return
        
    def act_on_pressDOWN( self ):
        self.frog.down()
        return
    
    def act_on_pressLEFT( self ):
        self.frog.left()
        return
    
    def act_on_pressRIGHT( self ):
        self.frog.right()
        return
    
    def draw_rect(self, surface, obj, color):
        rect = pygame.Rect(int(obj.getX()), int(obj.getY()), int(obj.getWidth()), int(obj.getHeight()))
        pygame.draw.rect(surface, color, rect)
        return
    
    def text(self, surface, text, color):
        text_object = self.Font.render(text, True, color)
        text_rect = text_object.get_rect()
        text_rect.center = (self.width//2, self.height//2)
        surface.blit(text_object, text_rect)
        return