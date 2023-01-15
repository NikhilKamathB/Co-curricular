import numpy as np


min_velocity_magnitude_player, max_velocity_magnitude_player = 0, 1
min_velocity_magnitude_ego, max_velocity_magnitude_ego = 0, 5
h_list = list(set([_*(np.pi/180) for _ in range(0, 360, 30)] + [_*(np.pi/180) for _ in range(45, 360, 45)]))
du_list = [1]

def translate_velocity(v:tuple) -> tuple:
    '''
    calculates distance between two points
    input: v - (a, b) - velocity vector
    output: magnitude heading and 
    '''
    h_agent = np.arctan2(v[1], v[0])
    v_magnitude = np.linalg.norm(v)
    # Uncomment if you want the range to be [0, ...]
    # if h_agent < 0: h_agent = 2*np.pi + h_agent
    return (v_magnitude, h_agent)

def distance(x :tuple, y:tuple) -> float:
    '''
    calculates distance between two points
    input: x - (a, b)
           y - (c, d)
    output: distance between x and y
    '''
    return ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5

def heuristic(p_player:tuple, p_ego:tuple, goal_state:tuple) -> float:
    '''
    calculates heuristic for every state of the quad copter
    input: p_player - player postion in the real world
           p_ego - ego position in the real world
           goal_state - goal position in the real world
    output: a state value estimation
    '''
    d_player_goal = distance(p_player, goal_state)
    d_player_ego = distance(p_player, p_ego)
    return d_player_goal + d_player_ego

def movement_model(p_player:tuple, h_player:float) -> tuple:
    '''
    defines movement model for player (not quad copter)
    input: p_player - player postion in the real world - (a, b)
           h_player - player heading in the real/local world - between 0 and 2pi
    output: expected velocity vector
    '''
    x_hat, y_hat = max_velocity_magnitude_player*np.cos(h_player), max_velocity_magnitude_player*np.sin(h_player)
    return (x_hat, y_hat)

def interaction_model(p_player:tuple, v_player:tuple, p_ego:tuple, v_ego:tuple, t:int=1000, repulsion_strength:int=10) -> tuple:
    '''
    defines interaction model for player (not quad copter)
    input: p_player - player postion in the real world
           v_player - velocity vector of the player in the local world
           p_ego - ego position in the real world
           v_ego - velocity vector of the ego in the local world
           t - time in milliseconds (to be executed)
           repulsion_strength (self-explanatory)
    output: resultant velocity vector
    '''
    next_p_ego = (p_ego[0]+(v_ego[0]*t*1e-3), p_ego[1]+(v_ego[1]*t*1e-3))
    d_player_ego = distance(p_player, next_p_ego)
    h_repulsion = (p_player[0]-next_p_ego[0], p_player[1]-next_p_ego[1])
    repulsion_scale = repulsion_strength/(d_player_ego**2)
    x_hat, y_hat = v_player[0]+(repulsion_scale*h_repulsion[0]), v_player[1]+(repulsion_scale*h_repulsion[1])
    return (x_hat, y_hat)