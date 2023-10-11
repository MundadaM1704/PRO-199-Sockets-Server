import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
questions = ["In which field, Oscar awards are distributed? \n A.Sports\n B.Cinema\n C.Studies\n D.Technology",
             "Which one of the following river flows between Vindhyan and Satpura ranges? \n A.Narmada\n B.Mahanadi\n C.Son\n D.Netravati",
             "Who among the following wrote Sanskrit grammar? \n A.Kalidasa\n B.Charak\n C.Panini\n D.Aryabhatt",
             "The metal whose salts are sensitive to light is? \n A.Zinc\n B.Silver\n C.Copper\n D.Aluminum",
             "The hottest planet in the solar system? \n A.Mercury\n B.Jupiter\n C.Mars\n D.Venus"]
answers = ['B','A','C','B','D']

print("Quiz has started..")

def clientthread(conn):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one a, b, c or d\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time! :)\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

def get_random_question_answer(conn):
    random_index = random.randint(0, len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()
