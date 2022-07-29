from State import State
import random as rd
from Person import Person
from typing import List, Tuple
from constants import *
import constants

success_of_cure = False
success_of_bite = False
class Board:
    def __init__(
        self,
        dimensions: Tuple[int, int],
        player_role: str,
    ):
        self.rows = dimensions[0]
        self.columns = dimensions[1]
        self.player_role = player_role
        self.player_num = ROLE_TO_ROLE_NUM[player_role]
        self.population = 0
        self.States = []
        self.QTable = []
        for s in range(dimensions[0] * dimensions[1]):
            self.States.append(State(None, s))
            self.QTable.append([0] * 6)

        self.actionToFunction = {
            "moveUp": self.moveUp,
            "moveDown": self.moveDown,
            "moveLeft": self.moveLeft,
            "moveRight": self.moveRight,
            "heal": self.heal,
            "bite": self.bite,
            "kill": self.kill
        }
        self.statesSelected = [] # store the location of the state

    def num_zombies(self) -> int:
        r = 0
        for state in self.States:
            if state.person != None:
                if state.person.isZombie:
                    r += 1
        return r

    def act(self, oldstate: Tuple[int, int], givenAction: str):
        cell = self.toCoord(oldstate)
        f = self.actionToFunction[givenAction](cell)
        reward = self.States[oldstate].evaluate(givenAction, self)
        if f[0] == False:
            reward = 0
        return [reward, f[1]]

    def containsPerson(self, isZombie: bool):
        for state in self.States:
            if state.person is not None and state.person.isZombie == isZombie:
                return True
        return False

    def get_possible_moves(self, action: str, role: str):
        """
        Get the coordinates of people (or zombies) that are able
        to make the specified move.
        @param action - the action to return possibilities for (options are 'bite', 'moveUp', 'moveDown','moveLeft', 'moveRight', and 'heal')
        @param role - either 'Zombie' or 'Government'; helps decide whether an action
        is valid and which people/zombies it applies to
        """
        poss = []
        B = self.clone(self.States, role)

        if role == "Zombie":
            if not self.containsPerson(True):
                return poss
            for idx in range(len(self.States)):
                state = self.States[idx]
                if state.person is not None:
                    changed_states = False

                    if (
                        action == "bite"
                        and not state.person.isZombie
                        and self.isAdjacentTo(self.toCoord(idx), True)
                    ):
                        # if the current space isn't a zombie and it is adjacent
                        # a space that is a zombie
                        poss.append(B.toCoord(idx))
                        changed_states = True
                    elif (
                        action != "bite"
                        and state.person.isZombie
                        and B.actionToFunction[action](B.toCoord(idx))[0]
                    ):
                        poss.append(B.toCoord(idx))
                        changed_states = True

                    if changed_states:
                        # reset the states
                        B.States = [
                            self.States[i].clone()
                            if self.States[i] != B.States[i]
                            else B.States[i]
                            for i in range(len(self.States))
                        ]

        elif role == "Government":
            if not self.containsPerson(False):
                return poss
            for idx in range(len(self.States)):
                state = self.States[idx]
                if state.person is not None:
                    changed_states = False
                    if action == "heal" and (
                        state.person.isZombie
                    ):
                        poss.append(B.toCoord(idx))
                        changed_states = True
                    elif (
                        action != "heal"
                        and not state.person.isZombie
                        and B.actionToFunction[action](B.toCoord(idx))[0]
                    ):
                        poss.append(B.toCoord(idx))
                        changed_states = True

                    if changed_states:
                        # reset the states
                        B.States = [
                            self.States[i].clone()
                            if self.States[i] != B.States[i]
                            else B.States[i]
                            for i in range(len(self.States))
                        ]
        return poss

    def toCoord(self, i: int):
        return (int(i % self.columns), int(i / self.rows))

    def toIndex(self, coordinates: Tuple[int, int]):
        return int(coordinates[1] * self.columns) + int(coordinates[0])

    def isValidCoordinate(self, coordinates: Tuple[int, int]):
        return (
            coordinates[1] < self.rows
            and coordinates[1] >= 0
            and coordinates[0] < self.columns
            and coordinates[0] >= 0
        )

    def clone(self, L: List[State], role: str):
        NB = Board(
            (self.rows, self.columns),
            self.player_role,
        )
        NB.States = [state.clone() for state in L]
        NB.player_role = role
        return NB

    def isAdjacentTo(self, coord: Tuple[int, int], is_zombie: bool) -> bool:
        ret = False
        vals = [
            (coord[0], coord[1] + 1),
            (coord[0], coord[1] - 1),
            (coord[0] + 1, coord[1]),
            (coord[0] - 1, coord[1]),
        ]
        for coord in vals:
            if (
                self.isValidCoordinate(coord)
                and self.States[self.toIndex(coord)].person is not None
                and self.States[self.toIndex(coord)].person.isZombie == is_zombie
            ):
                ret = True
                break

        return ret

    def move(
        self, from_coords: Tuple[int, int], new_coords: Tuple[int, int]
    ) -> Tuple[bool, int]:
        """
        Check if the move is valid.
        If valid, then implement the move and return [True, destination_idx]
        If invalid, then return [False, None]
        If the space is currently occupied, then return [False, destination_idx]
        """
        # Get the start and destination index (1D)
        start_idx = self.toIndex(from_coords)
        destination_idx = self.toIndex(new_coords)

        # Check if the new coordinates are valid
        if not self.isValidCoordinate(new_coords):
            return [False, destination_idx, None]

        # Check if the destination is currently occupied
        if self.States[destination_idx].person is None:
            constants.CURRENT_SCORE+=SCORE_VALUES["move"]
            self.States[destination_idx].person = self.States[start_idx].person
            self.States[start_idx].person = None
            return [True, destination_idx, None]

        
        return [False, destination_idx, None]

    def moveUp(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        new_coords = (coords[0], coords[1] - 1)
        return self.move(coords, new_coords)

    def moveDown(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        new_coords = (coords[0], coords[1] + 1)
        return self.move(coords, new_coords)

    def moveLeft(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        new_coords = (coords[0] - 1, coords[1])
        return self.move(coords, new_coords)

    def moveRight(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        new_coords = (coords[0] + 1, coords[1])
        return self.move(coords, new_coords)

    def QGreedyat(self, state_id: int):
        biggest = self.QTable[state_id][0] * self.player_num
        ind = 0
        A = self.QTable[state_id]
        i = 0
        for qval in A:
            if (qval * self.player_num) > biggest:
                biggest = qval
                ind = i
            i += 1
        return [ind, self.QTable[ind]]  # action_index, qvalue

    def choose_action(self, state_id: int, lr: float):
        L = lr * 100
        r = rd.randint(0, 100)
        if r < L:
            return self.QGreedyat(state_id)
        else:
            if self.player_num == 1:  # Player is Govt
                d = rd.randint(0, 4)
            else:
                d = rd.randint(0, 5)
                while d != 4:
                    d = rd.randint(0, 4)
            return d

    def choose_state(self, lr: float):
        L = lr * 100
        r = rd.randint(0, 100)
        if r < L:
            biggest = None
            sid = None
            for x in range(len(self.States)):
                if self.States[x].person != None:
                    q = self.QGreedyat(x)
                    if biggest is None:
                        biggest = q[1]
                        sid = x
                    elif q[1] > biggest:
                        biggest = q[1]
                        sid = x
            return self.QGreedyat(sid)
        else:
            if self.player_num == -1:  # Player is Govt
                d = rd.randint(0, len(self.States))
                while self.States[d].person is None or self.States[d].person.isZombie:
                    d = rd.randint(0, len(self.States))
            else:
                d = rd.randint(0, len(self.States))
                while (
                    self.States[d].person is None
                    or self.States[d].person.isZombie == False
                ):
                    d = rd.randint(0, len(self.States))
            return d

    def bite(self, coords: Tuple[int, int], stage=3) -> Tuple[bool, int, bool]:
        i = self.toIndex(coords)
        global success_of_bite
        if (
            self.States[i].person is None
            or self.States[i].person.isZombie
            or not self.isAdjacentTo(coords, True)
        ):
            return [False, None, None]
        if stage==2:
            if rd.random()<constants.STAGE_2_BITE_RATE:
                success_of_bite = True
                self.States[i].person.get_bitten()
        elif stage==3:
            if rd.random()<constants.STAGE_3_BITE_RATE:
                success_of_bite = True
                self.States[i].person.get_bitten()
        constants.CURRENT_SCORE+=SCORE_VALUES["bite"]
        return [True, i, success_of_bite]
        

    def heal(self, coords: Tuple[int, int]) -> Tuple[bool, int, bool]:
        """
        Cures the person at the stated coordinates.
        If there is a zombie there, the person will be cured.
        If no person is selected, then return [False, None]
        if a person is cured, then return [True, index]
        """
        i = self.toIndex(coords)
        if self.States[i].person is None:
            return [False, None, None]
        p = self.States[i].person

        personAdjacent = False
        for state in self.States[i].get_adj_states(self):
            if state != None and state.person != None and not state.person.isZombie:
                personAdjacent = True
        if p.isZombie and personAdjacent:
            global success_of_cure
            success_of_cure = p.get_cured()
            constants.CURRENT_SCORE+=SCORE_VALUES["heal"]
        else:
            return [False, None, None]
        
        

        return [True, i, success_of_cure]

    def kill(self, coords: Tuple[int, int]) -> Tuple[bool, int, bool]:
        """
        KILLS ZOMBIE
        """
        i = self.toIndex(coords)
        if self.States[i].person is None:
            return [False, None, None]
        p = self.States[i].person

        personAdjacent = False
        for state in self.States[i].get_adj_states(self):
            if state != None and state.person != None and not state.person.isZombie:
                personAdjacent = True
        if p.isZombie and personAdjacent:
            p.kill_me()
            self.States[i].person = None
            p = None
            constants.CURRENT_SCORE+=SCORE_VALUES["kill"]
        else:
            return [False, None, None]
        
       

        return [True, i, True]
    def heuristic_action(self, optimum_state):
        poss_moves = optimum_state.get_possible_moves(self)
        if len(poss_moves)==0:
            return "moveUp"
        if rd.random()<.9:
            nearest_person_info = optimum_state.get_nearest_person(self)
            if nearest_person_info[1] == 1 and "bite" in poss_moves:
                    return "bite"
            
            person_is_isolated = True
            if nearest_person_info[0] == None:
                return rd.choice(poss_moves)

            for state in nearest_person_info[0].get_adj_states(self):
                if state.person != None and state.person.isZombie == False:
                    person_is_isolated = True
            from_opt_to_person = optimum_state.get_direction_to(nearest_person_info[0], self, poss_moves)
            
            return from_opt_to_person
            # if person_is_isolated and from_opt_to_person in poss_moves:
            #     return from_opt_to_person
            # else:
            #     if from_opt_to_person in poss_moves and len(poss_moves) > 2:
            #         poss_moves.remove(from_opt_to_person)
              
            #     return rd.choice(poss_moves)
        else:
            return rd.choice(poss_moves)
            

        
    def heuristic_state(self):
        zombie_states = []
        for state in self.States:
            if state.person != None and state.person.isZombie == True and state.person.zombieStage >= 2:
                zombie_states.append(state)
        dist = 100
        for state in zombie_states:
            if len(state.get_possible_moves(self)) <= 0:
                zombie_states.remove(state)
        if len(zombie_states) == 0:
            return False
        optimum_zombie_state = zombie_states[0]
        if rd.random() < .9:
            for state in zombie_states:
                nearest_person = state.get_nearest_person(self)
                if nearest_person[1] < dist:
                    dist = nearest_person[1]
                    optimum_zombie_state = state
        else:
            optimum_zombie_state = rd.choice(zombie_states)
        return optimum_zombie_state


    def get_possible_states(self, role_number: int):
        indexes = []
        i = 0
        for state in self.States:
            if state.person != None:
                if role_number == 1 and state.person.isZombie == False:
                    indexes.append(i)
                elif role_number == -1 and state.person.isZombie:
                    indexes.append(i)
            i += 1
        return indexes

    def step(self, role_number: int, learningRate: float):
        P = self.get_possible_states(role_number)
        r = rd.uniform(0, 1)
        if r < learningRate:
            rs = rd.randrange(0, len(self.States) - 1)
            if role_number == 1:
                while (
                    self.States[rs].person is not None
                    and self.States[rs].person.isZombie
                ):
                    rs = rd.randrange(0, len(self.States) - 1)
            else:
                while (
                    self.States[rs].person is not None
                    and self.States[rs].person.isZombie == False
                ):
                    rs = rd.randrange(0, len(self.States) - 1)

            # random state and value
        # old_value = QTable[state][acti]
        # next_max = np.max(QTable[next_state])
        # new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        # QTable[state][acti] = new_value

    def populate(self):
        total = rd.randint(7, ((self.rows * self.columns) / 3)) #choose between 7 and 12
        poss = [] 
        for x in range(len(self.States)):
            r = rd.randint(0, 100)
            if r < 30 and self.population < total:
                p = Person(False)
                self.States[x].person = p
                self.population = self.population + 1
                poss.append(x)
            else:
                self.States[x].person = None
        used = []
        amt_zombies = rd.randint(3, 5)
        for x in range(amt_zombies):
            s = rd.randint(0, len(poss) - 1)
            while s in used:
                s = rd.randint(0, len(poss) - 1)
            self.States[poss[s]].person.isZombie = True
            self.States[poss[s]].person.zombieStage = 3
            used.append(s)

    def update(self):
        """
        Update each of the states;
        This method should be called at the end of each round
        (after player and computer have each gone once)
        """
        for state in self.States:
            state.update()

    def updateMovesSinceTransformation (self):
        for state in self.States:
            if state.person is not None:
                state.person.updateMovesSinceTransformation()

    def resetBoard (self):
        self.population = 0
        self.States = []
        for s in range(6*6):
            self.States.append(State(None, s))
            
    def getPlayerStates (self):
        arr = []
        for i in self.States:
            if i.person is not None and i.person.isZombie == False:
                arr.append(i)
        return arr
    
    def getZombieStates(self):
        arr = []
        for i in self.States:
            if i.person is not None and i.person.isZombie == True:
                arr.append(i)
        return arr