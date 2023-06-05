from tkinter import filedialog
import tkinter as tk
from pygame.locals import *
import sys
import random
import pygame
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    initialdir=os.getcwd(), title="Select file")


class Camera:
    def __init__(self, x, y, distance, screen_width, screen_height, image_width, image_height):
        self.x = x
        self.y = y
        self.distance = distance
        self.dragging = False
        self.drag_start_pos = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image_width = image_width
        self.image_height = image_height
        self.update_distance()

    def update_distance(self):
        # Calculate the distance based on the screen and image dimensions
        screen_ratio = self.screen_width / self.screen_height
        image_ratio = self.image_width / self.image_height
        if screen_ratio > image_ratio:
            self.distance = self.screen_height / self.image_height
        else:
            self.distance = self.screen_width / self.image_width

    def apply(self, entity):
        # Apply camera translation and scaling to an entity
        entity_x = (entity[0] - self.x + self.screen_width /
                    (2 * self.distance)) * self.distance
        entity_y = (entity[1] - self.y + self.screen_height /
                    (2 * self.distance)) * self.distance
        return (entity_x, entity_y)

    def unapply(self, entity):
        # Reverse camera translation and scaling on an entity
        entity_x = (entity[0] / self.distance) - \
            self.screen_width / (2 * self.distance) + self.x
        entity_y = (entity[1] / self.distance) - \
            self.screen_height / (2 * self.distance) + self.y
        return (entity_x, entity_y)


