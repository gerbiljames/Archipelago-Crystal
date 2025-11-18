from BaseClasses import MultiWorld

from .Locations import finish_platform

required_cluster_per_button = {
    (13,1): [3, 11, 14, 15, 23, 24, 27],
    (16,1): [2, 17, 28],
    (18,1): [8],
    (22,1): [3, 11, 12, 20, 30],
}

required_cluster_per_platform = {
    (7,3): [6],
    (7,4): [6],
    (10,2): [6,9],
    (13,1): [3, 11, 14, 15, 23, 24, 27],
    (13,2): [3, 11, 14, 15, 23, 24, 27],
    (13,3): [3, 11, 14, 15, 23, 24, 27],
    (13,4): [3, 11, 14, 15, 23, 24, 27],
    (14,2): [13],
    (16,1): [2, 17, 28],
    (16,2): [2, 17, 28],
    (16,3): [2, 17, 28],
    (18,4): [5],
    (18,5): [5],
    (18,6): [5],
    (18,7): [5],
    (18,9): [5],
    (18,10): [5],
    (18,3): [6],
    (18,1): [8],
    (22,2): [3, 11, 12, 20, 30],
    (29,1): [25],
    (29,2): [25],
}






def set_refunct_rules(world: MultiWorld, player: int):
    for location in world.get_locations(player):  
        if location.name.startswith("Button"):
            parts = location.name.split("Button ")[1].split("-")
            cluster_nr = int(parts[0])
            button_nr = int(parts[1])
            required_clusters = []
            if (cluster_nr, button_nr) in required_cluster_per_button:
                required_clusters = required_cluster_per_button[(cluster_nr, button_nr)]
            location.access_rule = lambda state, player=player, cluster_nr=cluster_nr, button_nr=button_nr, required_clusters=required_clusters: all([
                state.has(f"Trigger Cluster {cluster_nr}", player, 1) or cluster_nr == 1,
                any(state.has(f"Trigger Cluster {i}", player, 1) for i in required_clusters) or not required_clusters
            ])
        elif location.name.startswith("Platform"):
            parts = location.name.split("Platform ")[1].split("-")
            cluster_nr = int(parts[0])
            platform_nr = int(parts[1])
            required_clusters = []
            if (cluster_nr, platform_nr) in required_cluster_per_platform:
                required_clusters = required_cluster_per_platform[(cluster_nr, platform_nr)]
            if (cluster_nr, platform_nr) == finish_platform:
                location.access_rule = lambda state, player=player, cluster_nr=cluster_nr, platform_nr=platform_nr, required_clusters=required_clusters: \
                    all(
                        [
                            state.has(f"Trigger Cluster {cluster_nr}", player, 1) or cluster_nr == 1,
                            any(state.has(f"Trigger Cluster {i}", player, 1) for i in required_clusters) or not required_clusters,
                            state.has("Grass", player, 100)
                        ]
                    )
            else:
                location.access_rule = lambda state, player=player, cluster_nr=cluster_nr, platform_nr=platform_nr, required_clusters=required_clusters: \
                    all(
                        [
                            state.has(f"Trigger Cluster {cluster_nr}", player, 1) or cluster_nr == 1,
                            any(state.has(f"Trigger Cluster {i}", player, 1) for i in required_clusters) or not required_clusters
                        ]
                    )
            

def set_refunct_completion(world: MultiWorld, player: int):
    world.completion_condition[player] = lambda state: all([state.has("Victory Location", player), state.has("Grass", player, 100)])
    