import discord
import random
import requests
from discord.ext import commands
import asyncio
import json
import datetime
from typing import Optional
from discord import Member
from difflib import get_close_matches
import time
import platform

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot está online como {bot.user.name}')

@bot.command()
async def oi(ctx):
    await ctx.send(f'Olá {ctx.author.name}!')

@bot.command()
async def eco(ctx, *, mensagem):
    await ctx.send(mensagem)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int):
    if quantidade <= 0:
        await ctx.send("Por favor, especifique um número maior que 0!")
        return
    
    if quantidade > 100:
        await ctx.send("Você só pode deletar até 100 mensagens por vez!")
        return
    
    try:
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=quantidade)
        
        msg = await ctx.send(f"✅ {len(deleted)} mensagens foram apagadas!")
        await asyncio.sleep(5)
        await msg.delete()
        
    except discord.Forbidden:
        await ctx.send("Eu não tenho permissão para apagar mensagens!")
    except discord.HTTPException as e:
        await ctx.send(f"Ocorreu um erro ao tentar apagar as mensagens: {e}")

@limpar.error
async def limpar_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para usar este comando!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Por favor, especifique quantas mensagens deseja apagar!\nExemplo: !limpar 10")
    else:
        await ctx.send(f"Ocorreu um erro: {error}")

@bot.command()
async def servidor(ctx):
    guild = ctx.guild
    await ctx.send(f'''
    Nome: {guild.name}
    Membros: {guild.member_count}
    Criado em: {guild.created_at.strftime("%d/%m/%Y")}
    ''')

