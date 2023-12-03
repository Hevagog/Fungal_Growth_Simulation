import math
import random

from . import helper as hlp
from . import config as cfg


class Fungi:
    def __init__(self):
        self.spores = []
        self.hyphae = []
        self.obstacles = []
        self.scarcities = []

    def add_hypha(self, hypha):
        self.hyphae.append(hypha)

    def add_scarcity(self, scarcity):
        self.scarcities.append(scarcity)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def add_spore(self, spore):
        self.spores.append(spore)

    def kill_hypha(self, hypha):
        self.hyphae.remove(hypha)

    def kill_spore(self, spore):
        self.spores.remove(spore)


class Spore:
    def __init__(self, origin_x, origin_y, substrate_concentration_at_origin, breed=0,
                 growth_probability=0.02, death_probability=0.0005, from_hypha=False):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.growth_probability = growth_probability
        self.death_probability = death_probability
        self.S = substrate_concentration_at_origin
        self.reproduce = False
        self.is_alive = True
        self.from_hypha = from_hypha
        self.breed_id = breed
        self.color = cfg.HYPHA_COLORS[self.breed_id]

    def update(self):
        if random.random() < self.death_probability:
            self.is_alive = False
            return
        if random.random() < self.growth_probability:
            self.reproduce = True


class Hypha:
    def __init__(self, origin_x, origin_y, substrate_concentration_at_origin, breed=0,
                 initial_tip_extension_rate=80, max_extension_rate=5,
                 branching_probability=0.02, k_t=5, k_s=200,
                 death_probability=0.0005, unit_radius=1):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.k_tip1 = initial_tip_extension_rate
        self.k_tip2 = max_extension_rate
        self.p_branch = branching_probability
        self.p_death = death_probability
        self.unit_radius = unit_radius
        self.S = substrate_concentration_at_origin
        self.k_t = k_t
        self.k_s = k_s
        self.breed_id = breed
        self.color = cfg.HYPHA_COLORS[self.breed_id]

        self.is_alive = True
        self.reproduce = False
        self.angle = random.uniform(0, 2 * math.pi)
        self.tip_x = self.origin_x + self.unit_radius * \
            math.cos(self.angle)
        self.tip_y = self.origin_y + self.unit_radius * \
            math.sin(self.angle)
        self.drain_points = hlp.calculate_points_on_line(
            (self.origin_x, self.origin_y), (self.tip_x, self.tip_y))

    def grow_direction(self):
        old_tip_x = self.tip_x
        old_tip_y = self.tip_y
        extension_coefficient = self.calc_tip_extension_rate()
        self.tip_x += self.unit_radius * \
            extension_coefficient * math.cos(self.angle)
        self.tip_y += self.unit_radius * \
            extension_coefficient * math.sin(self.angle)
        if self.tip_x >= cfg.SCREEN_WIDTH:
            self.tip_x = cfg.SCREEN_WIDTH - 1
        if self.tip_x <= 0:
            self.tip_x = 1
        if self.tip_y >= cfg.SCREEN_HEIGHT:
            self.tip_y = cfg.SCREEN_HEIGHT - 1
        if self.tip_y <= 0:
            self.tip_y = 1
        self.drain_points += hlp.calculate_points_on_line(
            (old_tip_x, old_tip_y), (self.tip_x, self.tip_y))

    def calc_branch_length(self):
        return math.sqrt((self.tip_x - self.origin_x) ** 2 + (self.tip_y - self.origin_y) ** 2)

    def calc_tip_extension_rate(self):
        l_bri = self.calc_branch_length()
        return hlp.extention_functions[self.breed_id](l_bri)
        # return (self.k_tip2 * l_bri / (l_bri * self.k_t)) * self.S / (self.S + self.k_s)

    def in_bounds(self):
        if self.tip_x <= 1 or self.tip_x >= cfg.SCREEN_WIDTH - 1 or self.tip_y <= 1 or self.tip_y >= cfg.SCREEN_HEIGHT-1:
            return False
        return True

    def update(self):
        if random.random() < self.p_death or self.S <= 0 or not self.in_bounds():
            self.is_alive = False

        if random.random() < self.p_branch and self.is_alive and self.in_bounds():
            self.reproduce = True

        if self.is_alive:
            self.grow_direction()
