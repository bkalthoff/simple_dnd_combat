import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import sys


import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",)

class Sprite:
    def __init__(self, pos, radius, color):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.dragging = False
        self.hovered = False
        self.player = False
        self.letter = ""
        self.number = None
        self.font_size = 30
        self.font = pygame.font.Font(None, self.font_size)
        self.prone = False
        self.dead = False
        self.cursed = False

    def draw(self, screen):
        ringsize = self.radius // 10
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        if self.player:
            pygame.draw.circle(screen, (255, 255, 255), self.pos, self.radius, width=ringsize)
        else:
            pygame.draw.circle(screen, (0, 0, 0), self.pos, self.radius, width=ringsize)

        intext = self.letter

        if self.number:
            intext += str(self.number)

        text_font = pygame.font.Font(None, int(self.font_size * (self.radius / 20)))  # Adjust the scaling factor as desired
        text_surface = text_font.render(self.letter, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.pos)

        # Invert the color of the text
        inverted_color = (255 - self.color[0], 255 - self.color[1], 255 - self.color[2])
        inverted_text_surface = text_font.render(self.letter, True, inverted_color)
        if self.dead:
            #draw cross
            pygame.draw.line(screen, (0, 0, 0), (self.pos[0] - self.radius, self.pos[1] - self.radius), (self.pos[0] + self.radius, self.pos[1] + self.radius), width=ringsize*2)
            pygame.draw.line(screen, (0, 0, 0), (self.pos[0] - self.radius, self.pos[1] + self.radius), (self.pos[0] + self.radius, self.pos[1] - self.radius), width=ringsize*2)

        if self.prone:
            #draw straight line under sprite
            pygame.draw.line(screen, (0, 0, 0), (self.pos[0] - self.radius, self.pos[1] + self.radius), (self.pos[0] + self.radius, self.pos[1] + self.radius), width=self.radius // 5)
            pygame.draw.line(screen, (255, 255, 255), (self.pos[0] - self.radius, self.pos[1] + self.radius), (self.pos[0] + self.radius, self.pos[1] + self.radius), width=self.radius // 10)

        if self.cursed:
            pygame.draw.circle(screen, (255, 0, 255), self.pos, self.radius + ringsize, width=ringsize)


        screen.blit(inverted_text_surface, text_rect)

    def check_hover(self, event):
        sprite_center = pygame.math.Vector2(self.pos)
        if sprite_center.distance_to(pygame.math.Vector2(event.pos)) <= self.radius:
            self.hovered = True
        else:
            self.hovered = False
    def update_radius(self, delta):
        self.radius += delta

class App:
    def __init__(self):
        pygame.init()
        self.background_image = pygame.image.load(file_path)
        self.background_rect = self.background_image.get_rect()
        #get monitor size
        infoObject = pygame.display.Info()
        self.monitor_width = infoObject.current_w
        self.monitor_height = infoObject.current_h
        #get size of background image
        x, y = self.background_image.get_size()
        #get aspect ratio of background image
        self.aspect_ratio = x / y
        #set initial screen size
        # Set up the display


        #if height is greater, set screen height to 80% of monitor height
        self.screen_height = int(self.monitor_height * 0.9)
        #set screen width to 80% of screen height
        self.screen_width = int(self.screen_height * self.aspect_ratio)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Add Movable Sprite")
        self.initial_screen_height = self.screen_height
        self.initial_screen_width = self.screen_width

        self.clock = pygame.time.Clock()

        # Load the background image

        # Initialize the sprite list
        self.sprites = []


    def update_sprite_positions(self):
        width_ratio = self.screen_width / self.initial_screen_width
        height_ratio = self.screen_height / self.initial_screen_height

        for sprite in self.sprites:
            sprite.pos = (
                int(sprite.pos[0] * width_ratio),
                int(sprite.pos[1] * height_ratio)
            )
            sprite.radius = sprite.radius * width_ratio
        self.initial_screen_width = self.screen_width
        self.initial_screen_height = self.screen_height

    def run(self):
        # Game loop
        running = True
        sprite_radius = 20
        while running:
            self.screen.fill((255, 255, 255))
            # Draw the background
            resized_background = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
            self.screen.blit(resized_background, (0, 0))

            # Draw the sprites
            for sprite in self.sprites:
                sprite.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left-click to add or start dragging a sprite
                        sprite_pos = event.pos
                        sprite_color = (255, 0, 0)
                        clicked_sprite = None
                        for sprite in self.sprites:
                            sprite_center = pygame.math.Vector2(sprite.pos)
                            if sprite_center.distance_to(pygame.math.Vector2(event.pos)) <= sprite.radius:
                                clicked_sprite = sprite
                                clicked_sprite.dragging = True
                                break
                        if clicked_sprite is None:
                            new_sprite = Sprite(sprite_pos, sprite_radius, sprite_color)
                            if pygame.key.get_mods() & pygame.KMOD_CTRL:  # Check if Ctrl key is pressed
                                new_sprite.player = True
                                new_sprite.color = (0, 0, 255)
                            new_sprite.check_hover(event)
                            new_sprite.dragging = True
                            self.sprites.append(new_sprite)
                    elif event.button == 3:  # Right-click to remove a sprite
                        for sprite in self.sprites:
                            sprite_center = pygame.math.Vector2(sprite.pos)
                            if sprite_center.distance_to(pygame.math.Vector2(event.pos)) <= sprite.radius:
                                self.sprites.remove(sprite)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left-click release to stop dragging
                        for sprite in self.sprites:
                            if sprite.dragging:
                                sprite.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    for sprite in self.sprites:
                        if sprite.dragging:
                            sprite.pos = event.pos
                        else:
                            sprite.check_hover(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key >= pygame.K_a and event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        hovered_sprite = None
                        for sprite in self.sprites:
                            if sprite.hovered:
                                hovered_sprite = sprite
                                break
                        # check if letter is already in use
                        # if letter is in use add a number to the end of it
                        # if letter and number is in use add another incrementing number to the end of it
                        # repeat until letter and number combination is unique
                        if hovered_sprite is not None:
                            letter_in_use = True
                            number_in_use = True
                            number = 0
                            while letter_in_use:
                                letter_in_use = False
                                for sprite in self.sprites:
                                    if sprite.letter == letter and hovered_sprite.player == sprite.player:
                                        letter_in_use = True
                                        letter = chr(event.key).upper() + str(number)
                                        number += 1
                                        break
                            while number_in_use:
                                number_in_use = False
                                for sprite in self.sprites :
                                    if sprite.number == number and hovered_sprite.player == sprite.player:
                                        number_in_use = True
                                        number += 1
                                        break
                            hovered_sprite.letter = letter
                            hovered_sprite.number = number
                    if event.key == pygame.K_DELETE:
                        for sprite in self.sprites:
                            if sprite.hovered:
                                sprite.dead = not sprite.dead
                    if event.key == pygame.K_1:
                        for sprite in self.sprites:
                            if sprite.hovered:
                                sprite.prone = not sprite.prone
                    if event.key == pygame.K_2:
                        for sprite in self.sprites:
                            if sprite.hovered:
                                sprite.cursed = not sprite.cursed


                elif event.type == pygame.MOUSEWHEEL:
                    delta = event.y
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:  # Check if Ctrl key is pressed
                        for sprite in self.sprites:
                            sprite.update_radius(delta)
                            sprite_radius = sprite.radius
                    else:
                        if len(self.sprites) > 0:
                            for sprite in self.sprites:
                                if sprite.hovered:
                                    sprite.update_radius(delta)
                                    sprite_radius = sprite.radius
                elif event.type == pygame.VIDEORESIZE:
                    self.screen_width = event.w
                    self.screen_height = event.h
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                    self.update_sprite_positions()

        pygame.quit()

app = App()
app.run()
