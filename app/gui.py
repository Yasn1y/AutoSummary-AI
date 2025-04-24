import PySimpleGUI as sg
from pathlib import Path
from core.api_client import OpenRouterClient
from core.config import Config
from core.utils import get_file_content, save_summary
from core.history import save_history

sg.theme('DarkTeal2')  # Внешний вид

def create_window():
    layout = [
        [sg.Text('OpenRouter API Key:'), sg.Input(key='-API_KEY-', password_char='*')],
        [sg.HorizontalSeparator()],
        [
            sg.Column([
                [sg.Multiline(size=(60, 10), key='-INPUT-')],
                [sg.FileBrowse("Выбрать файл", target='-FILE-'), 
                 sg.Input(visible=False, key='-FILE-', enable_events=True)],
            ]),
            sg.Column([
                [sg.Radio('Кратко', "SUMMARY_TYPE", default=True, key='-SHORT-')],
                [sg.Radio('Подробно', "SUMMARY_TYPE", key='-DETAILED-')],
                [sg.Radio('Полный конспект', "SUMMARY_TYPE", key='-FULL-')],
                [sg.Button('Сгенерировать', size=(15, 1))],
                [sg.Button('История', size=(15, 1))],
                [sg.Button('Сохранить', disabled=True, key='-SAVE-', size=(15, 1))],
            ])
        ],
        [sg.Output(size=(80, 15), key='-OUTPUT-')],
    ]
    
    return sg.Window('AutoSummary-AI', layout, finalize=True)

def show_history_window():
    history = []
    if Path('summary_history.json').exists():
        with open('summary_history.json', 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    layout = [
        [sg.Listbox(values=[f"{item['timestamp']} - {item['type']}" for item in history], 
                   size=(60, 10), key='-HISTORY_LIST-')],
        [sg.Button('Показать'), sg.Button('Закрыть')]
    ]
    
    window = sg.Window('История запросов', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Закрыть'):
            break
        if event == 'Показать' and values['-HISTORY_LIST-']:
            selected = values['-HISTORY_LIST-'][0]
            item = next(item for item in history if item['timestamp'] in selected)
            sg.popup_scrolled(f"Тип: {item['type']}\n\nОригинал:\n{item['original']}\n\nКонспект:\n{item['summary']}", 
                            title=selected)
    window.close()

def main():
    window = create_window()
    current_summary = None
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
            
        if event == '-FILE-':
            text = get_file_content(values['-FILE-'])
            if text:
                window['-INPUT-'].update(text)
        
        if event == 'Сгенерировать':
            Config.OPENROUTER_API_KEY = values['-API_KEY-']
            text = values['-INPUT-']
            
            if not text:
                sg.popup_error("Введите текст или выберите файл!")
                continue
                
            summary_type = 'short' if values['-SHORT-'] else 'detailed' if values['-DETAILED-'] else 'full'
            
            try:
                current_summary = OpenRouterClient.generate_summary(text, summary_type)
                window['-OUTPUT-'].update(current_summary)
                window['-SAVE-'].update(disabled=False)
                save_history(text, current_summary, summary_type)
            except Exception as e:
                sg.popup_error(f"Ошибка: {str(e)}")
        
        if event == '-SAVE-':
            save_summary(current_summary)
            sg.popup("Сохранено!", "Результат сохранён в summary.txt")
        
        if event == 'История':
            show_history_window()
    
    window.close()

if __name__ == "__main__":
    main()