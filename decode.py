import logging
from pathlib import Path
import sys



class Decoder:

    def __init__(self, file_path: Path) -> None:
        with open(file_path, "r") as f:
            self.contents = f.read()
            self.possible_solutions = []

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
                self.possible_solutions += local_solutions
                logging.debug(self.possible_solutions)
                # iterate through the possible solutions to see if it solves the next ones
                solutions = self.possible_solutions.copy()
                for solution in solutions:
                    for i in range(1, len(self.generations)):
                        if (
                            self.generate(self.generations[i - 1], solution)
                            != self.generations[i]
                        ):
                            self.possible_solutions.remove(solution)
                            break
                        if i == (len(self.generations) - 1):
                            logging.info(f"Found solution: {solution}")
                            found_solution = True
                            if solution not in self.possible_solutions:
                                self.possible_solutions.append(solution)

        logging.info("Done Find Possible Solutions")
        return self.possible_solutions

    def find_possible_solutions(self, previous_generation: str, current_generation: str) -> list[dict]:
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

        def split_recursive(A: str, B: str, current_split: list, char_to_part: dict, all_splits: list) -> None:
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
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    rules = Decoder(sys.argv[1]).decode()
    for ruleset in rules:
        print(f"{ruleset}")
