import random
import sys
import time
import pygame
from point import Point
from configs import (
    WIDTH,
    HEIGHT,
    BLOCK_SIZE,
    OBSTACLE_THRESHOLD,
    FIXED_AUTO_SPEED,
)
from colors import WHITE, RED, BLUE, GREEN, BLACK
from directions import Direction


class Game:
    def __init__(self, game_has_obstacles=False, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.direction = Direction.UP
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head]
        self.score = 0
        self.game_has_obstacles = game_has_obstacles
        self.obstacles = []
        self.food = None
        self.path = []

        # Pygame initializations
        self.display = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("arial", 25)
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        pygame.display.set_caption("Snake Game")

        # Initialize obstacles
        self.generate_obstacles()
        # Initialize food point
        self.generate_food()

    def reset(self):
        """
        Completely resets the game back to the initial starting point
        """
        self.direction = Direction.UP
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles = []
        self.food = None
        self.generate_obstacles()
        self.generate_food()

    def generate_food(self):
        """
        Randomly generates a food Point in the game.
        Ensures that obstacles and the snake are avoided in the process.
        """
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake or self.food in self.obstacles:
            self.generate_food()

    def generate_obstacles(self):
        """
        Randomly generates obstacles in the game.
        Ensures that the snake is avoided in the process.
        """
        if self.game_has_obstacles:
            for _ in range(0, OBSTACLE_THRESHOLD):
                x = (
                    random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE)
                    * BLOCK_SIZE
                )
                y = (
                    random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE)
                    * BLOCK_SIZE
                )
                obstacle = Point(x, y)
                if obstacle not in self.snake:
                    self.obstacles.append(obstacle)

    def get_next_head(self, direction):
        """
        Returns a point at which the snake's head should move next based on the given direction
        """
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        return Point(x, y)

    def detect_collision(self):
        """
        Checks if the snake has collided with any of the following entities:
        - Boundary of the game
        - The snake itself
        - Any obstacles in the game
        """
        if (
            self.head.x > self.width - BLOCK_SIZE
            or self.head.x < 0
            or self.head.y > self.height - BLOCK_SIZE
            or self.head.y < 0
        ):
            return True
        if self.head in self.snake[1:]:
            return True
        if self.head in self.obstacles:
            return True

    def detect_random_point_collision(self, next_head):
        """
        Checks if the given point collides with any of the following entities:
        - Boundary of the game
        - The snake itself
        - Any obstacles in the game

        Note: Here we assume that the random point is the next head.
        """
        if (
            next_head.x > self.width - BLOCK_SIZE
            or next_head.x < 0
            or next_head.y > self.height - BLOCK_SIZE
            or next_head.y < 0
        ):
            return True
        # Exclude the tail of the snake as we assume that it has moved by a point
        if next_head in self.snake[:-1]:
            return True
        if next_head in self.obstacles:
            return True

    def update_ui(self):
        """
        Updates the game's UI by plotting the following entities on the display window:
        - The snake's body
        - The snake's head
        - Obstacles
        - Food source
        - Current score
        """
        self.display.fill(BLACK)
        for point in self.snake:
            point.plot(self.display, GREEN)
        self.head.plot(self.display, WHITE)
        for point in self.obstacles:
            point.plot(self.display, BLUE)
        self.food.plot(self.display, RED)
        text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        # Draw elapsed time
        elapsed_time = pygame.time.get_ticks() // 1000  # Convert milliseconds to seconds
        time_text = self.font.render("Time: " + str(elapsed_time) + "s", True, WHITE)
        self.display.blit(time_text, [0, 30])
        pygame.display.flip()

    def display_game_over(self):
        """
        Display "Game Over" and the final score on the screen.
        Wait for the user to close the window.
        """
        game_over_time = pygame.time.get_ticks() - self.start_time
        total_time_seconds = game_over_time // 1000  # Convert milliseconds to seconds

        large_font = pygame.font.SysFont("arial", 40)  # Choose a larger font size

        game_over_text = large_font.render("Game Over", True, WHITE)
        score_text = large_font.render("Final Score: " + str(self.score), True, WHITE)
        time_text = large_font.render("Total Time: " + str(total_time_seconds) + "s", True, WHITE)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.display.fill((251, 252, 215))
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 30))
            self.display.blit(game_over_text, text_rect)

            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 30))
            self.display.blit(score_text, score_rect)

            time_rect = time_text.get_rect(center=(self.width // 2, self.height // 2 + 90))
            self.display.blit(time_text, time_rect)

            pygame.display.flip()

            # Introduce a slight delay to reduce CPU usage
            pygame.time.delay(100)


    def generate_path(self):
        """
        Core function that is redefined for each algorithm to generate
        the path on which the snake will traverse.
        """
        pass

    def single_step_traversal(self):
        """
        Executes traversal of the snake for algorithms where the snake's
        moves are evaluated step by step, one at a time.
        """
        while True:
            # Check user input
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    # self.display_game_over()

            # Set movement of snake
            self.direction = self.generate_path()
            if not self.direction:
                return self.score

            # Move snake
            self.head = self.get_next_head(self.direction)
            self.snake.insert(0, self.head)

            # Check if the snake has collided with something
            if self.detect_collision():
                return self.score
            # Check if snake has reached the food point
            elif self.head == self.food:
                self.score += 1
                self.generate_food()
            else:
                # Remove the last element from the snake's body as we have added a new head
                self.snake.pop()

            # Update UI and Clock
            self.update_ui()
            self.clock.tick(FIXED_AUTO_SPEED)


    def multi_step_traversal(self):
        """
        Executes traversal of the snake for algorithms where the complete path
        of the snake's movement is evaluated all at once.
        """
        while self.path:
            # check user input
            for event in pygame.event.get():
                # quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
            # move snake
            self.direction = self.path.pop(-1).get_direction()
            self.head = self.get_next_head(self.direction)
            self.snake.insert(0, self.head)

            # check if the snake has collided with something
            if self.detect_collision():
                return self.score
            # check if snake has reached the food point and generate path to this new point
            elif self.head == self.food:
                self.score += 1
                self.generate_food()
                self.generate_path()
            else:
                # remove the last element from the snake's body as we have added a new head
                self.snake.pop()

            # update UI and Clock
            self.update_ui()
            self.clock.tick(FIXED_AUTO_SPEED)
        return self.display_game_over()


    def main(self):
        """
        Wrapper function that is redefined for each algorithm to execute - single or
        multi step traversal based on the type of path generated by the algorithm.
        """
        pass