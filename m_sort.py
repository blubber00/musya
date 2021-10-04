import msql

def sort_start(message, tbot):
    if message['text'] == '/start':
        answer = msql.cmd_start(message)
    elif message['text'] == '/menu':
        return(msql.cmd_menu(message, tbot)) 