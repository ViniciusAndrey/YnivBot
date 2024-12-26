# YnivBot 🤖

<div align="center">

![Discord Bot](https://img.shields.io/badge/Discord%20Bot-YnivBot-7289DA?style=for-the-badge&logo=discord)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

</div>

## 📖 Sobre
YnivBot é um bot Discord multifuncional desenvolvido em Python que traz diversão e utilidade para seu servidor! Com uma ampla variedade de comandos, desde jogos divertidos até ferramentas de moderação, o YnivBot é o companheiro perfeito para sua comunidade.

## ✨ Funcionalidades

### 🛡️ Moderação
| Comando | Descrição |
|---------|-----------|
| `!kick` | Expulsa membros do servidor |
| `!ban` | Bane membros do servidor |
| `!limpar` | Remove mensagens em massa |
| `!convite` | Gera um convite para o servidor |

### 🎮 Jogos e Diversão
| Comando | Descrição |
|---------|-----------|
| `!forca` | Jogo da forca interativo |
| `!quiz` | Quiz de conhecimentos gerais |
| `!adivinha` | Adivinhe o número secreto |
| `!jogar` | Pedra, papel e tesoura |
| `!moeda` | Cara ou coroa |
| `!dado` | Rola dados customizados |

### 💰 Economia
| Comando | Descrição |
|---------|-----------|
| `!daily` | Recebe moedas diárias |
| `!saldo` | Consulta seu saldo |
| `!pagar` | Transfere moedas |

### 🔍 Utilidades
| Comando | Descrição |
|---------|-----------|
| `!perfil` | Informações do usuário |
| `!serverinfo` | Estatísticas do servidor |
| `!clima` | Previsão do tempo |
| `!ping` | Latência do bot |

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Uma conta Discord
- Token do bot Discord
- Chave API do serviço de clima

### Passo a Passo

1. **Clone o repositório**
```

2. **Crie um ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install discord.py python-dotenv requests
```

4. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
DISCORD_TOKEN=seu_token_aqui
WEATHER_API_KEY=sua_chave_api_aqui
```

5. **Inicie o bot**
```bash
python bot.py
```

## ⚙️ Configuração do Bot Discord

1. Acesse o [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications)
2. Clique em "New Application"
3. Dê um nome para sua aplicação
4. Vá para a seção "Bot"
5. Clique em "Add Bot"
6. Copie o token do bot
7. Ative as seguintes intents:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent

## 🔐 Permissões Necessárias
O bot precisa das seguintes permissões:
- [x] Ler Mensagens
- [x] Enviar Mensagens
- [x] Gerenciar Mensagens
- [x] Incorporar Links
- [x] Anexar Arquivos
- [x] Ver Histórico de Mensagens
- [x] Adicionar Reações
- [x] Expulsar Membros
- [x] Banir Membros
- [x] Criar Convite

## 🎯 Recursos Principais
- Sistema de economia com moedas diárias
- Jogos interativos (Forca, Quiz, Adivinhação)
- Comandos de moderação
- Sistema de clima
- Informações detalhadas de usuários e servidor
- Criação de enquetes
- Sistema de música (em desenvolvimento)

## 📫 Suporte
- Reporte bugs através das [issues](https://github.com/ViniciusAndrey/YnivBot/issues)
- Para sugestões, abra uma [nova issue](https://github.com/ViniciusAndrey/YnivBot/issues/new)

## 📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📊 Status do Projeto
- [x] Sistema de Moderação
- [x] Sistema de Economia
- [x] Jogos Interativos
- [x] Comandos de Utilidade
- [ ] Sistema de Música
- [ ] Sistema de Níveis
- [ ] Sistema de Boas-vindas
- [ ] Auto-moderação

---
<div align="center">
Desenvolvido com ❤️ usando Python e discord.py

[⭐ Dê uma estrela](https://github.com/ViniciusAndrey/YnivBot) • [🐛 Reportar Bug](https://github.com/ViniciusAndrey/YnivBot/issues) • [💡 Sugerir Feature](https://github.com/ViniciusAndrey/YnivBot/issues/new)
</div>
