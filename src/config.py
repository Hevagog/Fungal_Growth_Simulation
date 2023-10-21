initial_tip_extension_rate = 0
max_extension_rate = 0
branching_probability = 0
s_0 = 50000

simulation_params = {
    # Probability of branching event
    "p_branch": 0.05,

    # Probability of death event
    "p_death": 0.005,

    # Number of hyphae to start with (PL ilosc nitkowatych elementow, z ktorych zbudowana jest grzybnia- cialo grzybow)
    "M": 100000,

    # Number of iterations to run
    "N": 5000,

    # substrate concentration at start
    "s_0": 50000,  # unit: mg/L

    # time it takes to reach half of the maximum extension rate
    "k_t": 5,

    # substrate concentration to reach half of the maximum growth level
    "k_s": 200,  # unit: mg

    "fungi": {
        # Fungi name
        "Aspergillus oryzae": {
            "k_tip1": 80,  # initial tip extension rate of the branch
            "k_tip2": 75,  # difference between the maximum extension rate and the initial tip extension rate
        },

    }
}
