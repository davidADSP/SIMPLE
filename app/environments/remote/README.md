# Remote Environment

The remote environment allows you to train games using an HTTP interface.

## Implementing the server

See the [Tic Tac Toe server](app.py) for an example implementation.

The server must implement two endpoints `/newgame` and `/step/{id}`.

The `/newgame` endpoint initializes a new game and returns the following JSON:

```json
{
    "id": "unique game identifier used by the server to map game IDs to in-memory game states",
    "player_count": X (integer),
    "action_space_size": X (integer - size of legal_action array),
    "observation_space_size": X (integer - size of observation array),
    "player_count": X (integer),
    "current_player": X (integer),
    "observation": [array of floats],
    "legal_actions": [array of 1 or 0 where 1 indicates that the action can be taken]
}
```

The `/step/{id}` accepts POST data with `{"action": integer of action selected}`, advances the game state and returns the following JSON:

```json
{
    "observation": [encoding of current game state (-1 to 1)],
    "next_player": integer representing the player whose turn it is after the move is made,
    "reward": [array of rewards for each player],
    "done": true|false # is the game over?
}
```

By default the server should run on http://localhost:5000. The base URL can be changed by setting the `-rbu` parameter.

## Training the agent

To start training:

```bash
docker-compose exec app python3 train.py -r -e remote -rbu http://localhost:8765
```

To resume training:

```bash
docker-compose exec app python3 train.py -e remote -rbu http://localhost:8765
```

## Exporting tflite model

```bash
scripts/export_remote.sh
```

Saves `best_model.tflite` in the current directory.

## Testing the agent

```bash
scripts/random_play_remote.sh -rbu http://localhost:8765
```

Output example:

```bash
[...]
Final winners: {0: 9742, 1: 258}
```

The trained agent always plays as player 0 and random agents will be used for all other players. This result means that the trained agent beat the random agent 97.42% of the time. Any time there is no 1 in the rewards the win will be added to the "-1" player.
