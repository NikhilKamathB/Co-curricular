import random
import itertools
import numpy as np
import matplotlib.pyplot as plt

# remove h
# add time 
# make  plans for every t seconds


world = [100, 100]
min_velocity_magnitude, max_velocity_magnitude = 0, 1
heading_limit = np.pi/6
goal_state = [random.random()*world[0], random.random()*world[1]]
goal_aware_sphere_radius = 10
ego_state = [random.random()*world[0], random.random()*world[1]]
ego_heading = random.uniform(0, 2*np.pi)
ego_aware_sphere_radius = 30
player_aware_sphere_radius = 10
player_state = [random.random()*world[0], random.random()*world[1]]
player_heading = random.uniform(0, 2*np.pi)

# def correct_heading(p, v):
#     p_dash = [p[0]+v[0], p[1]+v[1]]
#     if (p_dash[0]*p_dash[1]) < 0 or (p_dash[0]<0 and p_dash[1]<0):
#         return np.arctan2(v[1], v[0])
#     return np.pi+np.arctan2(v[1], v[0])
#     # if p_dash[0] > world[0]:
#     #     p_dash[0] = world[0]-10
#     # elif p_dash[0] < world[0]:
#     #     p_dash[0] = 10
#     # if p_dash[1] > world[1]:
#     #     p_dash[1] = world[1]-10
#     # elif p_dash[1] < world[1]:
#     #     p_dash[1] = 10
#     # print(np.arctan2(p[1]-p_dash[1], p[0]-p_dash[0]) * (180/np.pi))
#     # return np.arctan2(p[1]-p_dash[1], p[0]-p_dash[0])


def movement_model(p_player, h_player):
    '''
    define movement model f~or player (not quad copter)
    input: p_player - player postion in the real world
           h_player - player heading in the real/local world
    output: tuple of desired position and desired velocity vector
    '''
    x_hat, y_hat = max_velocity_magnitude*np.cos(h_player), max_velocity_magnitude*np.sin(h_player)
    return ((p_player[0]+x_hat, p_player[1]+y_hat), (x_hat, y_hat))

def interaction_model(p_player, v_player, p_ego, v_ego):
    '''
    define movement model for player (not quad copter)
    input: p_player - player postion in the real world
           v_player - velocity vector of the player in the local world
           p_ego - ego position in the real world
           v_ego - velocity vector of the ego in the local worl
    output: tuple of distance to ego, actual position and actual velocity vector
    '''
    next_p_player = []
    h_player = np.arctan2(v_player[1], v_player[0])
    v_player_magnitude = np.linalg.norm(v_player)
    if h_player < 0: h_player = 2*np.pi + h_player
    r_h_player = [_ % (2*np.pi) if _ >= 2*np.pi else _ for _ in np.linspace(h_player-heading_limit, h_player+heading_limit, 10)] + [h_player]
    try:
        # if (p_player[0] - p_ego[0]) ** 2 - (p_player[1] - p_ego[1]) ** 2 <= player_aware_sphere_radius ** 2:
        next_p_ego = (p_ego[0]+v_ego[0], p_ego[1]+v_ego[1])
        for heading in r_h_player:
            x_hat, y_hat = v_player_magnitude*np.cos(heading), v_player_magnitude*np.sin(heading)
            p_player_dash = (p_player[0]+x_hat, p_player[1]+y_hat)
            d_player_ego = ((p_player_dash[0]-next_p_ego[0])**2 + (p_player_dash[1]-next_p_ego[1])**2)**0.5
            next_p_player.append((d_player_ego, p_player_dash, (x_hat, y_hat)))
        next_p_player = sorted(next_p_player, key=lambda x: x[0], reverse=True) 
        return next_p_player[0]
        # else:
        #     for heading in r_h_player:
        #         x_hat, y_hat = v_player_magnitude*np.cos(heading), v_player_magnitude*np.sin(heading)
        #         p_player_dash = (p_player[0]+x_hat, p_player[1]+y_hat)
        #         next_p_player.append((None, p_player_dash, (x_hat, y_hat)))
        #     return random.choice(next_p_player)
    except Exception as e:
        print(e)
        import pdb; pdb.set_trace()

def heuristic(p_player, p_ego):
    d_player_goal = ((p_player[0]-goal_state[0])**2 + (p_player[1]-goal_state[1])**2)**0.5
    d_player_ego = ((p_player[0]-p_ego[0])**2 + (p_player[1]-p_ego[1])**2)**0.5
    return d_player_goal + d_player_ego

