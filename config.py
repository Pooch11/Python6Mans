import os
import configparser as cp

configFile = "config.ini"
discordGroup = "Discord"
tokenKey = "token"
prefixKey = "prefix"
channelKey = "channel"
lbsizeKey = "sizekey"


class Config:
    def __init__(self):
        self.cp = cp.ConfigParser()
        self.check_config()

    def check_config(self):
        if os.path.isfile(configFile):
            self.cp.read(configFile)
            return
        print('No config.ini file. Creating a default one.')
        self.create_config()

    def create_config(self):
        self.cp[discordGroup] = {}
        self.cp[discordGroup][tokenKey] = ""
        self.cp[discordGroup][prefixKey] = ""
        self.cp[discordGroup][channelKey] = ""
        self.cp[discordGroup][lbsizeKey] = ""
        with open(configFile, "w") as file:
            self.cp.write(file)

    @property
    def bot_token(self):
        return self.cp[discordGroup][tokenKey]

    @property
    def command_prefix(self):
        return self.cp[discordGroup][prefixKey]
    
    @property
    def queue_channel(self):
        return self.cp[discordGroup][channelKey]
    
    @property
    def lobby_size(self):
        return self.cp[discordGroup][lbsizeKey]

