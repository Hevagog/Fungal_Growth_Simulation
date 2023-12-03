from src import simulation as sim

if __name__ == "__main__":
    sim.start(spores=3, num_of_obstacles=1,
              num_of_scarcity=4, scarcity_radius=50)
