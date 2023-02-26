import logging

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture as GMM
from sklearn.model_selection import GridSearchCV
from tqdm import trange

from model.nba_api_helpers import (generate_3_point_classifier,
                                   get_league_shot_loc_data,
                                   get_player_shot_loc_data)


class ThreesModel:

    """
    Model class for simulating three point shots for given player and opponent defense
    """

    @staticmethod
    def run_model(
            player_name:str="Buddy Hield", 
            opponent:str="BOS",
            n_components:int=5, 
            bootstrap_samples:int=100_000,
            n_simulated_games:int=200_000,
            min_samples:int=25,
            apply_3_point_classifier:bool=False,
            plot:bool=False,
            plot_args:dict={
                'seaborn_style': 'darkgrid',
                'seaborn_context': 'poster',
                'figsize': (10, 6)
            }
        ) -> np.array:

        """
        Main method to run Threes Model
        :param player_name: The name of the player to simulate shots for
        :param opponent: The opponent defense to simulate shots against (use 3 letter abbreviation)
        :param n_components: The number of clusters to use for the GMM
        :param bootstrap_samples: The number of bootstrap samples to use (suggested 100,000 - 500,000)
        :param n_simulated_games: The number of simulated games to run (suggested 10,000 - 200,000)
        :param plot: Whether to plot the results
        :return: numpy array of simulated shot results (1 = made, 0 = missed), length = n_simulated_games
        """
        try:
            player_df = get_player_shot_loc_data(player_name, context_measure_simple='FG3A')
        except Exception:
            logging.error(f'Error getting player data for {player_name}. Could not find player in NBA API.')
            return np.array([])
        
        threes = player_df.loc[:, ['GAME_ID', 'LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG', 'SHOT_ATTEMPTED_FLAG']]
        threes = threes.dropna()

        if threes.shape[0] < min_samples:
            logging.error(f'Not enough samples ({min_samples}) to run model for {player_name}. Skipping.')
            return np.array([])

        threes['SHOT_MADE_FLAG'] = threes['SHOT_MADE_FLAG'].astype(np.int64)
        
        threes_train_xy = threes[['LOC_X', 'LOC_Y']].values.reshape(-1, 2)
        fga_per_game_data = threes.groupby('GAME_ID')['SHOT_ATTEMPTED_FLAG'].count().values

        #get league shot data
        
        league_df = get_league_shot_loc_data(context_measure_simple='FG3A')
        league_test_xy = league_df[['LOC_X', 'LOC_Y']].values.reshape(-1, 2)

        param_grid = {
            "n_components": range(2, 15),
            "covariance_type": ["spherical", "tied", "diag", "full"],
        }
        try:
            grid_search = GridSearchCV(
                GMM(), param_grid=param_grid, error_score='raise', scoring=lambda estimator, x: -estimator.bic(x)
            )
            grid_search.fit(threes_train_xy)
        except ValueError:
            logging.error(f'Not enough samples to perform cross-validation for {player_name}. Skipping.')
            return np.array([])
        
        covariance_type = grid_search.best_params_['covariance_type']
        n_components = grid_search.best_params_['n_components']
        model = GMM(n_components=n_components, covariance_type=covariance_type, random_state=0).fit(threes_train_xy)
        
        model_labels_ = model.predict(threes_train_xy)

        league_model_labels_ = model.predict(league_test_xy)
        league_df['cluster'] = league_model_labels_
        
        #filter for opponent after assigning clusters
        opponent_df = league_df.loc[league_df['DEF'] == opponent]
        
        #create a dataframe from the cluster data dictionary
        cluster_df = pd.DataFrame({
            'shot_made': threes['SHOT_MADE_FLAG'],
            'cluster': model_labels_
        })

        #shooting percentage by cluster
        fg_percent_by_cluster = pd.DataFrame(cluster_df.groupby('cluster')['shot_made'].value_counts(normalize=True)).rename({'shot_made': 'fg_percent'}, axis=1).reset_index()
        fg_percent_by_cluster = fg_percent_by_cluster.loc[fg_percent_by_cluster['shot_made'] == 1].drop('shot_made', axis=1)['fg_percent']

        #league fg% by cluster
        league_fg_percent_by_cluster = pd.DataFrame(league_df.groupby('cluster')['SHOT_MADE_FLAG'].value_counts(normalize=True)).rename({'SHOT_MADE_FLAG': 'fg_percent'}, axis=1).reset_index()
        league_fg_percent_by_cluster = league_fg_percent_by_cluster.loc[league_fg_percent_by_cluster['SHOT_MADE_FLAG'] == 1].drop('SHOT_MADE_FLAG', axis=1)['fg_percent']

        #opponent def fg% by cluster
        opponent_fg_percent_by_cluster = pd.DataFrame(opponent_df.groupby('cluster')['SHOT_MADE_FLAG'].value_counts(normalize=True)).rename({'SHOT_MADE_FLAG': 'fg_percent'}, axis=1).reset_index()
        opponent_fg_percent_by_cluster = opponent_fg_percent_by_cluster.loc[opponent_fg_percent_by_cluster['SHOT_MADE_FLAG'] == 1].drop('SHOT_MADE_FLAG', axis=1)['fg_percent']
        
        #opponent defensive ratings per cluster relative to league average
        def_adjustment = opponent_fg_percent_by_cluster / league_fg_percent_by_cluster

        #bootstrap resample from FGA data to find normal distribution fo estimated mean FGA per game
        fga_per_game_est = [np.random.choice(fga_per_game_data, size=len(fga_per_game_data), replace=True).mean() for _ in range(bootstrap_samples)]
        fga_per_game_est_mean = np.mean(fga_per_game_est)
        fga_per_game_est_std = np.std(fga_per_game_est)

        fg3m_s = []
        #simulate n_simulations games
        for _ in trange(n_simulated_games, desc=f'Simulating 3PM outcomes for {player_name} vs {opponent}...'):

            #simulate FGA
            fga_i = np.random.poisson(np.random.normal(fga_per_game_est_mean, fga_per_game_est_std))

            if fga_i == 0:
                fg3m_s.append(0)
                continue

            #simulate shot locations based off density of where shots are taken
            sampled_shot_locs = []
            for _ in range(fga_i):

                selected_cluster = np.random.choice(np.arange(0, n_components), p=model.weights_)

                match covariance_type:
                    case 'full':
                        covariances_ = model.covariances_[selected_cluster].reshape(2, 2)
                    case 'tied':
                        covariances_ = model.covariances_.reshape(2, 2)
                    case 'diag':
                        covariances_ = np.diag(model.covariances_[selected_cluster])
                    case 'spherical':
                        covariances_ = np.eye(model.means_.shape[1]) * model.covariances_[selected_cluster]

                sampled_shot = np.random.multivariate_normal(model.means_[selected_cluster], covariances_)
                sampled_shot_locs = np.append(sampled_shot_locs, sampled_shot)    

            sampled_shot_locs = sampled_shot_locs.reshape(-1, 2)

            #apply weighting to each shot based off cluster
            weighted_fg_percent = np.dot(
                fg_percent_by_cluster.values * def_adjustment, model.predict_proba(sampled_shot_locs).T
            )

            fgm_i = np.vectorize(np.random.binomial)(1, weighted_fg_percent)

            fg3m_s.append(fgm_i.sum())

        if plot:
            sns.set_style(plot_args.get('seaborn_style'))
            sns.set_context(plot_args.get('seaborn_context'))
            plt.figure(figsize=plot_args.get('figsize'))
            sns.ecdfplot(fg3m_s, stat='proportion', color='red', alpha=0.5)
            plt.title(f'Results of {n_simulated_games} simulated games for {player_name}')
            plt.xlabel('3PM')
            plt.ylabel('Density')
            plt.show()

        return np.array(fg3m_s)