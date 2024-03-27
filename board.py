import random
import math
from typing import Self


class State:
    def __init__(self, state: str) -> None:
        self.__state = state
        self.threats = self.get_threats()

    def get_threats(self) -> int:
        sta = [*map(int, self.__state)]
        s = (
            sum(
                [
                    1 if i[1] == j[1] or abs(i[0] - j[0]) == abs(i[1] - j[1]) else 0
                    for i in enumerate(sta)
                    for j in enumerate(sta)
                    if i != j
                ]
            )
            // 2
        )
        return s

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and other.__state == self.__state

    def __hash__(self) -> int:
        return hash(self.__state)

    @property
    def state(self):
        """The state property."""
        return self.__state

    @state.setter
    def state(self, value: str):
        self.__state = value
        self.threats = self.get_threats()

    @staticmethod
    def get_random_state(length: int) -> str:
        nums = "".join([*map(str, range(1, length + 1))])
        return "".join(random.sample(nums, length))

    @staticmethod
    def crossover_states(s1: Self, s2: Self) -> tuple[Self, Self]:
        i = random.randint(0, len(s1.state))
        return (
            State(s1.state[0:i] + s2.state[i:]),
            State(s2.state[0:i] + s1.state[i:]),
        )

    def __str__(self) -> str:
        return f"{self.state}@{self.threats}"

    def __repr__(self) -> str:
        return self.__str__()


class GeneticAlgorithm:
    def __init__(
        self,
        starting_population: int = 50,
        mutation_chance: float = 0.001,
        coupling_chanse: float = 0.99,
        selected_parents_persent: float = 0.4,
        board_Width: int = 8,
        max_generations: int = 100,
    ) -> None:
        self.starting_population = starting_population
        self.mutation_chance = mutation_chance
        self.coupling_chanse = coupling_chanse
        self.selected_parents_persent = selected_parents_persent
        self.board_Width = board_Width
        self.max_generations = max_generations
        self.population: set[State] = []

        self.board_index_list = "".join([*map(str, range(1, self.board_Width + 1))])

    def start(self):
        self.population = {
            State(State.get_random_state(self.board_Width))
            for _ in range(self.starting_population)
        }

        # start main loop
        for i in range(self.max_generations):
            print(f"Starting generation {i}")
            # select top x persent of population to couple
            current_pupulation: list[State] = sorted(
                self.population, key=lambda x: x.threats
            )

            if current_pupulation[0].threats == 0:
                return current_pupulation[0].state
                # print("State Found")
            # take top x percent of parents to select from randomly
            selected_parents: list[State] = current_pupulation[
                0 : math.ceil(
                    self.starting_population * (self.selected_parents_persent / 2)
                )
                * 2
            ]
            # select parents with the better one with higher chanse
            total_points = sum([self.get_fitness(state) for state in selected_parents])
            # get weights for parents
            weights = [
                (self.get_fitness(state=state) * 100) // total_points
                for state in selected_parents
            ]
            # chose parents randomly base of weights
            selected_parents = random.choices(
                population=selected_parents, weights=weights, k=len(selected_parents)
            )

            # crossover
            childs: list[State] = []
            for j in range(0, len(selected_parents) - 1, 2):
                if random.random() < self.coupling_chanse:
                    childs.extend(
                        State.crossover_states(
                            selected_parents[j], selected_parents[j + 1]
                        )
                    )
            for j in childs:
                l = [*j.state]
                for y in range(len(l)):
                    changed_flag = False
                    if random.random() <= self.mutation_chance:
                        l[y] = random.choice(self.board_index_list)
                        changed_flag = True
                if changed_flag:
                    j.state = "".join(l)
            self.population.update(childs)
        return None

    @staticmethod
    def get_fitness(state: State) -> int:
        return (len(state.state) * len(state.state) - 1) // 2 - state.threats


# with cProfile.Profile() as pr:
a = GeneticAlgorithm(
    max_generations=100,
    starting_population=100,
    mutation_chance=0.05,
    selected_parents_persent=0.5,
    board_Width=8,
)
if res := a.start():
    print(res)
