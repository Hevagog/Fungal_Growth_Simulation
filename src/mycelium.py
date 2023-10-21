import math
import random

from . import config


class Fungi:
    # Fungi manages the spores and hyphae
    def __init__(self) -> None:
        self.spores = []
        self.hyphae = []

    def add_hypae(self, hyphae):
        self.hyphae.append(hyphae)

    def add_spore(self, spore):
        self.spores.append(spore)

    def kill_hyphae(self, hyphae):
        self.hyphae.remove(hyphae)

    def kill_spore(self, spore):
        self.spores.remove(spore)


class Spore:
    # Spore initiates a Hyphae object
    def __init__(self, position, growth_probability=0.01, death_probability=0.005):
        self.position = position
        self.growth_probability = growth_probability
        self.death_probability = death_probability
        self.is_alive = True

    def update(self):
        if random.random() < self.death_probability:
            self.is_alive = False
            return
        if random.random() < self.growth_probability:
            new_hyphae = Hyphae(self.position, self.k_tip1,
                                self.k_tip2, self.p_branch)


class Hyphae:
    def __init__(self, origin, initial_tip_extension_rate, max_extension_rate, branching_probability, death_probability=0.005):
        self.origin = origin
        self.tip = origin
        self.k_tip1 = initial_tip_extension_rate
        self.k_tip2 = max_extension_rate
        self.p_branch = branching_probability
        self.death_probability = death_probability
        self.is_alive = True
        # TODO: when init create branches with probability p_branch
        # Branching should create new Fungi object because calc extension rate will explode

    def calc_branch_length(self, tip):
        return math.sqrt((tip[0] - self.origin[0]) ** 2 + (tip[1] - self.origin[1]) ** 2)

    def calc_tip_extension_rate(self, k_t, k_s, S):
        l_bri = self.calc_branch_length(tip)
        return (self.k_tip2 * l_bri/(l_bri*k_t)) * S/(S+k_s)

    def update(self):
        if random.random() < self.p_branch:
            new_branch = Hyphae((self.origin[0], self.origin[1]), self.k_tip1,
                                self.k_tip2, self.p_branch, self.death_probability)
            return new_branch
        if random.random() < self.p_death:
            self.is_alive = False
        else:
            self.k_tip1 = self.calc_tip_extension_rate(
                config.k_t, config.k_s, config.s_0)
            self.origin[0] += self.k_tip1
