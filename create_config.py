import configparser
import os

""" Config generator """


path_conf = os.getcwd() + '/settings.cfg'


def createConfig(path_conf):
    config = configparser.ConfigParser()
    token_input = input('\nEnter you Token Telegram\n\n')
    config.add_section('Telegram_Token')
    config.set("Telegram_Token", "Token", token_input)

    with open (path_conf, 'w') as config_file:
            config.write(config_file)




if __name__ == '__main__':

   if not os.path.exists(path_conf): 
        createConfig(path_conf)
    
