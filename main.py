import cv2
import numpy as np
import sqlite3
import os

# Conectar ao banco de dados SQLite (ou criar se não existir)
conn = sqlite3.connect('face_recognition.db')
cursor = conn.cursor()

# Criar a tabela para armazenar os dados faciais
cursor.execute('''
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    face_id INTEGER NOT NULL
)
''')
conn.commit()

# Inicializar o reconhecedor facial e o classificador de cascata
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Criar a pasta faces se não existir
if not os.path.exists('faces'):
    os.makedirs('faces')

def carregar_rostos():
    cursor.execute('SELECT name, face_id FROM faces')
    rostos = cursor.fetchall()
    nomes = []
    ids = []
    for rosto in rostos:
        nomes.append(rosto[0])
        ids.append(rosto[1])
    return nomes, ids

def salvar_rosto(nome, face_id):
    cursor.execute('INSERT INTO faces (name, face_id) VALUES (?, ?)', (nome, face_id))
    conn.commit()

def treinar_modelo():
    face_samples = []
    face_ids = []
    nomes, ids = carregar_rostos()
    for i, face_id in enumerate(ids):
        caminho = f'faces/user.{face_id}.jpg'
        if os.path.exists(caminho):
            imagem = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
            face_samples.append(imagem)
            face_ids.append(face_id)
    
    if face_samples:
        face_recognizer.train(face_samples, np.array(face_ids))
        face_recognizer.write('face_trainer.yml')

def registrar_rosto():
    nome = input("Digite o nome da pessoa: ")
    if not nome:
        print("Erro: Nome não pode estar vazio!")
        return
    
    cursor.execute('SELECT MAX(face_id) FROM faces')
    result = cursor.fetchone()
    novo_id = 1 if result[0] is None else result[0] + 1

    webcam = cv2.VideoCapture(0)
    print("Capturando rosto. Pressione 's' para salvar e sair.")
    i = 0
    while i < 10:
        verificacao, frame = webcam.read()
        if not verificacao:
            print("Erro ao acessar a câmera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostos = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in rostos:
            cv2.imwrite(f"faces/user.{novo_id}.jpg", gray[y:y+h, x:x+w])
            salvar_rosto(nome, novo_id)
            print(f"Rosto de {nome} salvo com sucesso!")
            treinar_modelo()
            i += 1
            print(i)  # Aqui você imprime o valor de i após o incremento

        cv2.imshow("Registrar Rosto", frame)
        if cv2.waitKey(7) & 0xFF == ord('s'):
            break

    webcam.release()
    cv2.destroyAllWindows()

def reconhecimento_facial():
    if not os.path.exists('face_trainer.yml'):
        print("Nenhum rosto registrado para reconhecimento.")
        return
    
    face_recognizer.read('face_trainer.yml')
    nomes_salvos, _ = carregar_rostos()
    
    webcam = cv2.VideoCapture(0)
    print("Pressione 'ESC' para sair.")

    while True:
        verificacao, frame = webcam.read()
        if not verificacao:
            print("Erro ao acessar a câmera.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostos = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in rostos:
            id, confianca = face_recognizer.predict(gray[y:y+h, x:x+w])
            if confianca < 100:
                cursor.execute('SELECT name FROM faces WHERE face_id = ?', (id,))
                result = cursor.fetchone()
                if result:
                    nome = result[0]
                    confianca_txt = f"{round(100 - confianca)}%"
                    print(f"Nome: {nome}, Confiança: {confianca_txt}")
            else:
                print("Rosto não reconhecido")
        
        cv2.imshow("Reconhecimento Facial", frame)
        if cv2.waitKey(4) == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()

# Menu principal
def menu():
    while True:
        print("\nSistema de Reconhecimento Facial")
        print("1. Registrar Rosto")
        print("2. Reconhecimento Facial")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            registrar_rosto()
        elif escolha == '2':
            reconhecimento_facial()
        elif escolha == '3':
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()
    conn.close()  # Feche a conexão com o banco de dados ao sair do programa
