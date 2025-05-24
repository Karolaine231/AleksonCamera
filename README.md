# 📷 AleksonCamera

**AleksonCamera** é uma aplicação em Python com interface gráfica para **cadastro e reconhecimento facial** de colaboradores. Utiliza **OpenCV**, **face_recognition** e um banco de dados (**MySQL** ou **SQLite**) para armazenar e reconhecer rostos automaticamente por meio da webcam.

---

## ✨ Funcionalidades

- 📸 Captura facial com webcam  
- 🧠 Reconhecimento facial em tempo real  
- 🗃️ Armazenamento de encodings faciais no banco de dados  
- 🧑‍💼 Interface gráfica amigável com Tkinter  
- ✅ Atualização automática de dados de colaboradores (nome e matrícula)  

---

## 🖥️ Tecnologias Utilizadas

- Python 3.x  
- [OpenCV](https://opencv.org/)  
- [face_recognition](https://github.com/ageitgey/face_recognition)  
- Tkinter (interface gráfica)  
- MySQL Connector / SQLite3  
- Pickle (para serialização dos encodings)  

---

## ⚙️ Requisitos

- Python 3.7 ou superior  
- Webcam funcional  
- Servidor MySQL ativo (caso utilize banco de dados online)  

---

## 🖼️ Interface

A interface é amigável e pensada para uso por **recepcionistas ou operadores**.  
Ela inclui:

- Campo para **Nome completo**  
- Campo para **Matrícula**  
- Botão **📸 Capturar Foto e Atualizar Encoding**  
- Instruções interativas durante o processo (ex: *pressione espaço para capturar*)  

---

## 🔍 Reconhecimento Facial

O sistema reconhece rostos previamente cadastrados e exibe **nome e matrícula em tempo real** utilizando a câmera.

### Para usar:
- Execute o script de reconhecimento
- Mantenha o rosto visível diante da webcam
- A tecla **`q`** encerra o modo de reconhecimento

---

## 📌 Observações

- Caso o rosto **não seja detectado**, a imagem **não será salva**  
- Os encodings são armazenados em formato **serializado (pickle)** no banco de dados  
- Recomenda-se iluminação adequada para melhores resultados  

---

## 🤝 Contribuições

Agradecimentos especiais a:

- **Karolaine S.** — desenvolvimento da interface gráfica, estruturação do projeto  
- **Julya Dias** — implementação do reconhecimento facial e integração com o banco de dados  
- **Professor André** — orientação técnica e suporte acadêmico  

---

## 📬 Licença

Este projeto é de livre uso educacional. Para outros fins, consulte os autores.
