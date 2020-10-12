import znc

class customctcpversion(znc.Module):
    description = "Try to append custom text to ctcp"
    module_types = [znc.CModInfo.UserModule, znc.CModInfo.NetworkModule]

    def OnLoad(self, args, message):
        #self.PutModule("Loading python module customctcp")
        try:
            self.nv['prefix'] # If key prefix doesn't exist, create it
        except KeyError:
            self.nv['prefix'] = ""
        try:
            self.nv['suffix'] # If key suffix doesn't exist, create it
        except KeyError:
            self.nv['suffix'] = ""
        self.custom = len(self.nv['prefix']) + len(self.nv['suffix']) # If there is anything in the prefix or suffix then set custom to true
        try:
            self.nv['log'] # If key log doesn't exist, create it
        except KeyError:
            self.nv['log'] = 'false'
        return znc.CONTINUE

    def OnShutdown(self):
        #self.PutModule("Unloading python module customctcp")
        return znc.CONTINUE

    def handleMsg(self, nick, message):
        if self.nv['log'] == 'true':
            self.PutModule("CTCP from {0}: {1}".format(str(nick), str(message)))
        return znc.CONTINUE

    def OnPrivCTCP(self, nick, message):
        return self.handleMsg(nick, message)

    def OnChanCTCP(self, nick, channel, message):
        return self.handleMsg(nick, message)

    def OnCTCPReply(self, nick, message):
        return self.handleReply(nick, message)

    def OnUserCTCPReply(self, nick, message):
        #return self.handleReply(nick, message)
        return znc.CONTINUE

    def OnPrivCTCPReply(self, nick, message):
        return znc.CONTINUE

    def handleReply(self, nick, message):
        if self.nv['log'] == 'true':
            self.PutModule("onCTCPReply {0}: {1}".format(str(nick),str(message)))
        try:
            if self.custom:
                message.s = self.nv['prefix'] + "via".join(str(message).split("via")[:-1]) + self.nv['suffix'] # Remove the original "via ZNC - https://znc.in" text and add prefix/suffix
            # Turns out I never even needed to know about GetHideVersion()
        except Exception as e:
            self.PutModule("Error (please contact user3456 on irc/pythonmcpi on github): {0}".format(repr(e))) # Probably a corrupt input
        else:
            pass
            #self.Putmodule(str(message))
        return znc.CONTINUE

    def OnModCommand(self, line):
        if line.lower().startswith("help"):
            if line.lower() == "help" or len(line.lower().split()) == 1:
                self.PutModule("CustomCTCPVersion Help")
                self.PutModule("Set - Set Settings")
                self.PutModule("Help - Help Message")
                self.PutModule("Reset - Reset Settings")
            elif line.lower().split()[1] == "help":
                self.PutModule("Prints the help message")
            elif line.lower().split()[1] == "set":
                self.PutModule("Set prefix <prefix> - Set the prefix for the version string")
                self.PutModule("Set suffix <suffix> - Set the suffix for the version string")
                self.PutModule("Set log <true|false> - Turn on/off notifying you of any CTCP messages")
                self.PutModule("Use %space% for a space, %empty% to leave empty (so you could type a literal %space%)")
            elif line.lower().split()[1] == "reset":
                self.PutModule("Resets your settings")
            else:
                self.PutModule("Unknown Command")
        elif line.lower().startswith("set"):
            if len(line.lower().split()) == 1:
                self.PutModule("See Help Set for a list of settings")
            elif line.lower().split()[1] == "prefix":
                self.nv["prefix"] = " ".join(line.lower().split()[2:]).replace("%space%", " ").replace("%empty%", "")
                self.custom = len(self.nv["prefix"]) + len(self.nv["suffix"])
                self.PutModule("Setting prefix set to '{0}'".format(self.nv["prefix"]))
            elif line.lower().split()[1] == "suffix":
                self.nv["suffix"] = " ".join(line.lower().split()[2:]).replace("%space%", " ").replace("%empty%", "")
                self.custom = len(self.nv["prefix"]) + len(self.nv["suffix"])
                self.PutModule("Setting suffix set to '{0}'".format(self.nv["suffix"]))
            elif line.lower().split()[1] == "log":
                if line.lower().split()[2] in ['true', 'false']:
                    self.nv["log"] = line.lower().split()[2]
                    self.PutModule("Setting log set to {0}".format(self.nv["log"]))
                else:
                    self.PutModule("Please put true or false.")
            else:
                self.PutModule("Unknown Setting.")
        elif line.lower().startswith("reset"):
            self.nv["prefix"] = ""
            self.nv["suffix"] = ""
            self.nv["log"] = "false"
            self.custom = False
            self.PutModule("Settings Reset.")
        else:
            self.PutModule("Unknown Command. Type 'Help' for help.")
        return znc.CONTINUE
