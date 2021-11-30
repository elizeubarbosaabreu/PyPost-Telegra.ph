import PySimpleGUI as sg
from telegraph import Telegraph
import clipboard, webbrowser
# ---------------------------------------------------------------
#      _       _                              _     
#     | |_ ___| | ___  __ _ _ __ __ _   _ __ | |__  
#     | __/ _ \ |/ _ \/ _` | '__/ _` | | '_ \| '_ \ 
#     | ||  __/ |  __/ (_| | | | (_| |_| |_) | | | |
#      \__\___|_|\___|\__, |_|  \__,_(_) .__/|_| |_|
#                     |___/            |_|          
# 
#---------------------------------------------------------------
def postar(user, title, content):
    telegraph = Telegraph()    
    try:
        telegraph.create_account(short_name=user)

        response = telegraph.create_page(title, html_content=content)
        
        mensagem = (response['url'])    
        clipboard.copy(mensagem)    
        sg.popup_timed('Link gerado!!',
                       f'O link <{mensagem}> já está em sua área de transferência\nUse CTRL+V para colar onde deseja compartilhar...')
    
    except:
        
        sg.popup_error('Erro!',
                       'Mensagem não publicada...',
                       'Verifique sua conexão de internet ou mude o seu nome de usuário...')

#---------------------------------------------------------------
        
def manual():
    sg.Popup('Manual',
             'PyPost Telegra.ph é uma versão gráfica para o site http://telegra.ph',
             'Preencha com um título, crie um nome de usuário (pode ser fictício), crie o conteúdo e clique no botão [Publicar no Telegra.ph] ',
             'Cole o link que é gerado na área da transferência, tente [CTRL]+[V]',
             'Telegra.ph é um sistema de postagens anônimo do Telegram. Basta criar uma postagem e compartilhar o link da postagem gerado no Facebook, Twitter ou qualquer outro lugar...',
             'Telegra.ph tem suporte a links e incorporação do Youtube, Vimeo, twitter e outros...',
             'PyPost Telegra.ph foi escrito inteiramente em Python e usa a API telegra.ph e pysimplegui para interface gráfica...',
             'Obrigado por usar o PyPost Telegra.ph')
#---------------------------------------------------------------

sg.theme('SystemDefaultForReal')

heart = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAm0lEQVRYhe2Vyw2AIBBER2NFUAqWKaVAS3oy0Q3CLp9wcN+RZJjHJwAoyt9Z6MBhzMkJ7jG+srW5qknoZLU5AFglwRFsLWHpylNM3wEVUAEVKAq4EIYKsP4CFwK8tV0K6V/AOgJv7bCdYN+BHhJ09UDiCG56vPOl8qxAT5GvcpZAq0iuXCQgFSkVVwuUJLjFTQJUQlr6ZPpTrCgXkhg7Ez2kfusAAAAASUVORK5CYII='

menu = [['&Arquivo',
            ['&Texto',
             ['&Abrir',
              '&Salvar'],
             '&Publicar',
             '&Limpar',
             '&Sair']],
           ['&Editar',
            ['&Copiar',
             '&Colar']],
           ['&Formatar',
            ['&Negrito',
             '&Itálico']],
           ['&Inserir',
            ['&Code',
             '&Imagem',
             '&Link',
             '&Lista',
             '&Parágrafo']],
           ['&Ajuda',
            ['&Manual',
             '&Autor',
             ['&GitHub',
              '&Linkedin']]]
           ]

layout = [[sg.Menu(menu)],
          [sg.Text('Título da postagem:')],
          [sg.Input(key='-title-', size=(1000,1))],
          [sg.Text('Autoria (seu nome):')],
          [sg.Input(key='-autor-', size=(1000,1))],
          [sg.Text('Conteúdo: Use texto simples para parágrafos únicos ou html para textos formatados:')],
          [sg.Multiline(key='-content-', size=(1000,12))],
          [sg.Text('', size=(5, 1))],
          [sg.Stretch(),
           sg.Button('Publicar no Telegra.ph', font=('Arial', 18)),
           sg.Stretch()],
          [sg.Text('', size=(5, 1))],          
          [sg.Stretch(), sg.Text('Software feito com o', font=('Courier', 10), size=(20, 1)), sg.Image(heart)]]

window = sg.Window('PyPost Telegra.ph', layout, size=(640, 480), resizable=True)

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == 'Sair': 
        break
    
    elif event == 'Limpar':
        window['-autor-'].update('')
        window['-title-'].update('')
        window['-content-'].update('')
    
    elif event == 'Publicar' or event == 'Publicar no Telegra.ph':
        user = values['-autor-']
        title = values['-title-']
        content = values['-content-']
        postar(user, title, content)
    
    elif event == 'Abrir':
        with open('.temp.txt', 'r') as content:
            window['-content-'].update(content.read())
    
    elif event == 'Salvar':
        content = values['-content-']
        with open('.temp.txt','w') as arquivo:
            arquivo.write(content)
            sg.popup_timed('Arquivo salvo',
                           'Seu texto foi salvo no computador',
                           'Use o menu "Arquivo->Texto->Abrir"')
    
    elif event == 'Copiar':
        content = values['-content-']
        clipboard.copy(content)
        sg.popup_timed('Texto copiado',
                       'Todo o conteudo da postagem foi copiado para a área de transferência.',
                       'Use Ctrl+V para colar o conteúdo no local desejado...')
    
    elif event == 'Colar':
        content = values['-content-']
        copiado = clipboard.paste()
        content += f'{copiado}'        
        window['-content-'].update(content)
    
    elif event == 'Negrito':
        content = values['-content-']        
        content += f'<b> Seu texto aqui </b>'
        window['-content-'].update(content)
        
    elif event == 'Parágrafo':
        content = values['-content-']        
        content += f'''

<p> Seu texto aqui </p>

'''
        window['-content-'].update(content)        
    
    elif event == 'Itálico':
        content = values['-content-']        
        content += f'<i> Seu texto aqui </i>'
        window['-content-'].update(content)         
    
    elif event == 'Code':
        content = values['-content-']        
        content += f'''

<p><code>
Seu código aqui
</code></p>

'''
        window['-content-'].update(content)
    
    elif event == 'Imagem':
        content = values['-content-']        
        content += f'''
<p><img src="Link da sua imagem"></p>'''
        window['-content-'].update(content)
    
    elif event == 'Link':
        content = values['-content-']        
        content += f'<img src="Link da sua imagem">'
        window['-content-'].update(content)
    
    elif event == 'Lista':
        content = values['-content-']        
        content += f'''

<p><ol>
	<li>Editar esse texto</li><li>Editar esse texto</li><li>Editar esse texto</li>	
</ol></p>
'''
        window['-content-'].update(content)
        
        
    elif event == 'Manual':
        manual()
    
    elif event == 'GitHub':
        webbrowser.open('https://github.com/elizeubarbosaabreu/PyPost-Telegra.ph.git')
    
    elif event == 'Linkedin':
        webbrowser.open('https://www.linkedin.com/in/elizeu-barbosa-abreu-69965b218/')

window.close()

