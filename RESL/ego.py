import itertools
from utils import *


def ego_model_next_state(p_player:tuple, v_player:tuple, p_ego:tuple, v_ego:tuple, t:int=1000) -> tuple:
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
        d_ego_player = distance(p_player_dash, p_ego_dash)
        if d_ego_player > worst_state:
            worst_state = d_ego_player
            state = (p_player_dash, [x_hat, y_hat], p_ego_dash)
    return state
    
def ego_model_tree(depth:int, state:tuple, r_h_ego:list, r_du_ego:list, t:int=1000) -> tuple:
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
            state=ego_model_next_state(p_player, v_player, p_ego, v_ego, t),
            r_h_ego=r_h_ego,
            r_du_ego=r_du_ego,
            t=t
        )
        if score < v:
            v = score
            best_velocity_duration = (v_ego, du)
    return (v, best_velocity_duration)
    
def ego_model(p_player:tuple, p_player_previous:tuple, p_ego:tuple, depth:int=3, t:int=1000) -> tuple:
    '''
    define search space for ego vehicle (quad copter)
    input: p_player - player postion in the real world
           p_player_previous - previous player postion in the real world
           p_ego - ego position in the real world
           depth - depth of the search tree
           t - time in milliseconds (to be executed)
    output: tuple of best position and best velocity vector
    '''
    v_player = ((p_player[0]-p_player_previous[0])/t*1e-3, (p_player[1]-p_player_previous[1])/t*1e-3)
    _, velocity_duration = ego_model_tree(
        depth=depth,
        state=(p_player, v_player, p_ego),
        r_h_ego=h_list,
        r_du_ego=du_list,
        t=t
    )
    v_ego, _ = velocity_duration
    return v_ego

def ego(p_player:tuple, p_player_previous:tuple, p_ego:tuple, depth:int=3, t:int=1000) -> dict:
    '''
    defines interaction model for player (not quad copter)
    input: p_player - player postion in the real world
           p_player_previous - previous player postion in the real world
           v_player - velocity vector of the player in the local world
           p_ego - ego position in the real world
           v_ego - velocity vector of the ego in the local world
           depth - depth of the search tree
           t - time in milliseconds (to be executed)
    output: resultant velocity vector
    '''
    v_ego_resultant = ego_model(p_player, p_player_previous, p_ego, depth, t)
    v_ego_magnitude, v_ego_heading = translate_velocity(v_ego_resultant)
    context = {
        'linear': {
            'x': v_ego_magnitude,
            'y': 0,
            'z': 0
        },
        'angluar': {
            'x': 0,
            'y': 0,
            'z': v_ego_heading
        }
    }
    return context