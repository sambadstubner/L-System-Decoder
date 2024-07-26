import logging
from pathlib import Path
import sys


class Decoder:

    def __init__(self, file_path: Path) -> None:
        with open(file_path, "r") as f:
            self.contents: str = f.read()
            self.possible_solutions: list[dict] = []
            self.valid_solutions: list[dict] = []

        self.generations = self.contents.split()

    def decode(self) -> list[dict]:
        self.rules = {}
        self.axiom = self.generations[0]
        found_solution = False
        for i in range(1, len(self.generations)):
            """
            Each generation try to solve for the next generation with the current solutions
            If it is correct then keep going
            If it is not then through it away
            If none is found then do a full search by splitting the next generation
            """
            if not found_solution:
                logging.info(f"No found solution yet, decoding generation {i}")
                local_solutions = self.find_possible_solutions(
                    self.generations[i - 1], self.generations[i]
                )

                self.update_possible_solutions(local_solutions)
                logging.debug(f"Possible solutions:\n{self.possible_solutions}")

                # iterate through the possible solutions to see if it solves the next ones
                solutions = self.possible_solutions.copy()
                for solution in solutions:
                    for i in range(1, len(self.generations)):
                        if (
                            self.generate(self.generations[i - 1], solution)
                            != self.generations[i]
                        ):
                            break

                        if i == (len(self.generations) - 1):
                            logging.info(f"Found solution: {solution}")
                            found_solution = True
                            if solution not in self.possible_solutions:
                                self.valid_solutions.append(solution)

        return self.valid_solutions
    
    def update_possible_solutions(self, new_solutions: list[dict]) -> None:
        previous_solutions = self.possible_solutions.copy()
        self.possible_solutions = []

        for new_sol in new_solutions:
            has_subset = False
            for prev_sol in previous_solutions:
                if self.is_dict_subset(prev_sol, new_sol):
                    has_subset = True
                    prev_sol.update(new_sol)
                    self.possible_solutions.append(prev_sol)
            if not has_subset:
                self.possible_solutions.append(new_sol)



    @staticmethod
    def is_dict_subset(dict_a: dict, dict_b: dict) -> bool:
        for key_a, value_a in dict_a.items():
            if key_a in dict_b.keys():
                if dict_b[key_a] != value_a:
                    return False
        return True



    def find_possible_solutions(
        self, previous_generation: str, current_generation: str
    ) -> list[dict]:
        splits = self.split_generation(previous_generation, current_generation)
        return [dict(zip(previous_generation, split)) for split in splits]

    @staticmethod
    def generate(current_population: str, rules: dict) -> str:
        """
        Generate the next generation given the previous generation and a set of rules
        """
        new_population = ""
        for i in current_population:
            if i in rules.keys():
                new_population += rules[i]
            else:
                new_population += i

        return new_population

    @staticmethod
    def split_generation(previous_generation: str, current_generation: str) -> list:
        def is_valid_partial_split(part, char, char_to_part):
            """
            Checks if the current split already appears in the strings and if so that they match
            """
            if char in char_to_part:
                return char_to_part[char] == part
            return True

        def split_recursive(
            A: str, B: str, current_split: list, char_to_part: dict, all_splits: list
        ) -> None:
            """
            Recursive function split B with the following rules
            1. Split the current generation for each corresponding character in the previous generation
            2. For each same character in the previous generation,
               the cooresponding groupd in the current generation must also match
            """
            if not A:
                if not B:
                    all_splits.append(current_split)
                return

            char = A[0]
            for i in range(1, len(B) - len(A) + 2):
                part = B[:i]
                if is_valid_partial_split(part, char, char_to_part):
                    new_char_to_part = char_to_part.copy()
                    new_char_to_part[char] = part
                    split_recursive(
                        A[1:],
                        B[i:],
                        current_split + [part],
                        new_char_to_part,
                        all_splits,
                    )

        all_splits = []
        split_recursive(previous_generation, current_generation, [], {}, all_splits)

        return all_splits


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    sys.setrecursionlimit(10000)
    rules = Decoder(sys.argv[1]).decode()
    for ruleset in rules:
        print(f"{ruleset}")
