import math
import pygame

pygame.init()

# Sabitler
WIDTH, HEIGHT = 800, 800  # Pencere boyutları
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
clock = pygame.time.Clock()

x_center = WIDTH // 2
y_center = HEIGHT // 2

# Font modülünü başlat
pygame.font.init()
font = pygame.font.Font(None, 36)  # Varsayılan font, 36 boyutunda

# Gezegen sınıfı
class Planet:
    def __init__(self, x_radius, y_radius, radius, color, orbit_speed, name, is_sun=False, parent=None):
        self.x_radius = x_radius  # Yörünge genişliği
        self.y_radius = y_radius  # Yörünge yüksekliği
        self.radius = radius  # Gezegenin boyutu
        self.color = color  # Gezegenin rengi
        self.orbit_speed = orbit_speed  # Yörüngedeki dönüş hızı
        self.name = name  # Gezegenin ismi
        self.angle = 0  # Gezegenin başlangıç açısı
        self.x = x_center + self.x_radius
        self.y = y_center
        self.is_sun = is_sun
        self.parent = parent  # Eğer bu gezegen bir başka gezegen etrafında dönüyorsa

    def update_position(self):
        """Gezegenin pozisyonunu günceller."""
        self.angle += self.orbit_speed
        if self.parent:  # Eğer başka bir gezegen etrafında dönüyorsa
            parent_x = self.parent.x
            parent_y = self.parent.y
            self.x = parent_x + self.x_radius * math.cos(math.radians(self.angle))
            self.y = parent_y + self.y_radius * math.sin(math.radians(self.angle))
        else:  # Güneş gibi sabit bir merkeze göre hareket
            self.x = x_center + self.x_radius * math.cos(math.radians(self.angle))
            self.y = y_center + self.y_radius * math.sin(math.radians(self.angle))

    def draw(self, WIN):
        """Gezegenin kendisini çizer."""
        pygame.draw.circle(WIN, self.color, (int(self.x), int(self.y)), self.radius)

    def draw_name(self, WIN):
        """Gezegenin ismini çizer."""
        text = font.render(self.name, True, (255, 255, 255))  # Beyaz renkli metin
        WIN.blit(text, (int(self.x) - text.get_width() // 2, int(self.y) - self.radius - 20))  # Gezegenin üstünde ortala

    def draw_ring(self, WIN):
        """Gezegenin halkasını çizer."""
        if self.color == (255, 215, 0):  # Sarı ise (Satürn için örnek)
            # Halka için elips çizimi
            pygame.draw.ellipse(WIN, (210, 180, 140),  # Halka rengi
                                (int(self.x) - self.radius * 2, int(self.y) - self.radius * 0.5,
                                 self.radius * 4, self.radius * 1.5), 1)

    def draw_orbital(self, WIN):
        """Gezegenin yörüngesini çizer."""
        if not self.is_sun:  # Eğer gezegen güneş değilse yörüngesini çiz
            if self.parent:  # Yörüngeyi, bağlı olduğu gezegene göre çiz
                pygame.draw.ellipse(WIN, (200, 200, 200),
                                     (int(self.parent.x - self.x_radius), int(self.parent.y - self.y_radius),
                                      2 * self.x_radius, 2 * self.y_radius), 1)
            else:  # Güneşe göre yörünge
                pygame.draw.ellipse(WIN, (200, 200, 200),
                                     (x_center - self.x_radius, y_center - self.y_radius,
                                      2 * self.x_radius, 2 * self.y_radius), 1)

# Ana döngü
def main():
    run = True

    sun = Planet(0, 0, 30, (255, 255, 0), 0, 'Güneş', is_sun=True)  # Güneş
    mercury = Planet(80, 80, 10, (139, 0, 0), 1.2, 'Merkür')  # Merkür
    earth = Planet(150, 100, 20, (0, 0, 255), 1, 'Dünya')  # Dünya
    moon = Planet(30, 20, 5, (255, 255, 255), 5, 'Ay', parent=earth)  # Ay (Dünya'nın etrafında)
    mars = Planet(200, 150, 15, (255, 0, 0), 0.5, 'Mars')  # Mars
    uranus = Planet(300, 300, 8, (222, 184, 135), 0.2, 'Uranüs')  # Uranüs
    saturn = Planet(350, 350, 25, (255, 215, 0), 0.1, 'Satürn')  # Satürn

    planets = [sun, mercury, earth, moon, mars, uranus, saturn]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Çıkış kontrolü
                run = False

        WIN.fill((0, 0, 0))  # Arka plan siyah

        for planet in planets:
            planet.draw_orbital(WIN)  # Gezegenin yörüngesini çiz
            planet.update_position()  # Gezegenin konumunu güncelle
            planet.draw(WIN)  # Gezegenin kendisini çiz
            planet.draw_name(WIN)  # Gezegenin ismini çiz
            planet.draw_ring(WIN)  # Halka çizimi (özellikle Satürn için)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()  # Pygame işlemlerini sonlandırma

main()
