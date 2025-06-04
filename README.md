# 📸 Sistema de Reconhecimento e Controle de Ponto Inteligente

O **Sistema de Reconhecimento e Controle de Ponto Inteligente** é uma solução completa para gerenciamento de acesso e registro de ponto de colaboradores, integrando reconhecimento facial, um robusto backend MySQL com PHP e um frontend baseado em ESP32 para automação.

---

## ✨ Funcionalidades

### AleksonCamera (Módulo de Cadastro e Reconhecimento Facial - Python)
- 📷 **Captura Facial com Webcam**
- 🔍 **Reconhecimento Facial em Tempo Real**
- 💾 **Armazenamento de Encodings Faciais no MySQL**
- 🖼️ **Interface Gráfica com Tkinter**
- 📝 **Cadastro e Atualização de Dados**
- 👨‍🏫 **Instruções Interativas para o Usuário**

### Sistema de Controle de Ponto (Backend PHP e Frontend ESP32)
- 🏢 **Gerenciamento de Empresas e Departamentos**
- 👷 **Cadastro de Colaboradores com Dados Completos e Encoding Facial**
- 🕒 **Registro de Ponto Automatizado com Data/Hora**
- 🔄 **Backup Automático via Trigger MySQL**
- 🛠️ **API PHP para Registro (`index.php`) e Sincronização (`select.php`)**
- 📡 **Frontend com ESP32: Automação com Sensores e Saídas Digitais**

---

## 🖥️ Tecnologias Utilizadas

### Módulo Python (AleksonCamera) - Front-end
- Python 3.10+
- `opencv-python`
- `face_recognition`
- `tkinter`
- `mysql-connector-python`
- `pickle`
- `requests`

### Backend (PHP)
- PHP 7+
- MySQL

### Comunicação Hardware (ESP32 / Arduino)
- ESP32 com Arduino IDE
- Bibliotecas: `WiFi.h`, `HTTPClient.h`, `ArduinoJson.h (v6+)`, `DHT.h`

---

## ⚙️ Requisitos

- Python 3.10 ou superior
- Webcam funcional
- Servidor MySQL com acesso remoto
- Servidor Web com suporte a PHP
- Placa ESP32 com Arduino IDE

---

## 🏛️ Estrutura do Banco de Dados (MySQL)

- `BDEmpresaInterno`
- `Departamento`
- `Colaborador` (inclui `encoding` tipo BLOB)
- `Ponto` (registros temporários, apagados após leitura)
- `BackupPontoCompleto` (backup automático via trigger)

---

## 🚀 Como Usar

### 1. Configuração do Banco de Dados
- Crie as tabelas conforme especificado.
- Configure o trigger para backup automático.

### 2. Configuração do Backend (PHP)
- Hospede `index.php` e `select.php`.
- Ajuste as credenciais MySQL.

#### Exemplo de `index.php` (POST):
```json
{
  "encoding": "base64_string_do_encoding_facial",
  "dataRegistro": "YYYY-MM-DD",
  "horarioentrada": "HH:MM:SS",
  "matricula": "XXXXXXXX"
}
```

#### Exemplo de resposta:
```json
{"status": "success", "message": "Reconhecimento confirmado...", "matricula": "...", "nome": "..."}
```

### 3. Configuração do Módulo Python
- Instale com:  
  ```bash
  pip install opencv-python face_recognition mysql-connector-python requests
  ```
- Configure variáveis de conexão e execute:  
  ```bash
  python seu_script_cadastro_reconhecimento.py
  ```

### 4. Configuração do ESP32
- Instale bibliotecas no Arduino IDE.
- Ajuste SSID, senha e URL da API.
- Faça upload para o ESP32.

---

## 🛠️ Teste Completo

1. Inicie o módulo AleksonCamera.
2. Cadastre um colaborador e capture o rosto.
3. Realize o reconhecimento com a câmera.
4. Verifique o registro no banco (tabela `Ponto` e `BackupPontoCompleto`).
5. Confirme a leitura e acionamento no ESP32.

---

## 📌 Observações Adicionais

- Iluminação adequada melhora a detecção facial.
- Registros na tabela `Ponto` são removidos após leitura.
- A lógica de entrada/saída é definida no backend PHP.

---

## 🤝 Contribuições

- **Karolaine S.** — Responsável pelo design e implementação da interface gráfica (Tkinter) e pela estruturação geral do projeto.
- **Julya Dias** — Envolveu-se diretamente na implementação do reconhecimento facial, na integração do sistema com o banco de dados e no desenvolvimento da lógica para a arquitetura de comunicação Back-end.
- **Alice B.** — Contribuiu com a concepção da estrutura física do projeto e a montagem dos circuitos eletrônicos.
- **Professor André** — Prestou orientação técnica e suporte acadêmico contínuo.

---

## 📬 Licença

Uso livre para fins educacionais. Para usos comerciais, consulte os autores.
