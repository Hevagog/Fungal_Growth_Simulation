import math
import random


class Fungi:
    def __init__(self):
        self.spores = []
        self.hyphae = []

    def add_hypha(self, hypha):
        self.hyphae.append(hypha)

    def add_spore(self, spore):
        self.spores.append(spore)

    def kill_hypha(self, hypha):
        self.hyphae.remove(hypha)

    def kill_spore(self, spore):
        self.spores.remove(spore)

    def update(self):
        for spore in self.spores:
            spore.update()
            if not spore.is_alive:
                self.kill_spore(spore)
            if spore.reproduce:
                self.add_hypha(
                    Hypha(origin_x=spore.origin_x, origin_y=spore.origin_y))
                spore.reproduce = False

        for hypha in self.hyphae:
            hypha.update()
            if not hypha.is_alive:
                self.kill_hypha(hypha)
            elif hypha.reproduce:
                self.add_hypha(
                    Hypha(origin_x=hypha.tip_x, origin_y=hypha.tip_y))
                hypha.reproduce = False


class Spore:
    def __init__(self, origin_x, origin_y, growth_probability=0.02, death_probability=0.0005, S_0=5000):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.growth_probability = growth_probability
        self.death_probability = death_probability
        self.S = S_0
        self.reproduce = False
        self.is_alive = True

    def update(self):
        if random.random() < self.death_probability:
            self.is_alive = False
            return
        if random.random() < self.growth_probability:
            self.reproduce = True


class Hypha:
    def __init__(self, origin_x, origin_y, initial_tip_extension_rate=80, max_extension_rate=5,
                 branching_probability=0.02, substrate_concentration_at_origin=50000, k_t=5, k_s=200,
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
        self.is_alive = True
        self.reproduce = False
        self.angle = random.uniform(0, 2 * math.pi)
        self.tip_x = origin_x + unit_radius * math.cos(self.angle)
        self.tip_y = origin_y + unit_radius * math.sin(self.angle)

    def grow_direction(self):
        extension_coefficient = self.calc_tip_extension_rate()
        self.tip_x += self.unit_radius * \
            extension_coefficient * math.cos(self.angle)
        self.tip_y += self.unit_radius * \
            extension_coefficient * math.sin(self.angle)

    def calc_branch_length(self):
        return math.sqrt((self.tip_x - self.origin_x) ** 2 + (self.tip_y - self.origin_y) ** 2)

    def calc_tip_extension_rate(self):
        l_bri = self.calc_branch_length()
        return (self.k_tip2 * l_bri / (l_bri * self.k_t)) * self.S / (self.S + self.k_s)

    def update(self):
        if random.random() < self.p_branch:
            self.reproduce = True
        if random.random() < self.p_death:
            self.is_alive = False
        else:
            self.grow_direction()