class Sprite:
    def __init__(self, pos, radius, color, camera):
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
        self.camera = camera

    def draw(self):
        sprite_surface = pygame.Surface(
            (3 * self.radius, 3 * self.radius), pygame.SRCALPHA)
        ringsize = self.radius // 10

        pygame.draw.circle(sprite_surface, self.color,
                           (self.radius, self.radius), self.radius)
        if self.player:
            pygame.draw.circle(sprite_surface, (255, 255, 255),
                               (self.radius, self.radius), self.radius, width=ringsize)
        else:
            pygame.draw.circle(sprite_surface, (0, 0, 0),
                               (self.radius, self.radius), self.radius, width=ringsize)

        intext = self.letter

        if self.number:
            intext += str(self.number)

        # Adjust the scaling factor as desired
        text_font = pygame.font.Font(
            None, int(self.font_size * (self.radius / 20)))
        text_surface = text_font.render(self.letter, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.radius, self.radius))

        # Invert the color of the text
        text_surface = text_font.render(self.letter, True, (0, 0, 0))
        if self.dead:
            # Draw cross
            pygame.draw.line(sprite_surface, (0, 0, 0), (0, 0),
                             (2 * self.radius, 2 * self.radius), width=ringsize * 2)
            pygame.draw.line(sprite_surface, (0, 0, 0), (0, 2 *
                                                         self.radius), (2 * self.radius, 0), width=ringsize * 2)

        if self.prone:
            # Draw straight line under sprite
            pygame.draw.line(sprite_surface, (0, 0, 0), (0, 2 * self.radius),
                             (2 * self.radius, 2 * self.radius), width=self.radius // 5)
            pygame.draw.line(sprite_surface, (255, 255, 255), (0, 2 * self.radius),
                             (2 * self.radius, 2 * self.radius), width=self.radius // 10)

        if self.cursed:
            pygame.draw.circle(sprite_surface, (0, 255, 0),
                               (self.radius, self.radius), self.radius // 2)

        sprite_surface.blit(text_surface, text_rect)

        return sprite_surface

    def check_hover(self, pos):
        sprite_center = pygame.math.Vector2(
            self.pos[0] + self.radius, self.pos[1] + self.radius)
        translated_pos = self.camera.unapply(pos)
        if sprite_center.distance_to(pygame.math.Vector2(translated_pos)) <= self.radius:
            self.hovered = True
            print("Hovering over sprite")
        else:
            self.hovered = False

    def update_radius(self, delta):
        # Calculate the new radius
        new_radius = self.radius + delta

        # Calculate the difference between the new and old radius
        radius_diff = new_radius - self.radius

        # Update the sprite position to keep it centered
        self.pos = (
            self.pos[0] - radius_diff,
            self.pos[1] - radius_diff
        )

        # Update the radius
        self.radius = new_radius


class App:
    def __init__(self):
        pygame.init()
        self.background_image = pygame.image.load(file_path)

        infoObject = pygame.display.Info()
        self.monitor_width = infoObject.current_w
        self.monitor_height = infoObject.current_h

        x, y = self.background_image.get_size()
        self.aspect_ratio = x / y

        self.screen_height = int(self.monitor_height * 0.9)
        self.screen_width = int(self.screen_height * self.aspect_ratio)
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Add Movable Sprite")
        self.initial_screen_height = self.screen_height
        self.initial_screen_width = self.screen_width

        self.clock = pygame.time.Clock()

        self.sprites = []
        self.camera = Camera(
            x/2, y/2, 1.0, self.screen_width, self.screen_height, x, y)
        self.last_mouse_pos = None

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
        running = True
        sprite_radius = 20
        while running:
            self.screen.fill((255, 255, 255))
            image_scaled_size = (
                int(self.background_image.get_width() * self.camera.distance),
                int(self.background_image.get_height() * self.camera.distance)
            )
            image_scaled = pygame.transform.scale(
                self.background_image, image_scaled_size)
            image_pos = self.camera.apply((0, 0))
            self.screen.blit(image_scaled, image_pos)

            for sprite in self.sprites:
                surface = sprite.draw()
                sprite_scaled_size = (
                    int(surface.get_width() * self.camera.distance),
                    int(surface.get_height() * self.camera.distance)
                )
                surface_scaled = pygame.transform.scale(
                    surface, sprite_scaled_size)
                self.screen.blit(surface_scaled, self.camera.apply(sprite.pos))

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Update the screen and camera dimensions on window resize
                    self.screen_width, self.screen_height = event.size
                    self.screen = pygame.display.set_mode(
                        (self.screen_width, self.screen_height), pygame.RESIZABLE)
                    self.camera.screen_width = self.screen_width
                    self.camera.screen_height = self.screen_height

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("Left mouse button pressed at: ", event.pos)
                        translated_pos = self.camera.unapply(event.pos)
                        sprite_pos = translated_pos
                        sprite_color = (255, 0, 0)
                        clicked_sprite = None
                        for sprite in self.sprites:
                            if sprite.hovered:
                                clicked_sprite = sprite
                                clicked_sprite.dragging = True
                                break
                        if clicked_sprite is None:
                            sprite_pos = (
                                sprite_pos[0] - sprite_radius,
                                sprite_pos[1] - sprite_radius
                            )
                            new_sprite = Sprite(
                                sprite_pos, sprite_radius, sprite_color, self.camera)
                            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                                new_sprite.player = True
                                new_sprite.color = (0, 0, 255)
                            new_sprite.check_hover(event.pos)
                            new_sprite.dragging = True
                            self.sprites.append(new_sprite)
                            print("New sprite added at: ", sprite_pos)
                    elif event.button == 2:
                        print("Middle mouse button pressed at: ", translated_pos)
                        self.camera.dragging = True
                        self.camera.drag_start_pos = translated_pos
                    elif event.button == 3:
                        for sprite in self.sprites:
                            if sprite.hovered:
                                self.sprites.remove(sprite)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for sprite in self.sprites:
                            if sprite.dragging:
                                sprite.dragging = False
                    if event.button == 2:
                        self.camera.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    translated_pos = self.camera.unapply(event.pos)
                    self.last_mouse_pos = event.pos
                    if self.camera.dragging:
                        self.camera.x -= event.rel[0] / self.camera.distance
                        self.camera.y -= event.rel[1] / self.camera.distance
                        self.camera.drag_start_pos = translated_pos
                    for sprite in self.sprites:
                        if sprite.dragging:
                            sprite.pos = translated_pos[0] - \
                                sprite.radius, translated_pos[1] - \
                                sprite.radius
                        else:
                            sprite.check_hover(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key >= pygame.K_a and event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        hovered_sprite = None
                        for sprite in self.sprites:
                            if sprite.hovered:
                                hovered_sprite = sprite
                                break
                        if hovered_sprite is not None:
                            letter_in_use = True
                            number_in_use = True
                            number = 0
                            while letter_in_use:
                                letter_in_use = False
                                for sprite in self.sprites:
                                    if sprite.letter == letter and hovered_sprite.player == sprite.player:
                                        letter_in_use = True
                                        letter = chr(
                                            event.key).upper() + str(number)
                                        number += 1
                                        break
                            while number_in_use:
                                number_in_use = False
                                for sprite in self.sprites:
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

                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.camera.distance += delta / 20
                        if self.camera.distance < 0.1:
                            self.camera.distance = 0.1

                            if delta != 0 and self.last_mouse_pos:
                                mouse_x, mouse_y = self.last_mouse_pos
                                mouse_world_x, mouse_world_y = self.camera.unapply(
                                    (mouse_x, mouse_y))
                                camera_center_x = self.camera.x + \
                                    self.screen_width / \
                                    (2 * self.camera.distance)
                                camera_center_y = self.camera.y + \
                                    self.screen_height / \
                                    (2 * self.camera.distance)

                                # Calculate the difference between the current and new zoom levels
                                zoom_diff = self.camera.distance

                                # Adjust the camera position based on the zoom difference
                                self.camera.x -= (camera_center_x -
                                                  mouse_world_x) * zoom_diff
                                self.camera.y -= (camera_center_y -
                                                  mouse_world_y) * zoom_diff

                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        for sprite in self.sprites:
                            sprite.update_radius(delta)
                            sprite_radius = sprite.radius
                    else:
                        if len(self.sprites) > 0:
                            for sprite in self.sprites:
                                if sprite.hovered:
                                    sprite.update_radius(delta)
                                    sprite_radius = sprite.radius

        pygame.quit()


app = App()
app.run()
