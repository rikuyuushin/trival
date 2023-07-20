import sys
import pygame
import requests
from pygame.locals import *
import random


def print_text(font, x, y, text, color=(255, 255, 255), shadow=True):
    if shadow:
        imgText = font.render(text, True, (0, 0, 0))
        screen.blit(imgText, (x - 2, y - 2))
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


class Trivia(object):
    def __init__(self):
        self.current = 0
        self.correct = 0
        self.score = 0
        self.scored = False
        self.failed = False
        self.wronganswer = 0
        self.colors = [white, white, white, white]
        self.questions = []

        response = requests.get('https://the-trivia-api.com/v2/questions')
        if response.status_code == 200:
            data = response.json()
            for i in range(10):
                question_data = data[i]
                question = question_data['question']['text']
                choices = [question_data['correctAnswer']] + question_data['incorrectAnswers']
                self.questions.append((question, choices))
        else:
            print('Failed to fetch trivia questions from the API.')

        self.total = len(self.questions) * 6
        self.generate_question()

    def generate_question(self):
        self.question, self.choices = self.questions[self.current // 6]
        random.shuffle(self.choices)
        self.correct = random.choice(range(1, 5))

    def show_question(self):
        print_text(font1, 210, 5, "TRIVIA GAME")
        print_text(font2, 190, 500 - 20, "Press Keys (1-4) to Answer", purple)
        print_text(font2, 530, 5, "SCORE", purple)
        print_text(font2, 550, 25, str(self.score), purple)

        question_num = self.current // 6 + 1
        print_text(font1, 5, 80, "QUESTION " + str(question_num))
        print_text(font2, 20, 120, self.question, yellow)

        if self.scored:
            self.colors = [white, white, white, white]
            self.colors[self.correct - 1] = green
            print_text(font1, 230, 380, "CORRECT!", green)
            if self.current >= self.total - 6:
                print_text(font2, 280, 420, "QUIT (q)?", yellow)
            else:
                print_text(font2, 170, 420, "Press Enter For Next Question", green)
        elif self.failed:
            self.colors = [white, white, white, white]
            self.colors[self.wronganswer - 1] = red
            self.colors[self.correct - 1] = green
            print_text(font1, 220, 380, "INCORRECT!", red)
            if self.current >= self.total - 6:
                print_text(font2, 280, 420, "QUIT (q)?", yellow)
            else:
                print_text(font2, 170, 420, "Press Enter For Next Question", red)

        print_text(font1, 5, 170, "Answers")
        print_text(font2, 20, 210, "1 - " + self.choices[0], self.colors[0])
        print_text(font2, 20, 240, "2 - " + self.choices[1], self.colors[1])
        print_text(font2, 20, 270, "3 - " + self.choices[2], self.colors[2])
        print_text(font2, 20, 300, "4 - " + self.choices[3], self.colors[3])

    def next_question(self):
        if self.scored or self.failed:
            self.scored = False
            self.failed = False
            self.correct = 0
            self.colors = [white, white, white, white]
            self.current += 6
            if self.current >= self.total:
                print_text(font1, 240, 380, "Final Score: " + str(self.score), cyan)
                pygame.display.update()
                pygame.time.wait(3000)
                sys.exit()
            self.generate_question()

    def handle_input(self, number):
        if not self.scored and not self.failed:
            if number == self.correct:
                self.scored = True
                self.score += 1
            else:
                self.failed = True
                self.wronganswer = number


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("The Trivia Game")
    font1 = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 24)
    white = 255, 255, 255
    cyan = 0, 255, 255
    yellow = 255, 255, 0
    purple = 255, 0, 255
    green = 0, 255, 0
    red = 255, 0, 0

    trivia = Trivia()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_1:
                    trivia.handle_input(1)
                elif event.key == pygame.K_2:
                    trivia.handle_input(2)
                elif event.key == pygame.K_3:
                    trivia.handle_input(3)
                elif event.key == pygame.K_4:
                    trivia.handle_input(4)
                elif event.key == pygame.K_RETURN:
                    trivia.next_question()
                elif event.key == pygame.K_q:
                    sys.exit()

        screen.fill((0, 0, 200))
        trivia.show_question()
        pygame.display.update()




