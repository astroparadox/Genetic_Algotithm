import pygame
import random
import math

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1350, 650
MAX_SPEED = 10
GENERATION_SIZE = 30
CHANGE_DIRECTION_INTERVAL = 20  #change direction every 30 frames

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Evolution Simulation")

class Creature:
    def __init__(self, x, y):
        self.alive = True
        self.x = x
        self.y = y
        self.speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
        self.speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
        self.agility = random.uniform(1, 5)
        self.age = random.randint(5, 50)
        self.spikes = random.choice([0, 1])
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.frames_until_direction_change = random.randint(0, CHANGE_DIRECTION_INTERVAL)

    def draw(self):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 5)
        if self.spikes:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 7, 2)
        if not self.alive:
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 5)
        font = pygame.font.Font(None, 12)
        text = font.render(f"AvgSpeed: {abs((self.speed_x + self.speed_y) / 2):.2f}, Agility: {abs(self.agility):.2f}", True, (255, 255, 255))
        screen.blit(text, (self.rect.x - 60, self.rect.y - 25))

    def move(self):
        self.frames_until_direction_change -= 1
        if self.frames_until_direction_change <= 0:
            self.speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
            self.speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
            self.frames_until_direction_change = random.randint(0, CHANGE_DIRECTION_INTERVAL)

        self.x += self.speed_x
        self.y += self.speed_y
        self.age -= 1
        self.rect.x = self.x
        self.rect.y = self.y

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

        if self.age == 0:
            self.alive = False
            self.age = random.randint(5, 30)

creatures = [Creature(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(GENERATION_SIZE)]

def fitness(creature):
    return creature.agility + creature.spikes + creature.speed_y + creature.speed_x

def evolve(creatures, mutation_rate=0.1, crossover_rate=0.5):
    creatures.sort(key=fitness, reverse=True)
    top_performers = int(len(creatures) * 0.2)
    creatures = creatures[:top_performers]

    new_creatures = []
    while len(new_creatures) < GENERATION_SIZE:
        parent1 = random.choice(creatures)
        parent2 = random.choice(creatures)

        if random.random() < crossover_rate:
            child = Creature(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            child.speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
            child.speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
            child.agility = parent2.agility
            child.age = parent2.age
            child.spikes = parent2.spikes
        else:
            child = Creature(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            child.speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
            child.speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
            child.agility = parent1.agility
            child.age = parent1.age
            child.spikes = parent1.spikes

        if random.random() < mutation_rate:
            child.agility += random.uniform(-1, 1)
            child.age += random.randint(-1, 1)
            child.spikes = 1 - child.spikes

        new_creatures.append(child)

    return new_creatures

running = True
generation_count = 1
score = 0
average_speed = 0
spike_percentage = 0
num_spikes = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for creature in creatures:
        if creature.alive:
            creature.move()

    if all(not creature.alive for creature in creatures):
        generation_count += 1
        creatures = evolve(creatures)
        for creature in creatures:
            score += (creature.agility / GENERATION_SIZE)
            average_speed += abs(((creature.speed_x + creature.speed_y) / 2) / GENERATION_SIZE)
            if creature.spikes == 1:
                num_spikes += 1
        spike_percentage = (num_spikes / GENERATION_SIZE) * 100
        num_spikes = 0
        pygame.time.wait(1000)

    screen.fill((0, 0, 0))
    for creature in creatures:
        creature.draw()
        font = pygame.font.Font(None, 30)
        text1 = font.render(f"Generation: {generation_count}", True, (0, 255, 255))
        text2 = font.render(f"Average Pop Speed: {round(average_speed, 2):.2f}", True, (0, 255, 255))
        text3 = font.render(f"Spike %: {spike_percentage:.2f}", True, (0, 255, 255))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 30))
        screen.blit(text3, (10, 50))
    pygame.display.update()
    pygame.time.wait(100)

pygame.quit()