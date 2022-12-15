import random
import itertools
import numpy as np
import matplotlib.pyplot as plt

t = 1000 # milliseconds
world = (100, 100)
h_list = list(set([_*(np.pi/180) for _ in range(0, 360, 30)] + [_*(np.pi/180) for _ in range(45, 360, 45)]))

min_velocity_magnitude_player, max_velocity_magnitude_player = 0, 1
min_velocity_magnitude_ego, max_velocity_magnitude_ego = 0, 5

goal_state = (random.random()*world[0], random.random()*world[1])
goal_aware_sphere_radius = 2.5

ego_state = (random.random()*world[0], random.random()*world[1])
ego_heading = random.uniform(0, 2*np.pi)
ego_aware_sphere_radius = 30

player_aware_sphere_radius = 10
player_state = (random.random()*world[0], random.random()*world[1])
player_heading = random.uniform(0, 2*np.pi)

def distance(x:tuple, y:tuple) -> float:
    '''
    calculates distance between two points
    input: x - (a, b)
           y - (c, d)
    output: distance between x and y
    '''
    return ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5

def movement_model(p_player:tuple, h_player:float) -> tuple:
    '''
    defines movement model for player (not quad copter)
    input: p_player - player postion in the real world
           h_player - player heading in the real/local world
    output: tuple of desired position and desired velocity vector
    '''
    x_hat, y_hat = max_velocity_magnitude_player*np.cos(h_player), max_velocity_magnitude_player*np.sin(h_player)
    return ((p_player[0]+(x_hat*t*1e-3), p_player[1]+(y_hat*t*1e-3)), (x_hat, y_hat))

