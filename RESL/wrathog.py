from utils import *


def wrathog(p_player:tuple, v_player:float, p_ego:tuple, v_ego:tuple, t:int=1000, repulsion_strength:int=10) -> dict:
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
    p_heading = np.arctan2(v_player[1], v_player[0])
    v_player_expected = movement_model(p_player, p_heading)
    v_player_resultant = interaction_model(p_player, v_player_expected, p_ego, v_ego, t, repulsion_strength)
    v_player_magnitude, v_player_heading = translate_velocity(v_player_resultant)
    context = {
        'linear': {
            'x': v_player_magnitude,
            'y': 0,
            'z': 0
        },
        'angluar': {
            'x': 0,
            'y': 0,
            'z': v_player_heading
        }
    }
    return context