def load_bank():
    try:
        with open('bank.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_bank(bank):
    with open('bank.json', 'w') as f:
        json.dump(bank, f)

bank = load_bank()

PALAVRAS_FORCA = ['python', 'programacao', 'computador', 'desenvolvimento', 'tecnologia', 'javascript', 'discord']

PERGUNTAS_QUIZ = [
    {
        'pergunta': 'Qual é a linguagem de programação mais popular?',
        'resposta': 'python',
        'dica': 'É uma serpente...'
    },
    {
        'pergunta': 'Qual é o maior planeta do sistema solar?',
        'resposta': 'jupiter',
        'dica': 'É um planeta gasoso...'
    },
    {
        'pergunta': 'Quem criou o Linux?',
        'resposta': 'linus torvalds',
        'dica': 'Seu primeiro nome é Linus...'
    }
]

@bot.command()
async def perfil(ctx, membro: Optional[Member] = None):
    membro = membro or ctx.author
    
    conta_criada = membro.created_at.strftime("%d/%m/%Y")
    entrou_servidor = membro.joined_at.strftime("%d/%m/%Y")
    
    embed = discord.Embed(title=f"Perfil de {membro.name}", color=membro.color)
    embed.set_thumbnail(url=membro.avatar.url if membro.avatar else membro.default_avatar.url)
    embed.add_field(name="ID", value=membro.id, inline=True)
    embed.add_field(name="Conta criada em", value=conta_criada, inline=True)
    embed.add_field(name="Entrou no servidor em", value=entrou_servidor, inline=True)
    embed.add_field(name="Cargo mais alto", value=membro.top_role.name, inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    
    embed = discord.Embed(title=f"Informações do {guild.name}", color=discord.Color.blue())
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    owner = guild.owner
    owner_name = owner.name if owner else "Não encontrado"
    
    embed.add_field(name="Dono", value=owner_name, inline=True)
    embed.add_field(name="Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Membros", value=guild.member_count, inline=True)
    
    text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
    voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
    
    embed.add_field(name="Canais de Texto", value=text_channels, inline=True)
    embed.add_field(name="Canais de Voz", value=voice_channels, inline=True)
    embed.add_field(name="Cargos", value=len(guild.roles), inline=True)
    
    embed.add_field(name="Nível de Boost", value=f"Nível {guild.premium_tier}", inline=True)
    embed.add_field(name="Boosters", value=guild.premium_subscription_count or "0", inline=True)
    
    embed.add_field(name="Emojis", value=len(guild.emojis), inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, pergunta, *opcoes):
    if len(opcoes) > 10:
        await ctx.send("Máximo de 10 opções!")
        return
    
    if len(opcoes) < 2:
        await ctx.send("Mínimo de 2 opções!")
        return
    
    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    descricao = []
    for i, opcao in enumerate(opcoes):
        descricao.append(f"{emojis[i]} {opcao}")
    
    embed = discord.Embed(title=pergunta, description='\n'.join(descricao), color=discord.Color.blue())
    embed.set_footer(text=f"Enquete criada por {ctx.author.name}")
    
    msg = await ctx.send(embed=embed)
    
    for i in range(len(opcoes)):
        await msg.add_reaction(emojis[i])

@bot.command()
async def daily(ctx):
    user_id = str(ctx.author.id)
    
    if user_id not in bank:
        bank[user_id] = {"wallet": 0, "last_daily": ""}
    
    last_daily = bank[user_id].get("last_daily", "")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if last_daily == today:
        await ctx.send("Você já recebeu suas moedas diárias hoje! Volte amanhã!")
        return
    
    bank[user_id]["wallet"] = bank[user_id].get("wallet", 0) + 100
    bank[user_id]["last_daily"] = today
    save_bank(bank)
    
    await ctx.send(f"Você recebeu 100 moedas! Seu saldo atual é {bank[user_id]['wallet']} moedas.")

@bot.command()
async def saldo(ctx):
    user_id = str(ctx.author.id)
    
    if user_id not in bank:
        bank[user_id] = {"wallet": 0, "last_daily": ""}
        save_bank(bank)
    
    await ctx.send(f"Seu saldo atual é {bank[user_id]['wallet']} moedas.")

@bot.command()
async def pagar(ctx, membro: Member, quantidade: int):
    if quantidade <= 0:
        await ctx.send("A quantidade deve ser maior que zero!")
        return
    
    pagador_id = str(ctx.author.id)
    recebedor_id = str(membro.id)
    
    if pagador_id not in bank:
        bank[pagador_id] = {"wallet": 0, "last_daily": ""}
    if recebedor_id not in bank:
        bank[recebedor_id] = {"wallet": 0, "last_daily": ""}
    
    if bank[pagador_id]["wallet"] < quantidade:
        await ctx.send("Você não tem moedas suficientes!")
        return
    
    bank[pagador_id]["wallet"] -= quantidade
    bank[recebedor_id]["wallet"] += quantidade
    save_bank(bank)
    
    await ctx.send(f"Transferência realizada com sucesso! {quantidade} moedas foram enviadas para {membro.name}")

@bot.command()
async def moeda(ctx):
    resultado = random.choice(['Cara', 'Coroa'])
    embed = discord.Embed(title="🪙 Cara ou Coroa", color=discord.Color.gold())
    embed.add_field(name="Resultado", value=f"**{resultado}**!")
    await ctx.send(embed=embed)

@bot.command()
async def forca(ctx):
    palavra = random.choice(PALAVRAS_FORCA)
    letras_certas = set()
    letras_erradas = set()
    tentativas = 6
    
    def mostrar_palavra():
        return ' '.join(letra if letra in letras_certas else '_' for letra in palavra)
    
    def mostrar_forca():
        stages = [
            '''
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / \\
               -
            ''',
            '''
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     /
               -
            ''',
            '''
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |
               -
            ''',
            '''
               --------
               |      |
               |      O
               |     \\|
               |      |
               |
               -
            ''',
            '''
               --------
               |      |
               |      O
               |      |
               |      |
               |
               -
            ''',
            '''
               --------
               |      |
               |      O
               |
               |
               |
               -
            ''',
            '''
               --------
               |      |
               |
               |
               |
               |
               -
            '''
        ]
        return stages[tentativas]

    embed = discord.Embed(title="🎯 Jogo da Forca", color=discord.Color.blue())
    embed.add_field(name="Palavra", value=f"```{mostrar_palavra()}```", inline=False)
    embed.add_field(name="Letras erradas", value="Nenhuma", inline=True)
    embed.add_field(name="Tentativas restantes", value=tentativas, inline=True)
    embed.add_field(name="Forca", value=f"```{mostrar_forca()}```", inline=False)
    
    msg = await ctx.send(embed=embed)
    
    while tentativas > 0:
        try:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and len(m.content) == 1
            
            resposta = await bot.wait_for('message', timeout=30.0, check=check)
            letra = resposta.content.lower()
            
            if letra in letras_certas or letra in letras_erradas:
                await ctx.send("Você já tentou essa letra!", delete_after=3)
                continue
                
            if letra in palavra:
                letras_certas.add(letra)
                if all(letra in letras_certas for letra in palavra):
                    await ctx.send(f"🎉 Parabéns! Você venceu! A palavra era: **{palavra}**")
                    return
            else:
                letras_erradas.add(letra)
                tentativas -= 1
            
            embed = discord.Embed(title="🎯 Jogo da Forca", color=discord.Color.blue())
            embed.add_field(name="Palavra", value=f"```{mostrar_palavra()}```", inline=False)
            embed.add_field(name="Letras erradas", value=', '.join(letras_erradas) or "Nenhuma", inline=True)
            embed.add_field(name="Tentativas restantes", value=tentativas, inline=True)
            embed.add_field(name="Forca", value=f"```{mostrar_forca()}```", inline=False)
            
            await msg.edit(embed=embed)
            
        except asyncio.TimeoutError:
            await ctx.send(f"Tempo esgotado! A palavra era: **{palavra}**")
            return
    
    await ctx.send(f"💀 Game Over! A palavra era: **{palavra}**")

@bot.command()
async def quiz(ctx):
    pergunta = random.choice(PERGUNTAS_QUIZ)
    tentativas = 3
    dica_usada = False
    
    embed = discord.Embed(title="🎮 Quiz", color=discord.Color.green())
    embed.add_field(name="Pergunta", value=pergunta['pergunta'], inline=False)
    embed.add_field(name="Tentativas", value=tentativas, inline=True)
    embed.add_field(name="Dica", value="Digite !dica para receber uma dica", inline=True)
    
    await ctx.send(embed=embed)
    
    while tentativas > 0:
        try:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            
            resposta = await bot.wait_for('message', timeout=30.0, check=check)
            
            if resposta.content.lower() == '!dica' and not dica_usada:
                await ctx.send(f"💡 Dica: {pergunta['dica']}")
                dica_usada = True
                continue
            
            if get_close_matches(resposta.content.lower(), [pergunta['resposta']], n=1, cutoff=0.8):
                await ctx.send(f"🎉 Parabéns! Você acertou! A resposta era: **{pergunta['resposta']}**")
                return
            else:
                tentativas -= 1
                if tentativas > 0:
                    await ctx.send(f"❌ Resposta errada! Você ainda tem {tentativas} tentativas.")
                
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ Tempo esgotado! A resposta era: **{pergunta['resposta']}**")
            return
    
    await ctx.send(f"💀 Game Over! A resposta era: **{pergunta['resposta']}**")

@bot.command()
async def ajuda(ctx):
    embed = discord.Embed(title="📚 Lista de Comandos", 
                         description="Use ! antes de cada comando",
                         color=discord.Color.blue())

    basic = """
    `!oi` - Envia uma saudação
    `!eco [mensagem]` - Repete sua mensagem
    `!ping` - Mostra a latência do bot
    `!avatar [membro]` - Mostra o avatar
    `!botinfo` - Informações do bot
    `!convite` - Cria um convite
    """
    embed.add_field(name="📝 Comandos Básicos", value=basic, inline=False)

    mod = """
    `!kick [membro] [motivo]` - Expulsa um membro
    `!ban [membro] [motivo]` - Bane um membro
    `!limpar [quantidade]` - Limpa mensagens
    """
    embed.add_field(name="🛡️ Moderação", value=mod, inline=False)

    info = """
    `!perfil [membro]` - Mostra informações do perfil
    `!serverinfo` - Mostra informações do servidor
    `!clima [cidade]` - Mostra o clima atual da cidade
    """
    embed.add_field(name="ℹ️ Informações", value=info, inline=False)

    games = """
    `!jogar [pedra/papel/tesoura]` - Joga Pedra, Papel ou Tesoura
    `!adivinha` - Tenta adivinhar um número
    `!moeda` - Joga cara ou coroa
    `!forca` - Inicia um jogo da forca
    `!quiz` - Inicia um quiz de conhecimentos gerais
    `!escolher [opções]` - Escolhe entre opções
    `!dado [lados]` - Rola um dado
    """
    embed.add_field(name="🎮 Jogos", value=games, inline=False)

    economy = """
    `!daily` - Recebe moedas diárias
    `!saldo` - Mostra seu saldo atual
    `!pagar [membro] [quantidade]` - Transfere moedas
    """
    embed.add_field(name="💰 Economia", value=economy, inline=False)

    fun = """
    `!reverse [texto]` - Inverte o texto
    `!say [mensagem]` - Faz o bot falar
    `!poll [pergunta] [opções]` - Cria uma enquete
    """
    embed.add_field(name="🎪 Diversão", value=fun, inline=False)

    embed.set_footer(text="Para mais detalhes sobre um comando, use !ajuda [comando]")

    await ctx.send(embed=embed)

@bot.command()
async def clima(ctx, *, cidade):
    API_KEY = 'SUA_CHAVE_AQUI'
    url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={cidade}&lang=pt'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print("Resposta da API:", data)
        
        if 'error' in data:
            await ctx.send(f"Erro: {data['error']['message']}")
            return
            
        temp = data['current']['temp_c']
        condição = data['current']['condition']['text']
        umidade = data['current']['humidity']
        sensação = data['current']['feelslike_c']
        
        embed = discord.Embed(title=f"Clima em {data['location']['name']}, {data['location']['country']}", 
                            color=discord.Color.green())
        embed.add_field(name="Temperatura", value=f"{temp}°C", inline=True)
        embed.add_field(name="Sensação", value=f"{sensação}°C", inline=True)
        embed.add_field(name="Condição", value=condição, inline=True)
        embed.add_field(name="Umidade", value=f"{umidade}%", inline=True)
        
        await ctx.send(embed=embed)
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        await ctx.send("Erro ao conectar com o serviço de clima. Tente novamente mais tarde.")
    except KeyError as e:
        print(f"Erro ao processar dados: {e}")
        print("Dados recebidos:", data)
        await ctx.send("Erro ao processar as informações do clima.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        await ctx.send("Ocorreu um erro inesperado ao buscar as informações do clima.")

@bot.command()
async def jogar(ctx, escolha):
    opcoes = ['pedra', 'papel', 'tesoura']
    if escolha.lower() not in opcoes:
        await ctx.send("Escolha pedra, papel ou tesoura!")
        return
    
    bot_escolha = random.choice(opcoes)
    
    if escolha.lower() == bot_escolha:
        resultado = "Empate!"
    elif (escolha.lower() == "pedra" and bot_escolha == "tesoura") or \
         (escolha.lower() == "papel" and bot_escolha == "pedra") or \
         (escolha.lower() == "tesoura" and bot_escolha == "papel"):
        resultado = "Você venceu!"
    else:
        resultado = "Eu venci!"
    
    await ctx.send(f"Você escolheu {escolha}\nEu escolhi {bot_escolha}\n{resultado}")

@bot.command()
async def adivinha(ctx):
    numero = random.randint(1, 10)
    await ctx.send("Adivinhe o número que estou pensando (entre 1 e 10)! Você tem 3 tentativas.")
    
    tentativas = 3
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    while tentativas > 0:
        try:
            msg = await bot.wait_for('message', timeout=30.0, check=check)
            palpite = int(msg.content)
            
            if palpite == numero:
                await ctx.send(f"Parabéns! Você acertou! O número era {numero}!")
                return
            elif palpite < numero:
                tentativas -= 1
                if tentativas > 0:
                    await ctx.send(f"O número é maior! Você ainda tem {tentativas} tentativas.")
            else:
                tentativas -= 1
                if tentativas > 0:
                    await ctx.send(f"O número é menor! Você ainda tem {tentativas} tentativas.")
                    
        except ValueError:
            await ctx.send("Por favor, digite apenas números!")
        except TimeoutError:
            await ctx.send("Tempo esgotado! Jogo encerrado.")
            return
    
    await ctx.send(f"Suas tentativas acabaram! O número era {numero}!")

@bot.command()
async def ping(ctx):
    inicio = time.perf_counter()
    mensagem = await ctx.send("Calculando ping...")
    fim = time.perf_counter()
    
    latencia = round((fim - inicio) * 1000)
    latencia_api = round(bot.latency * 1000)
    
    embed = discord.Embed(title="🏓 Pong!", color=discord.Color.green())
    embed.add_field(name="Latência", value=f"{latencia}ms", inline=True)
    embed.add_field(name="Latência API", value=f"{latencia_api}ms", inline=True)
    
    await mensagem.edit(content=None, embed=embed)

@bot.command()
async def avatar(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    
    embed = discord.Embed(title=f"Avatar de {membro.name}", color=membro.color)
    embed.set_image(url=membro.avatar.url if membro.avatar else membro.default_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(title="Informações do Bot", color=discord.Color.blue())
    
    embed.add_field(name="Python", value=platform.python_version(), inline=True)
    embed.add_field(name="Discord.py", value=discord.__version__, inline=True)
    embed.add_field(name="Sistema", value=platform.system(), inline=True)
    
    embed.add_field(name="Servidores", value=len(bot.guilds), inline=True)
    embed.add_field(name="Usuários", value=len(set(bot.get_all_members())), inline=True)
    embed.add_field(name="Comandos", value=len(bot.commands), inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def escolher(ctx, *opcoes):
    if len(opcoes) < 2:
        await ctx.send("Por favor, forneça pelo menos duas opções!")
        return
    
    escolha = random.choice(opcoes)
    await ctx.send(f"🎲 Eu escolho: **{escolha}**")

@bot.command()
async def dado(ctx, lados: int = 6):
    if lados < 2:
        await ctx.send("O dado precisa ter pelo menos 2 lados!")
        return
    
    resultado = random.randint(1, lados)
    await ctx.send(f"🎲 Você rolou um d{lados} e obteve: **{resultado}**")

@bot.command()
async def reverse(ctx, *, texto: str):
    await ctx.send(texto[::-1])

@bot.command()
async def say(ctx, *, mensagem):
    await ctx.message.delete()
    await ctx.send(mensagem)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro: discord.Member, *, motivo=None):
    try:
        await membro.kick(reason=motivo)
        embed = discord.Embed(title="👢 Membro Expulso", color=discord.Color.red())
        embed.add_field(name="Membro", value=f"{membro.name}#{membro.discriminator}", inline=True)
        embed.add_field(name="Moderador", value=ctx.author.name, inline=True)
        embed.add_field(name="Motivo", value=motivo or "Nenhum motivo fornecido", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Não foi possível expulsar o membro.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo=None):
    try:
        await membro.ban(reason=motivo)
        embed = discord.Embed(title="🔨 Membro Banido", color=discord.Color.dark_red())
        embed.add_field(name="Membro", value=f"{membro.name}#{membro.discriminator}", inline=True)
        embed.add_field(name="Moderador", value=ctx.author.name, inline=True)
        embed.add_field(name="Motivo", value=motivo or "Nenhum motivo fornecido", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Não foi possível banir o membro.")

@bot.command()
async def convite(ctx):
    try:
        invite = await ctx.channel.create_invite(max_age=300)
        await ctx.send(f"🎫 Aqui está seu convite: {invite}")
    except:
        await ctx.send("Não foi possível criar um convite.")

bot.run('SEU_TOKEN_AQUI') 