def interaction_model(p_player:tuple, v_player:tuple, p_ego:tuple, v_ego:tuple) -> tuple:
    '''
    defines interaction model for player (not quad copter)
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
    r_h_player = [_ % (2*np.pi) if _ >= 2*np.pi else _ for _ in np.linspace(0, 2*np.pi, 36)] + [h_player]
    next_p_ego = (p_ego[0]+(v_ego[0]*t*1e-3), p_ego[1]+(v_ego[1]*t*1e-3))
    for heading in r_h_player:
        x_hat, y_hat = v_player_magnitude*np.cos(heading), v_player_magnitude*np.sin(heading)
        p_player_dash = (p_player[0]+(x_hat*t*1e-3), p_player[1]+(y_hat*t*1e-3))
        if p_player_dash[0] >= 0 and p_player_dash[0] <= world[0] and p_player_dash[1] >= 0 and p_player_dash[1] <= world[1]:
            d_player_ego = distance(p_player_dash, next_p_ego)
            next_p_player.append((d_player_ego, p_player_dash, (x_hat, y_hat)))
    if not next_p_player:
        p_player_dash = (min(max(0, p_player[0]), world[0]), min(max(0, p_player[1]), world[1]))
        h_player = np.arctan2(p_player[1]-p_player_dash[1], p_player[0]-p_player_dash[0])
        x_hat, y_hat = v_player_magnitude*np.cos(heading), v_player_magnitude*np.sin(heading)
        d_player_ego = distance(p_player_dash, next_p_ego)
        next_p_player.append((d_player_ego, p_player_dash, (x_hat, y_hat)))
    next_p_player = sorted(next_p_player, key=lambda x: x[0], reverse=True) 
    return next_p_player[0]

def heuristic(p_player:tuple, p_ego:tuple) -> float:
    '''
    calculates heuristic for every state of the quad copter
    input: p_player - player postion in the real world
           p_ego - ego position in the real world
    output: a state value estimation
    '''
    d_player_goal = distance(p_player, goal_state)
    d_player_ego = distance(p_player, p_ego)
    return d_player_goal + d_player_ego

def ego_model_next_state(p_player:tuple, v_player:tuple, p_ego:tuple, v_ego:tuple) -> tuple:
    '''
    generates the next state of the quad copter
    input: p_player - player postion in the real world
           v_player - velocity vector of the player in the local world
           p_ego - ego position in the real world
           v_ego - velocity vector of the ego in the local world
           a tuple containing player position, player velocity and ego position
    output:
    '''
    h_player = np.arctan2(v_player[1], v_player[0])
    v_player_magnitude = np.linalg.norm(v_player)
    if h_player < 0: h_player = 2*np.pi + h_player
    r_h_player = [_ % (2*np.pi) if _ >= 2*np.pi else _ for _ in np.linspace(0, 2*np.pi, 36)] + [h_player]
    worst_state, state = -np.inf, None
    p_ego_dash = (p_ego[0]+(v_ego[0]*t*1e-3), p_ego[1]+(v_ego[1]*t*1e-3))
    for heading in r_h_player:
        x_hat, y_hat = v_player_magnitude*np.cos(heading), v_player_magnitude*np.sin(heading)
        p_player_dash = (p_player[0]+(x_hat*t*1e-3), p_player[1]+(y_hat*t*1e-3))
        if p_player_dash[0] >= 0 and p_player_dash[0] <= world[0] and p_player_dash[1] >= 0 and p_player_dash[1] <= world[1]:
            d_ego_player = distance(p_player_dash, p_ego_dash)
            if d_ego_player > worst_state:
                worst_state = d_ego_player
                state = (p_player_dash, [x_hat, y_hat], p_ego_dash)
    return state

def ego_model_tree(depth:int, state:tuple, r_h_ego:list, r_du_ego:list) -> tuple:
    '''
    generates the tree of states for the quad copter
    input: depth - max depth of the tree
           state - a tuple containing player position, player velocity and ego position
           r_h_ego - possible range of heading angles
           r_du_ego - possible duration for volocity execution
    output: tuple of state value and the best possible velocity command
    '''
    p_player, v_player, p_ego = state
    if depth == 0: return (heuristic(p_player, p_ego), None)
    best_velocity_duration = None
    v = np.inf
    for h, du in list(itertools.product(r_h_ego, r_du_ego)):
        v_ego = (max_velocity_magnitude_ego*np.cos(h), max_velocity_magnitude_ego*np.sin(h))
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

def ego_model(p_player:tuple, p_player_previous:tuple, p_ego:tuple, depth=3):
    '''
    define search space for ego vehicle (quad copter)
    input: p_player - player postion in the real world
           p_player_previous - previous player postion in the real world
           p_ego - ego position in the real world
    output: tuple of best position and best velocity vector
    '''
    v_player = ((p_player[0]-p_player_previous[0])/t*1e-3, (p_player[1]-p_player_previous[1])/t*1e-3)
    r_du_ego = [1]
    _, velocity_duration = ego_model_tree(
        depth=depth,
        state=(p_player, v_player, p_ego),
        r_h_ego=h_list,
        r_du_ego=r_du_ego
    )
    v_ego, _ = velocity_duration
    return ((p_ego[0]+(v_ego[0]*t*1e-3), p_ego[1]+(v_ego[1]*t*1e-3)), v_ego)

def simulate():
    '''
    runs the simulation
    '''
    p_player_plot = []
    v_player_plot = []
    p_player, p_heading = player_state, player_heading
    p_ego, v_ego = ego_state, [np.cos(ego_heading), np.sin(ego_heading)]
    reached_goal_state = False
    ctr = 0
    while not reached_goal_state:
        ctr += 1
        p_player_previous = p_player
        p_player_plot.append(p_player_previous)
        v_player_plot.append(p_ego)
        _, v_player = movement_model(p_player, p_heading)
        _, p_player, v_player = interaction_model(p_player, v_player, p_ego, v_ego)
        p_heading = np.arctan2(v_player[1], v_player[0])
        p_ego, v_ego = ego_model(p_player, p_player_previous, p_ego)
        if ((p_player[0]-goal_state[0])**2 + (p_player[1]-goal_state[1])**2)**0.5 < goal_aware_sphere_radius:
            reached_goal_state=True
        print(f'Step {ctr}: Distance to goal state:\tFrom player = {distance(p_player, goal_state)}\tFrom ego = {distance(p_ego, goal_state)}')
    x = np.asarray(p_player_plot)
    y = np.asarray(v_player_plot)
    plt.figure(figsize=(13, 7))
    plt.xlim(0, world[0])
    plt.ylim(0, world[0])
    plt.grid()
    plt.plot(x[:, 0], x[:, 1], '--bo', label='line with marker')
    plt.plot(y[:, 0], y[:, 1], '--ro', label='line with marker')
    plt.plot(goal_state[0], goal_state[1], marker="o", markersize=10,markerfacecolor="green")
    plt.plot(x[-1,0], x[-1, 1], marker="*", markersize=10,markerfacecolor="red")
    plt.plot(y[-1,0], y[-1, 1], marker="*", markersize=10,markerfacecolor="red")
    plt.show()


if __name__ == '__main__':
    simulate()