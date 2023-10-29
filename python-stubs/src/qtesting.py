import random

class QTraining():
    def __init__(self, agent, init_state, learning_rate, discount_factor, exploration_prob, num_episodes):
        self.init_state = init_state
        self.agent = agent
        self.actions = [
            'none',
            'jump',
            'left',
            'right',
            'neutral',
            'special',
            'tilt_up',
            'tilt_down',
            'tilt_left',
            'tilt_right',
            'smash_up',
            'smash_down',
            'smash_left',
            'smash_right',
            'shield',
            'grab'
        ]
        
        self.attack_actions = [
            'neutral',
            'special',
            'tilt_up',
            'tilt_down',
            'tilt_left',
            'tilt_right',
            'smash_up',
            'smash_down',
            'smash_left',
            'smash_right'
        ]
        
        self.movement_actions = [
            'none',
            'jump',
            'left',
            'right'
        ]
    
        # Define hyperparameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.num_episodes = num_episodes
        
        self.num_features = len(self.get_features(init_state))
        self.weights = [0] * self.num_features
        
        self.q_values = {action: 0.0 for action in self.actions}
        
    def get_actions(self):
        return self.actions

    def get_features(self, state):
        if len(state) == 3:
            time_remaining, player_info, enemy_info, = state
            action = 'none'
        elif len(state) == 4:
            time_remaining, player_info, enemy_info, action = state
            
        # Encode the action using one-hot encoding based on your actions list
        num_actions = len(self.actions)
        action_encoding = [0] * num_actions
        action_index = self.actions.index(action)
        action_encoding[action_index] = 1
            
        player_features = [float(player_info[0][0]), float(player_info[0][1]), float(player_info[2]), float(player_info[3])]
        enemy_features = [float(enemy_info[0][0]), float(enemy_info[0][1]), float(enemy_info[2])]
        
        return player_features + enemy_features + action_encoding

    def calculate_q_value(self, state, action):
        q_value = 0
        features = self.get_features(state + [action])
        for i in range(self.num_features):
            q_value += self.weights[i] + float(features[i])
        return q_value
    
    def train(self, state, prev_state):
        # Choose an action using epsilon-greedy strategy
        if random.random() < self.exploration_prob:
            action = random.choice(self.actions)
        else:
            # Calculate Q-values for each action
            self.q_values = [self.calculate_q_value(state, a) for a in self.actions]
            action = self.actions[self.q_values.index(max(self.q_values))]
        
        self.agent.action(action)
        reward = self.reward(state, prev_state, action)  # Define your reward function
        td_error = reward + self.discount_factor * float(max(self.q_values)) - self.calculate_q_value(state, action)
        # print(f"{reward} + {self.discount_factor} * {max(self.q_values)} - {self.calculate_q_value(state, action)} = {td_error}")
        for i in range(self.num_features):
            self.weights[i] += self.learning_rate * td_error * self.get_features(state + [action])[i]
            
        return self.weights
    
    def reward(self, state, prev_state, action):
        # Deconstruct current player information
        curr_player_info = state[2]
        (
            curr_player_pos,
            curr_player_direction,
            curr_player_percentage,
            curr_player_stocks,
            curr_player_action_state,
            curr_player_knockouts,
            curr_player_self_destructs
        ) = curr_player_info

        # Deconstruct current opponent information
        curr_opponent_info = state[1]
        (
            curr_opponent_pos,
            curr_opponent_direction,
            curr_opponent_percentage,
            curr_opponent_stocks,
            curr_opponent_action_state,
            curr_opponent_knockouts,
            curr_opponent_self_destructs
        ) = curr_opponent_info

        # Deconstruct previous player information
        prev_player_info = prev_state[2]
        (
            prev_player_pos,
            prev_player_direction,
            prev_player_percentage,
            prev_player_stocks,
            prev_player_action_state,
            prev_player_knockouts,
            prev_player_self_destructs
        ) = prev_player_info

        # Deconstruct previous opponent information
        prev_opponent_info = prev_state[1]
        (
            prev_opponent_pos,
            prev_opponent_direction,
            prev_opponent_percentage,
            prev_opponent_stocks,
            prev_opponent_action_state,
            prev_opponent_knockouts,
            prev_opponent_self_destructs
        ) = prev_opponent_info

        reward = 0

        if curr_opponent_percentage > prev_opponent_percentage:
            reward -= 1
        
        if curr_player_knockouts > prev_player_knockouts:
            reward += 100
        
        if curr_player_percentage > prev_player_percentage:
            reward -= 5
            
        if curr_player_self_destructs > prev_player_self_destructs:
            reward -= 100
        
        return reward
        
        
        