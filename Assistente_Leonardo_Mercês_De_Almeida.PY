
from datetime import datetime
import os
from click import pass_context
import speech_recognition as sr
from geopy.geocoders import Nominatim
#pyttsx3 is a text-to-speech conversion library in Python
#import pyttsx3
#Google Text-to-Speech
from gtts import gTTS, tts
import random
import playsound 
import webbrowser

#Função para ouvir e reconhecer a fala
class AssistenteVirtual():
    def __init__(assistente, nomeAssistente, pessoa):
        """
        inistanciar o assistente virtual
        """
        assistente.pessoa = pessoa
        assistente.nomeAssistente = nomeAssistente

        #assistente.engine = pyttsx3.init()
        assistente.reconhecer = sr.Recognizer()
        
        assistente.voice_data = ''

    def gravar_microfone(assistente, pergunta=""):
        #usando o microfone
        with sr.Microphone() as source:
            if pergunta:
                assistente.engine_speak(pergunta)
            
            #Armazena o que foi dito numa variavel
            audio = assistente.reconhecer.listen(source,5 , 5)# pega dados de auido
            print('Verificando dados!....')

            try:
                #converte audio para texto
                assistente.voice_data = assistente.reconhecer.recognize_google(audio,language='pt-BR') 

            except sr.UnknownValueError:
                #não entendeu o que foi dito
                assistente.engine_speak('Desculpe , não entendi poderia repetir ?')

            except sr.RequestError:
                #reconhecedor não conectado
                assistente.engine_speak('Desculpe , servidor indisponível!') 

            print(">>",assistente.voice_data.lower()) #imprime o que vc disse
            assistente.voice_data = assistente.voice_data.lower()

            return assistente.voice_data.lower()

    def engine_speak(assistente, audio_strig):
        audio_strig = str(audio_strig)
        tts = gTTS(text=audio_strig, lang='pt-BR')
        r = random.randint(1,20000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(assistente.nomeAssistente + ':', audio_strig)
        os.remove(audio_file)


    def termosDePesquisa(assistente, termos):
        """
        função para identificar se o termo existe
        """
        for termo in termos:
            if termo in assistente.voice_data:
                return True


    def resposta(assistente, voice_data):
        if assistente.termosDePesquisa(['oi', 'vai', 'hello', 'oi', 'holla', 'iniciar']):
            texto_assistente = F'Oi {assistente.pessoa}, o que vamos fazer hoje!'
            assistente.engine_speak(texto_assistente)
            texto_assistente = F'{assistente.pessoa}, diga google por para pesquisar no Google'
            assistente.engine_speak(texto_assistente)
            texto_assistente = F'{assistente.pessoa}, diga youtube por para proucurar no Youtube'
            assistente.engine_speak(texto_assistente)
            texto_assistente = F'{assistente.pessoa}, diga gps por para buscar o endereço e posicao geográfica de um local'
            assistente.engine_speak(texto_assistente)
            texto_assistente = F'{assistente.pessoa}, diga hora para saber a hora exata'
            assistente.engine_speak(texto_assistente)
            texto_assistente = F'{assistente.pessoa}, diga bye , sair , encerrar , acabou ou terminar para sair do assistente'
            assistente.engine_speak(texto_assistente)

        #google
        elif assistente.termosDePesquisa(['google por ']) :
            search_term = voice_data.split('por')[-1]
            search_term  = search_term[1:]
            url =  "http://google.com/search?q=" + search_term
            webbrowser.get().open(url)
            assistente.engine_speak('Aqui é o que eu encontrei para ' + search_term + 'no google')

        #google 
        elif assistente.termosDePesquisa(['youtube por']):
            search_term  = voice_data.split('por')[-1]
            search_term  = search_term[1:]
            url = "http://www.youtube.com/results?search_query=" + search_term
            webbrowser.get().open(url)
            assistente.engine_speak('Aqui é o que eu encontrei para ' + search_term + 'on youtube')

        #google 
        elif assistente.termosDePesquisa(['gps por']):
            search_term  = voice_data.split('por')[-1]
            search_term  = search_term[1:]
            loc = Nominatim(user_agent=search_term) 
            getLoc = loc.geocode(search_term) 
            assistente.engine_speak('Aqui é o que eu encontrei para ' + search_term + 'na pesquisa geográfica')
            assistente.engine_speak(getLoc.address)
        elif assistente.termosDePesquisa(['hora']):
            hora  = datetime.now().strftime('%H:%M:%S')
            assistente.engine_speak('Agora são ' + hora )
        elif assistente.termosDePesquisa(['bye', 'sair', 'encerrar', 'acabou', 'terminar']):
            pass
        else :
            assistente.engine_speak('Comando não reconhecido!')
            assistente.engine_speak('Diga oi, vai, hello , holla ou iniciar caso queira mais instruçoes!')

# Instanciar classe assistente virtual, nomeAssistente, pessoa
assistenteVirtual = AssistenteVirtual('Ganbiarra', 'Leonardo')

while True:

    voice_data = assistenteVirtual.gravar_microfone('Ouvindo...')
    assistenteVirtual.resposta(voice_data)

    if assistenteVirtual.termosDePesquisa(['bye', 'sair', 'encerrar', 'acabou', 'terminar']):
        assistenteVirtual.engine_speak('Tenha um bom dia!')
        break