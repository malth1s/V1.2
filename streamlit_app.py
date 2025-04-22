import streamlit as st
import random

# ======================== Game Logic ========================
def initialize_game(num_players, seed=None):
    if seed is not None:
        random.seed(seed)

    all_players = [f"Player{i}" for i in range(1, num_players)]
    random.shuffle(all_players)
    zombie = all_players.pop(0)
    non_leader_players = all_players
    return zombie, non_leader_players

def form_groups(non_leader_players, zombie, group_sizes):
    players_with_zombie = non_leader_players + [zombie]
    random.shuffle(players_with_zombie)

    groups = []
    start = 0
    for size in group_sizes:
        groups.append(players_with_zombie[start:start + size])
        start += size
    return groups

def risk_round(round_number, zombie, non_leader_players, infected_players, infection_probability, group_sizes, infection_log):
    groups = form_groups(non_leader_players, zombie, group_sizes)
    new_infected = []

    st.subheader(f"🧟 Risk Round {round_number}")
    for group in groups:
        st.markdown(f"**Group:** {', '.join(group)}")
        group_has_infection = any(player in infected_players for player in group)

        if group_has_infection:
            healthy_candidates = [p for p in group if p not in infected_players]
            random.shuffle(healthy_candidates)
            for player in healthy_candidates:
                if random.random() < infection_probability:
                    infected_players.add(player)
                    infection_log[player] = round_number
                    new_infected.append(player)
                    break

        for player in group:
            status = "🧟‍♂️ Infected" if player in infected_players else "😎 Healthy"
            st.markdown(f"- {player}: {status}")

    if new_infected:
        st.warning(f"New infection: {new_infected[0]}!")
    else:
        st.success("No new infections this round!")

def mission_scan(round_number, infected_players, total_players):
    st.subheader(f"🔍 Mission {round_number}: Scan")
    st.info(f"Total Infected: {len(infected_players)} / {total_players - 1}")

def run_game(num_players, infection_probability, round_group_selection, seed):
    zombie, non_leader_players = initialize_game(num_players, seed)
    infected_players = {zombie}
    infection_log = {zombie: 0}

    st.success("Game Started! You are the Leader (Player0, immune to infection).")
    st.info(f"The original zombie is **{zombie}**.")

    for round_number in range(1, 9):
        group_sizes = round_group_selection.get(round_number, [])

        if round_number in [1, 3, 6]:
            risk_round(round_number, zombie, non_leader_players, infected_players, infection_probability, group_sizes, infection_log)

        elif round_number == 8:
            mission_scan(round_number, infected_players, num_players)

    st.subheader("📜 Final Infection Log")
    for player, rnd in infection_log.items():
        st.markdown(f"- {player} was infected in round {rnd}")

# ======================== Streamlit UI ========================
st.set_page_config(page_title="Turned: Zombie Game", page_icon="🧟", layout="wide")
st.title("🧟 Turned: The Infection Game")

with st.sidebar:
    st.header("Game Settings")
    num_players = st.slider("Number of players (you are Player0 / the Leader)", 5, 12, 10)
    infection_probability = st.slider("Infection probability", 0.1, 1.0, 0.3, 0.05)
    custom_seed = st.number_input("Seed (for reproducible randomness)", value=42)

round_group_selection = {
    1: [3, 3, 3],
    2: [4, 5],
    3: [2, 3, 4],
    4: [2, 2, 2, 2, 2],
    5: [3, 3, 3],
    6: [4, 5],
    7: [5, 5],
    8: [num_players - 1],
}

if st.button("🧪 Start Game!"):
    run_game(num_players, infection_probability, round_group_selection, custom_seed)
    st.balloons()