def ego_model_next_state(p_player, v_player, p_ego, v_ego):
    h_player = np.arctan2(v_player[1], v_player[0])
    v_player_magnitude = np.linalg.norm(v_player)
    if h_player < 0: h_player = 2*np.pi + h_player
    r_h_player = [_ % (2*np.pi) if _ >= 2*np.pi else _ for _ in np.linspace(h_player-heading_limit, h_player+heading_limit, 10)] + [h_player]
    worst_state, state = -np.inf, None
    p_ego_dash = (p_ego[0]+v_ego[0], p_ego[1]+v_ego[1])
    for heading in r_h_player:
        x_hat, y_hat = v_player_magnitude*np.cos(heading), v_player_magnitude*np.sin(heading)
        p_player_dash = (p_player[0]+x_hat, p_player[1]+y_hat)
        d_ego_player = ((p_player_dash[0]-p_ego_dash[0])**2 + (p_player_dash[1]-p_ego_dash[1])**2)**0.5
        if d_ego_player > worst_state:
            worst_state = d_ego_player
            state = (p_player_dash, [x_hat, y_hat], p_ego_dash)
    return state

def ego_model_tree(depth, state, r_h_ego, r_du_ego):
    p_player, v_player, p_ego = state
    if depth == 0: return (heuristic(p_player, p_ego), None)
    best_velocity_duration = None
    v = np.inf
    for h, du in list(itertools.product(r_h_ego, r_du_ego)):
        v_ego = (5*np.cos(h), 5*np.sin(h))
        score, _ = ego_model_tree(
            depth=depth-1,
            state=ego_model_next_state(p_player, v_player, p_ego, v_ego),
            r_h_ego=r_h_ego,
            r_du_ego=r_du_ego
        )
        if score < v:
            v = score
            best_velocity_duration = (v_ego, du)
    return (v, best_velocity_duration)

def ego_model(p_player, p_player_previous, p_ego, depth=3):
    '''
    define search space for ego vehicle (quad copter)
    input: p_player - player postion in the real world
           p_ego - ego position in the real world
    output: expected velocity of the ego vehicle with duration
    '''
    v_player = (p_player[0]-p_player_previous[0], p_player[1]-p_player_previous[1])
    # if (p_player[0] - p_ego[0]) ** 2 - (p_player[1] - p_ego[1]) ** 2 <= ego_aware_sphere_radius ** 2:
    r_h_ego = list(set([_*(np.pi/180) for _ in range(0, 360, 30)] + [_*(np.pi/180) for _ in range(45, 360, 45)]))
    r_du_ego = [1]
    _, velocity_duration = ego_model_tree(
        depth=depth,
        state=(p_player, v_player, p_ego),
        r_h_ego=r_h_ego,
        r_du_ego=r_du_ego
    )
    v_ego, _ = velocity_duration
    print('EM 1 ', p_ego, 'EM 1 pp', p_player)
    # else:
    #     h_ego_expected = np.arctan2(p_ego[0]-p_player[0], p_ego[1]-p_player[1])
    #     v_ego = (5*np.cos(h_ego_expected), 5*np.sin(h_ego_expected))
    #     print('EM 2 ', p_ego, 'EM 2 vel ', v_ego)
    return ((p_ego[0]+v_ego[0], p_ego[1]+v_ego[1]), v_ego)


def simulate():
    p_player_plot = []
    v_player_plot = []
    # p_player, p_heading = player_state, player_heading
    p_player, p_heading = [50, 50], np.pi/2
    # p_ego, v_ego = ego_state, [np.cos(ego_heading), np.sin(ego_heading)]
    p_ego, v_ego = [40, 40], [0, 1]
    reached_goal_state = False
    ctr = 0
    while not reached_goal_state:
        ctr += 1
        p_player_previous = p_player
        p_player_plot.append(p_player_previous)
        v_player_plot.append(p_ego)
        print(ctr, '---', p_ego)
        _, v_player = movement_model(p_player, p_heading)
        _, p_player, v_player = interaction_model(p_player, v_player, p_ego, v_ego)
        p_heading = np.arctan2(v_player[1], v_player[0])
        p_ego, v_ego = ego_model(p_player, p_player_previous, p_ego)
        print(ctr, '--end-', p_ego)
        if ctr == 50:
            break
    x = np.asarray(p_player_plot)
    y = np.asarray(v_player_plot)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid()
    plt.plot(x[:, 0], x[:, 1], '--bo', label='line with marker')
    plt.plot(y[:, 0], y[:, 1], '--ro', label='line with marker')
    plt.plot(goal_state[0], goal_state[1], marker="o", markersize=10,markerfacecolor="green")
    plt.plot(x[-1,0], x[-1, 1], marker="*", markersize=10,markerfacecolor="red")
    plt.plot(y[-1,0], y[-1, 1], marker="*", markersize=10,markerfacecolor="red")
    plt.show()



if __name__ == '__main__':
    simulate()