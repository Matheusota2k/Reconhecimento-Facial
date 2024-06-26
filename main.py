import os
import cv2
import numpy as np
import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect('face_recognition.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    face_id INTEGER NOT NULL
)
''')

conn.commit()

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Criação da pasta 'faces' para armazenar as imagens de rostos, se não existir
os.makedirs('faces', exist_ok=True)

def carregar_rostos():
    cursor.execute('SELECT name, face_id FROM faces')
    rostos = cursor.fetchall()
    nomes, ids = zip(*rostos) if rostos else ([], [])
    return nomes, ids

# Função para salvar um novo rosto no banco de dados
def salvar_rosto(nome, face_id):
    cursor.execute('INSERT INTO faces (name, face_id) VALUES (?, ?)', (nome, face_id))
    conn.commit()
    
def treinar_modelo():
    face_samples, face_ids = [], []
    nomes, ids = carregar_rostos()
    
    for face_id in ids:
        caminho = f'faces/user.{face_id}.jpg'
        if os.path.exists(caminho):
            imagem = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
            face_samples.append(imagem)
            face_ids.append(face_id)
    
    if face_samples:
        face_recognizer.train(face_samples, np.array(face_ids))
        face_recognizer.write('face_trainer.yml')

# Função para capturar um novo rosto e registrá-lo no banco de dados
def capturar_rosto(nome, novo_id):
    webcam = cv2.VideoCapture(0)
    print("Capturando rosto. Pressione 's' para salvar e sair.")
    
    while True:
        verificacao, frame = webcam.read()
        if not verificacao:
            print("Erro ao acessar a câmera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostos = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in rostos:
            # Salva a imagem do rosto detectado e registra no banco de dados
            cv2.imwrite(f"faces/user.{novo_id}.jpg", gray[y:y+h, x:x+w])
            salvar_rosto(nome, novo_id)
            print(f"Rosto de {nome} salvo com sucesso!")
            treinar_modelo()
            webcam.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow("Registrar Rosto", frame)
        if cv2.waitKey(7) & 0xFF == ord('s'):
            break
    webcam.release()
    cv2.destroyAllWindows()

# Função para registrar um novo rosto
def registrar_rosto():
    nome = input("Digite o nome da pessoa: ").strip()
    if not nome:
        print("Erro: Nome não pode estar vazio!")
        return
    
    cursor.execute('SELECT MAX(face_id) FROM faces')
    result = cursor.fetchone()
    novo_id = (result[0] or 0) + 1
    capturar_rosto(nome, novo_id)

# Função para o reconhecimento facial em tempo real
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
                    print(f"Nome: {nome}, Compatibilidade: {confianca_txt}")
            else:
                print("Rosto não reconhecido")
        
        cv2.imshow("Reconhecimento Facial", frame)
        if cv2.waitKey(5) == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()

# Função para exibir o menu principal
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
    conn.close()