# backend/live_ops.py
class LiveGameOperations:
    """Manage live game operations without downtime"""
    
    def __init__(self):
        self.feature_flags = {}
        self.ab_tests = {}
        self.player_segments = {}
    
    def roll_out_feature(self, feature_name, rollout_percentage):
        """Gradually roll out new features to players"""
        
        current_players = self._get_active_players()
        target_count = len(current_players) * rollout_percentage
        
        # Select players for rollout
        selected_players = self._select_players_for_rollout(
            current_players, 
            target_count,
            criteria=['active', 'engaged', 'feedback_givers']
        )
        
        # Enable feature for selected players
        for player_id in selected_players:
            self._enable_feature(player_id, feature_name)
        
        # Monitor impact
        self._monitor_feature_impact(feature_name, selected_players)
        
        return {
            'feature': feature_name,
            'players_affected': len(selected_players),
            'rollout_percentage': rollout_percentage
        }
    
    def run_ab_test(self, test_name, variants):
        """Run A/B test on game features"""
        
        # Split players into groups
        groups = self._split_players_into_groups(
            self._get_test_eligible_players(),
            len(variants)
        )
        
        results = {}
        for i, variant in enumerate(variants):
            group = groups[i]
            
            # Apply variant to group
            for player_id in group:
                self._apply_variant(player_id, variant)
            
            # Collect metrics
            metrics = self._collect_group_metrics(group, variant)
            results[variant['name']] = metrics
        
        # Determine winning variant
        winner = self._determine_winner(results)
        
        # Roll out winning variant to all players
        self._rollout_winner(winner)
        
        return {
            'test': test_name,
            'results': results,
            'winner': winner,
            'confidence': self._calculate_confidence(results)
        }
