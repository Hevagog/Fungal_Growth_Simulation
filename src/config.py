initial_tip_extension_rate = 0
max_extension_rate = 0
branching_probability = 0
# substrate concentration at start
s_0 = 50000
# time it takes to reach half of the maximum extension rate
k_t = 5
# substrate concentration to reach half of the maximum growth level
k_s = 200  # unit: mg

Aspergillus_oryzae = {
    "k_tip1": 80,  # initial tip extension rate of the branch
    "k_tip2": 75,  # difference between the maximum extension rate and the initial tip extension rate
}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
SPORE_COLOR = (0, 0, 255)
HYPHA_COLOR = (0, 255, 0)
