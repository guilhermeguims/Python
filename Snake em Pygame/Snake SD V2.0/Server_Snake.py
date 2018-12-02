import pygame, Pyro4
import random

@Pyro4.expose #Expondo os métodos
@Pyro4.behavior(instance_mode = "single")

class Funcoes(object):
    
    def Pos_Aleatoria(self):
        x = random.randint(60,640)
        y = random.randint(60,740)
        return (x//10 * 10, y//10 * 10)

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(Funcoes)
ns.register("Obj",uri)
daemon.requestLoop()
