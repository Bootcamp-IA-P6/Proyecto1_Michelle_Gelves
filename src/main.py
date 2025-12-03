from languages.es import LANG_ES
from languages.en import LANG_EN
from taximeter import taximeter

def main():
    #Elegir Idioma
    choice = input(LANG_ES["choose_language"]).strip().lower()
    if choice == 'es':
        lang = LANG_ES
        commands = {
            "start": "iniciar",
            "stop": "parar",
            "move": "mover",
            "finish": "finalizar",
            "exit": "salir",
        }
    elif choice == 'en':
        lang = LANG_EN
        commands = {
            "start": "start",
            "stop": "stop",
            "move": "move",
            "finish": "finish",
            "exit": "exit",
        }
    #Llamar a la funcion principal del Taxímetro
    taximeter(lang, commands)
        
if __name__ == "__main__":
    main()