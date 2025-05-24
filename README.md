📷 AleksonCamera
AleksonCamera é uma aplicação em Python com interface gráfica para cadastro e reconhecimento facial de colaboradores. Utiliza OpenCV, Face Recognition e um banco de dados (MySQL ou SQLite) para armazenar e reconhecer rostos automaticamente por meio da webcam.

✨ Funcionalidades

📸 Captura facial com webcam.

🧠 Reconhecimento facial em tempo real.

🗃️ Armazenamento de encodings faciais no banco de dados.

🧑‍💼 Interface gráfica amigável com Tkinter.

✅ Atualização automática de dados de colaboradores (nome e matrícula).


🖥️ Tecnologias utilizadas
Python 3.x

OpenCV

face_recognition

Tkinter

MySQL Connector / SQLite3

Pickle (serialização dos encodings)


⚙️ Requisitos
Python 3.7 ou superior

Webcam funcional

MySQL Server (caso use banco online)

🖼️ Interface
A interface é amigável e pensada para uso por recepcionistas ou operadores:

Campo para Nome completo

Campo para Matrícula

Botão 📸 Capturar Foto e Atualizar Encoding

Instruções interativas (ex: pressione espaço para capturar)

🔍 Reconhecimento Facial

O sistema reconhece rostos previamente cadastrados e exibe nome e matrícula em tempo real usando a câmera. Basta executar o script de reconhecimento e manter o rosto visível na frente da webcam.

📌 Observações

Caso o rosto não seja detectado, a imagem não será salva.

Os encodings são salvos em formato serializado (pickle) no banco.

A tecla q encerra o modo de reconhecimento em tempo real.

🤝 Contribuições

Agradecimentos especiais a:

Karolaine S. — desenvolvimento da interface gráfica, estruturação do projeto

Julya Dias — implementação do reconhecimento facial e integração com o banco de dados

Professor André — orientação técnica e suporte acadêmico

