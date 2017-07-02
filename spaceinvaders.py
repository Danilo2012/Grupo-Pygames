from pygame import *
import sys
from random import shuffle, randrange, choice

#           R    G    B
BLANCO     = (255, 255, 255)
VERDE     = (78, 255, 87)
AMARILLO     = (241, 255, 0)
AZUL     = (80, 255, 239)
MORADO     = (203, 0, 255)
ROJO     = (237, 28, 36)

PANTALLA         = display.set_mode((800,600))
FONDO = "fonts/space_invaders.ttf"
IMG_NAMES     = ["nave", "nave", "bonus", "enemigo1_1", "enemigo1_2", "enemigo2_1", "enemigo2_2",
                "enemigo3_1", "enemigo3_2", "explosionazul", "explosionverde", "explosionmorado", "laser", "enemigolaser"]
IMAGES         = {name: image.load("imagenes/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES}

class nave(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = IMAGES["nave"]
        self.rect = self.image.get_rect(topleft=(375, 540))
        self.velocidad = 5

    def update(self, tecla, *args):
        if tecla[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.velocidad
        if tecla[K_RIGHT] and self.rect.x < 740:
            self.rect.x += self.velocidad
        game.screen.blit(self.image, self.rect)


class Proyectil(sprite.Sprite):
    def __init__(self, xpos, ypos, direccion, velocidad, nombrefila, lado):
        sprite.Sprite.__init__(self)
        self.image = IMAGES[nombrefila]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.velocidad = velocidad
        self.direccion = direccion
        self.lado = lado
        self.nombrefila = nombrefila

    def update(self, tecla, *args):
        game.screen.blit(self.image, self.rect)
        self.rect.y += self.velocidad * self.direccion
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()


class Enemigo(sprite.Sprite):
    def __init__(self, fila, columna):
        sprite.Sprite.__init__(self)
        self.fila = fila
        self.columna = columna
        self.images = []
        self.cargar_imagenes()
        self.indice = 0
        self.image = self.images[self.indice]
        self.rect = self.image.get_rect()
        self.direccion = 1
        self.moverDerecha = 15
        self.moverIzquierda = 30
        self.moveNumero = 0
        self.cambiarTiempo = 600
        self.primerTiempo = True
        self.movimientoY = False;
        self.columnas = [False] * 10
        self.columnasVivas = [True] * 10
        self.agregarMovimientoDerecha = False
        self.agregarMovimientoIzquierda = False
        self.numeroDeMovimientosDerecha= 0
        self.numeroDeMovimientosIzquierda = 0
        self.contador = time.get_ticks()

    def update(self, tecla, horaActual, muertefila, muertecolumna, muerteFormacion):
        self.comprobar_eliminacion_columnaa(muertefila, muertecolumna, muerteFormacion)
        if horaActual - self.contador > self.cambiarTiempo:
            self.movimientoY = False;
            if self.moveNumero >= self.moverDerecha and self.direccion == 1:
                self.direccion *= -1
                self.moveNumero = 0
                self.rect.y += 35
                self.movimientoY = True
                if self.agregarMovimientoDerecha:
                    self.moverDerecha += self.numeroDeMovimientosDerecha
                if self.primerTiempo:
                    self.moverDerecha = self.moverIzquierda;
                    self.primerTiempo = False;
                self.agregarMovimientoDerechaDespuesBajar = False
            if self.moveNumero >= self.moverIzquierda and self.direccion == -1:
                self.direccion *= -1
                self.moveNumero = 0
                self.rect.y += 35
                self.movimientoY = True
                if self.agregarMovimientoIzquierda:
                    self.moverIzquierda += self.numeroDeMovimientosIzquierda
                self.agregarMovimientoIzquierdaAfterDrop = False
            if self.moveNumero < self.moverDerecha and self.direccion == 1 and not self.movimientoY:
                self.rect.x += 10
                self.moveNumero += 1
            if self.moveNumero < self.moverIzquierda and self.direccion == -1 and not self.movimientoY:
                self.rect.x -= 10
                self.moveNumero += 1

            self.indice += 1
            if self.indice >= len(self.images):
                self.indice = 0
            self.image = self.images[self.indice]

            self.contador += self.cambiarTiempo
        game.screen.blit(self.image, self.rect)

    def comprobar_eliminacion_columnaa(self, muertefila, muertecolumna, muerteFormacion):
        if muertefila != -1 and muertecolumna != -1:
            muerteFormacion[muertefila][muertecolumna] = 1
            for columna in range(10):
                if all([muerteFormacion[fila][columna] == 1 for fila in range(5)]):
                    self.columnas[columna] = True

        for i in range(5):
            if all([self.columnas[x] for x in range(i + 1)]) and self.columnasVivas[i]:
                self.moverIzquierda += 5
                self.columnasVivas[i] = False
                if self.direccion == -1:
                    self.moverDerecha += 5
                else:
                    self.agregarMovimientoDerecha = True
                    self.numeroDeMovimientosDerecha+= 5
                    
        for i in range(5):
            if all([self.columnas[x] for x in range(9, 8 - i, -1)]) and self.columnasVivas[9 - i]:
                self.columnasVivas[9 - i] = False
                self.moverDerecha += 5
                if self.direccion == 1:
                    self.moverIzquierda += 5
                else:
                    self.agregarMovimientoIzquierda = True
                    self.numeroDeMovimientosIzquierda += 5

    def cargar_imagenes(self):
        images = {0: ["1_2", "1_1"],
                  1: ["2_2", "2_1"],
                  2: ["2_2", "2_1"],
                  3: ["3_1", "3_2"],
                  4: ["3_1", "3_2"],
                 }
        img1, img2 = (IMAGES["enemigo{}".format(img_num)] for img_num in images[self.fila])
        self.images.append(transform.scale(img1, (40, 35)))
        self.images.append(transform.scale(img2, (40, 35)))


class Bloque(sprite.Sprite):
    def __init__(self, dimension, color, fila, columna):
       sprite.Sprite.__init__(self)
       self.altura = dimension
       self.anchura = dimension
       self.color = color
       self.image = Surface((self.anchura, self.altura))
       self.image.fill(self.color)
       self.rect = self.image.get_rect()
       self.fila = fila
       self.columna = columna

    def update(self, tecla, *args):
        game.screen.blit(self.image, self.rect)


class Bonus(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = IMAGES["bonus"]
        self.image = transform.scale(self.image, (75, 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.fila = 5
        self.cambiarTiempo = 25000
        self.direccion = 1
        self.contador = time.get_ticks()
        self.naveBonus = mixer.Sound('sonidos/entradabonus.wav')
        self.naveBonus.set_volume(0.3)
        self.iniciarSonido = True

    def update(self, tecla, horaActual, *args):
        reiniciarcontador = False
        if (horaActual - self.contador > self.cambiarTiempo) and (self.rect.x < 0 or self.rect.x > 800) and self.iniciarSonido:
            self.naveBonus.play()
            self.iniciarSonido = False
        if (horaActual - self.contador > self.cambiarTiempo) and self.rect.x < 840 and self.direccion == 1:
            self.naveBonus.fadeout(4000)
            self.rect.x += 2
            game.screen.blit(self.image, self.rect)
        if (horaActual - self.contador > self.cambiarTiempo) and self.rect.x > -100 and self.direccion == -1:
            self.naveBonus.fadeout(4000)
            self.rect.x -= 2
            game.screen.blit(self.image, self.rect)
        if (self.rect.x > 830):
            self.iniciarSonido = True
            self.direccion = -1
            reiniciarcontador = True
        if (self.rect.x < -90):
            self.iniciarSonido = True
            self.direccion = 1
            reiniciarcontador = True
        if (horaActual - self.contador > self.cambiarTiempo) and reiniciarcontador:
            self.contador = horaActual

    
class Explosion(sprite.Sprite):
    def __init__(self, xpos, ypos, fila, nave, mystery, score):
        sprite.Sprite.__init__(self)
        self.isMystery = mystery
        self.isnave = nave
        if mystery:
            self.text = Texto(FONDO, 20, str(score), BLANCO, xpos+20, ypos+6)
        elif nave:
            self.image = IMAGES["nave"]
            self.rect = self.image.get_rect(topleft=(xpos, ypos))
        else:
            self.fila = fila
            self.carga_imagen()
            self.image = transform.scale(self.image, (40, 35))
            self.rect = self.image.get_rect(topleft=(xpos, ypos))
            game.screen.blit(self.image, self.rect)
            
        self.contador = time.get_ticks()
        
    def update(self, tecla, horaActual):
        if self.isMystery:
            if horaActual - self.contador <= 200:
                self.text.draw(game.screen)
            if horaActual - self.contador > 400 and horaActual - self.contador <= 600:
                self.text.draw(game.screen)
            if horaActual - self.contador > 600:
                self.kill()
        elif self.isnave:
            if horaActual - self.contador > 300 and horaActual - self.contador <= 600:
                game.screen.blit(self.image, self.rect)
            if horaActual - self.contador > 900:
                self.kill()
        else:
            if horaActual - self.contador <= 100:
                game.screen.blit(self.image, self.rect)
            if horaActual - self.contador > 100 and horaActual - self.contador <= 200:
                self.image = transform.scale(self.image, (50, 45))
                game.screen.blit(self.image, (self.rect.x-6, self.rect.y-6))
            if horaActual - self.contador > 400:
                self.kill()
    
    def carga_imagen(self):
        imgColors = ["morado", "azul", "azul", "verde", "verde"]
        self.image = IMAGES["explosion{}".format(imgColors[self.fila])]

            
class Vida(sprite.Sprite):
    def __init__(self, xpos, ypos):
        sprite.Sprite.__init__(self)
        self.image = IMAGES["nave"]
        self.image = transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        
    def update(self, tecla, *args):
        game.screen.blit(self.image, self.rect)


class Texto(object):
    def __init__(self, textFont, dimension, message, color, xpos, ypos):
        self.font = font.Font(textFont, dimension)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class SpaceInvaders(object):
    def __init__(self):
        mixer.pre_init(44100, -16, 1, 512)
        init()
        self.caption = display.set_caption('Space Invaders')
        self.screen = PANTALLA
        self.background = image.load('imagenes/fondo.jpg').convert()
        self.startGame = False
        self.mainScreen = True
        self.gameOver = False
        self.enemyposition = 65

    def reinicio(self, score, vidas):
        self.player = nave()
        self.playerGroup = sprite.Group(self.player)
        self.explosionsGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.mysterynave = Bonus()
        self.mysteryGroup = sprite.Group(self.mysterynave)
        self.enemyBullets = sprite.Group()
        self.reiniciar_vidas()
        self.crear_enemigos()
        self.allBlockers = sprite.Group(self.crear_bloques(0), self.crear_bloques(1), self.crear_bloques(2), self.crear_bloques(3))
        self.tecla = key.get_pressed()
        self.clock = time.Clock()
        self.contador = time.get_ticks()
        self.notecontador = time.get_ticks()
        self.navecontador = time.get_ticks()
        self.score = score
        self.vidas = vidas
        self.introducir_audio()
        self.introducir_texto()
        self.muertefila = -1
        self.muertecolumna = -1
        self.crearNuevaNave = False
        self.naveAlive = True
        self.muerteFormacion = [[0] * 10 for x in range(5)]

    def crear_bloques(self, number):
       blockerGroup = sprite.Group()
       for fila in range(4):
           for columna in range(9):
               blocker = Bloque(10, VERDE, fila, columna)
               blocker.rect.x = 50 + (200 * number) + (columna * blocker.anchura)
               blocker.rect.y = 450 + (fila * blocker.altura)
               blockerGroup.add(blocker)
       return blockerGroup

    def reiniciar_vidas(self):
        self.vida1 = Vida(715, 3)
        self.vida2 = Vida(742, 3)
        self.vida3 = Vida(769, 3)
        self.vidasGroup = sprite.Group(self.vida1, self.vida2, self.vida3)
        
    def introducir_audio(self):
        self.sounds = {}
        for sound_name in ["disparo", "disparo2", "invasormuerto", "bonusmuerto", "naveexplosion"]:
            self.sounds[sound_name] = mixer.Sound("sonidos/{}.wav".format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.musicNotes = [mixer.Sound("sonidos/{}.wav".format(i)) for i in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.5)

        self.noteindice = 0

    def reproducir_musica_principal(self, horaActual):
        cambiarTiempo = self.enemies.sprites()[0].cambiarTiempo
        if horaActual - self.notecontador > cambiarTiempo:
            self.note = self.musicNotes[self.noteindice]
            if self.noteindice < 3:
                self.noteindice += 1
            else:
                self.noteindice = 0

            self.note.play()
            self.notecontador += cambiarTiempo

    def introducir_texto(self):
        self.titleText = Texto(FONDO, 50, "Space Invaders", BLANCO, 164, 155)
        self.titleText2 = Texto(FONDO, 25, "Presiona una tecla para continuar", BLANCO, 125, 225)
        self.gameOverText = Texto(FONDO, 50, "Fin Del Juego", BLANCO, 200, 270)
        self.nextRoundText = Texto(FONDO, 50, "Siguiente Nivel", BLANCO, 150, 270)
        self.enemy1Text = Texto(FONDO, 25, "   =   10 pts", VERDE, 368, 270)
        self.enemy2Text = Texto(FONDO, 25, "   =  20 pts", AZUL, 368, 320)
        self.enemy3Text = Texto(FONDO, 25, "   =  30 pts", MORADO, 368, 370)
        self.enemy4Text = Texto(FONDO, 25, "   =  ?????", ROJO, 368, 420)
        self.scoreText = Texto(FONDO, 20, "Puntaje", BLANCO, 5, 5)
        self.vidasText = Texto(FONDO, 20, "Vidas", BLANCO, 640, 5)
        
    def comprobar_entrada(self):
        self.tecla = key.get_pressed()
        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.bullets) == 0 and self.naveAlive:
                        if self.score < 1000:
                            bullet = Proyectil(self.player.rect.x+23, self.player.rect.y+5, -1, 15, "laser", "center")
                            self.bullets.add(bullet)
                            self.allSprites.add(self.bullets)
                            self.sounds["disparo"].play()
                        else:
                            leftbullet = Proyectil(self.player.rect.x+8, self.player.rect.y+5, -1, 15, "laser", "izquierda")
                            rightbullet = Proyectil(self.player.rect.x+38, self.player.rect.y+5, -1, 15, "laser", "derecha")
                            self.bullets.add(leftbullet)
                            self.bullets.add(rightbullet)
                            self.allSprites.add(self.bullets)
                            self.sounds["disparo2"].play()

    def crear_enemigos(self):
        enemigos = sprite.Group()
        for fila in range(5):
            for columna in range(10):
                enemy = Enemigo(fila, columna)
                enemy.rect.x = 157 + (columna * 50)
                enemy.rect.y = self.enemyposition + (fila * 45)
                enemigos.add(enemy)
        
        self.enemies = enemigos
        self.allSprites = sprite.Group(self.player, self.enemies, self.vidasGroup, self.mysterynave)

    def crear_disparo_enemigo(self):
        columnaList = []
        for enemigo in self.enemies:
            columnaList.append(enemigo.columna)

        columnaSet = set(columnaList)
        columnaList = list(columnaSet)
        shuffle(columnaList)
        columna = columnaList[0]
        enemyList = []
        filaList = []

        for enemigo in self.enemies:
            if enemigo.columna == columna:
                filaList.append(enemigo.fila)
        fila = max(filaList)
        for enemigo in self.enemies:
            if enemigo.columna == columna and enemigo.fila == fila:
                if (time.get_ticks() - self.contador) > 700:
                    self.enemyBullets.add(Proyectil(enemigo.rect.x + 14, enemigo.rect.y + 20, 1, 5, "enemigolaser", "center"))
                    self.allSprites.add(self.enemyBullets)
                    self.contador = time.get_ticks() 

    def calcular_puntaje(self, fila):
        scores = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                 }
                      
        score = scores[fila]
        self.score += score
        return score

    def crear_menu_principal(self):
        self.enemy1 = IMAGES["enemigo3_1"]
        self.enemy1 = transform.scale(self.enemy1 , (40, 40))
        self.enemy2 = IMAGES["enemigo2_2"]
        self.enemy2 = transform.scale(self.enemy2 , (40, 40))
        self.enemy3 = IMAGES["enemigo1_2"]
        self.enemy3 = transform.scale(self.enemy3 , (40, 40))
        self.enemy4 = IMAGES["bonus"]
        self.enemy4 = transform.scale(self.enemy4 , (80, 40))
        self.screen.blit(self.enemy1, (318, 270))
        self.screen.blit(self.enemy2, (318, 320))
        self.screen.blit(self.enemy3, (318, 370))
        self.screen.blit(self.enemy4, (299, 420))

        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYUP:
                self.startGame = True
                self.mainScreen = False
    
    def actualizar_velocidad_enemigos(self):
        if len(self.enemies) <= 10:
            for enemy in self.enemies:
                enemy.cambiarTiempo = 400
        if len(self.enemies) == 1:
            for enemy in self.enemies:
                enemy.cambiarTiempo = 200
                
    def comprobar_colision(self):
        collidedict = sprite.groupcollide(self.bullets, self.enemyBullets, True, False)
        if collidedict:
            for value in collidedict.values():
                for currentSprite in value:
                    self.enemyBullets.remove(currentSprite)
                    self.allSprites.remove(currentSprite)

        enemiesdict = sprite.groupcollide(self.bullets, self.enemies, True, False)
        if enemiesdict:
            for value in enemiesdict.values():
                for currentSprite in value:
                    self.sounds["invasormuerto"].play()
                    self.muertefila = currentSprite.fila
                    self.muertecolumna = currentSprite.columna
                    score = self.calcular_puntaje(currentSprite.fila)
                    explosion = Explosion(currentSprite.rect.x, currentSprite.rect.y, currentSprite.fila, False, False, score)
                    self.explosionsGroup.add(explosion)
                    self.allSprites.remove(currentSprite)
                    self.enemies.remove(currentSprite)
                    self.gamecontador = time.get_ticks()
                    break
        
        mysterydict = sprite.groupcollide(self.bullets, self.mysteryGroup, True, True)
        if mysterydict:
            for value in mysterydict.values():
                for currentSprite in value:
                    currentSprite.naveBonus.stop()
                    self.sounds["bonusmuerto"].play()
                    score = self.calcular_puntaje(currentSprite.fila)
                    explosion = Explosion(currentSprite.rect.x, currentSprite.rect.y, currentSprite.fila, False, True, score)
                    self.explosionsGroup.add(explosion)
                    self.allSprites.remove(currentSprite)
                    self.mysteryGroup.remove(currentSprite)
                    newnave = Bonus()
                    self.allSprites.add(newnave)
                    self.mysteryGroup.add(newnave)
                    break

        bulletsdict = sprite.groupcollide(self.enemyBullets, self.playerGroup, True, False)     
        if bulletsdict:
            for value in bulletsdict.values():
                for playernave in value:
                    if self.vidas == 3:
                        self.vidas -= 1
                        self.vidasGroup.remove(self.vida3)
                        self.allSprites.remove(self.vida3)
                    elif self.vidas == 2:
                        self.vidas -= 1
                        self.vidasGroup.remove(self.vida2)
                        self.allSprites.remove(self.vida2)
                    elif self.vidas == 1:
                        self.vidas -= 1
                        self.vidasGroup.remove(self.vida1)
                        self.allSprites.remove(self.vida1)
                    elif self.vidas == 0:
                        self.gameOver = True
                        self.startGame = False
                    self.sounds["naveexplosion"].play()
                    explosion = Explosion(playernave.rect.x, playernave.rect.y, 0, True, False, 0)
                    self.explosionsGroup.add(explosion)
                    self.allSprites.remove(playernave)
                    self.playerGroup.remove(playernave)
                    self.crearNuevaNave = True
                    self.navecontador = time.get_ticks()
                    self.naveAlive = False

        if sprite.groupcollide(self.enemies, self.playerGroup, True, True):
            self.gameOver = True
            self.startGame = False

        sprite.groupcollide(self.bullets, self.allBlockers, True, True)
        sprite.groupcollide(self.enemyBullets, self.allBlockers, True, True)
        sprite.groupcollide(self.enemies, self.allBlockers, False, True)

    def crear_nueva_nave(self, createnave, horaActual):
        if createnave and (horaActual - self.navecontador > 900):
            self.player = nave()
            self.allSprites.add(self.player)
            self.playerGroup.add(self.player)
            self.crearNuevaNave = False
            self.naveAlive = True

    def fin_del_juego(self, horaActual):
        self.screen.blit(self.background, (0,0))
        if horaActual - self.contador < 750:
            self.gameOverText.draw(self.screen)
        if horaActual - self.contador > 750 and horaActual - self.contador < 1500:
            self.screen.blit(self.background, (0,0))
        if horaActual - self.contador > 1500 and horaActual - self.contador < 2250:
            self.gameOverText.draw(self.screen)
        if horaActual - self.contador > 2250 and horaActual - self.contador < 2750:
            self.screen.blit(self.background, (0,0))
        if horaActual - self.contador > 3000:
            self.mainScreen = True
        
        for e in event.get():
            if e.type == QUIT:
                sys.exit()

    def main(self):
        while True:
            if self.mainScreen:
                self.reinicio(0, 3)
                self.screen.blit(self.background, (0,0))
                self.titleText.draw(self.screen)
                self.titleText2.draw(self.screen)
                self.enemy1Text.draw(self.screen)
                self.enemy2Text.draw(self.screen)
                self.enemy3Text.draw(self.screen)
                self.enemy4Text.draw(self.screen)
                self.crear_menu_principal()

            elif self.startGame:
                if len(self.enemies) == 0:
                    horaActual = time.get_ticks()
                    if horaActual - self.gamecontador < 3000:              
                        self.screen.blit(self.background, (0,0))
                        self.scoreText2 = Texto(FONDO, 20, str(self.score), VERDE, 115, 5)
                        self.scoreText.draw(self.screen)
                        self.scoreText2.draw(self.screen)
                        self.nextRoundText.draw(self.screen)
                        self.vidasText.draw(self.screen)
                        self.vidasGroup.update(self.tecla)
                        self.comprobar_entrada()
                    if horaActual - self.gamecontador > 3000:
                        self.reinicio(self.score, self.vidas)
                        self.enemyposition += 35
                        self.crear_enemigos()
                        self.gamecontador += 3000
                else:
                    horaActual = time.get_ticks()
                    self.reproducir_musica_principal(horaActual)              
                    self.screen.blit(self.background, (0,0))
                    self.allBlockers.update(self.screen)
                    self.scoreText2 = Texto(FONDO, 20, str(self.score), VERDE, 115, 5)
                    self.scoreText.draw(self.screen)
                    self.scoreText2.draw(self.screen)
                    self.vidasText.draw(self.screen)
                    self.comprobar_entrada()
                    self.allSprites.update(self.tecla, horaActual, self.muertefila, self.muertecolumna, self.muerteFormacion)
                    self.explosionsGroup.update(self.tecla, horaActual)
                    self.comprobar_colision()
                    self.crear_nueva_nave(self.crearNuevaNave, horaActual)
                    self.actualizar_velocidad_enemigos()

                    if len(self.enemies) > 0:
                        self.crear_disparo_enemigo()
    
            elif self.gameOver:
                horaActual = time.get_ticks()
                self.fin_del_juego(horaActual)

            display.update()
            self.clock.tick(60)
                

if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()