import pygame
import random

# Tenta carregar a imagem que o Flask baixou
try:
    imagem_pet = pygame.image.load("pet_atual.png")
    imagem_pet = pygame.transform.scale(imagem_pet, (50, 50))
except:
    imagem_pet = None # Caso falhe, usa o quadrado azul

# Inicialização
pygame.init()
LARGURA, ALTURA = 800, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cão Saltador")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)      # O Cão
VERMELHO = (255, 0, 0)  # Obstáculo
AMARELO = (255, 215, 0) # Osso

# Configurações do Cão
dog_largura, dog_altura = 50, 50
dog_x = 50
dog_y = ALTURA - dog_altura - 10
gravidade = 0.8
pulo_altura = -15
velocidade_y = 0
esta_pulando = False

# Listas de objetos
obstaculos = []
ossos = []
velocidade_jogo = 5
pontos = 0
clock = pygame.time.Clock()

def criar_objeto():
    if random.randint(0, 100) < 2: # Chance de criar obstáculo
        obstaculos.append(pygame.Rect(LARGURA, ALTURA - 40 - 10, 30, 40))
    if random.randint(0, 100) < 1: # Chance de criar osso
        ossos.append(pygame.Rect(LARGURA, ALTURA - 80, 20, 20))

rodando = True
while rodando:
    tela.fill(BRANCO)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not esta_pulando:
                velocidade_y = pulo_altura
                esta_pulando = True

    # Física do Pulo
    velocidade_y += gravidade
    dog_y += velocidade_y
    if dog_y >= ALTURA - dog_altura - 10:
        dog_y = ALTURA - dog_altura - 10
        esta_pulando = False

    # Desenhar Cão
    dog_rect = pygame.Rect(dog_x, dog_y, dog_largura, dog_altura)
    pygame.draw.rect(tela, AZUL, dog_rect)

    # Gerir Objetos
    criar_objeto()
    
    # Movimentar e desenhar Obstáculos
    for obs in obstaculos[:]:
        obs.x -= velocidade_jogo
        pygame.draw.rect(tela, VERMELHO, obs)
        if dog_rect.colliderect(obs):
            print(f"Game Over! Pontos: {pontos}")
            rodando = False
        if obs.x < -30: obstaculos.remove(obs)

    # Movimentar e desenhar Ossos
    for osso in ossos[:]:
        osso.x -= velocidade_jogo
        pygame.draw.rect(tela, AMARELO, osso)
        if dog_rect.colliderect(osso):
            pontos += 1
            ossos.remove(osso)
        if osso.x < -20: ossos.remove(osso)

    # Mostrar Pontuação
    fonte = pygame.font.SysFont("Arial", 24)
    texto = fonte.render(f"Ossos: {pontos}", True, (0,0,0))
    tela.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
 