from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import List

from tqdm import tqdm

class Decoder:

    def __init__(self, file_path: Path) -> None:
        with open(file_path, 'r') as f:
            self.contents = f.read()
            self.possible_solutions = []
        
        self.generations = self.contents.split()

    def decode(self):
        self.rules = {}
        self.axiom = self.generations[0]
        found_solution = False
        for i in range(1, len(self.generations)):
            """
            Each generation try to solve for the next generation with the current solution if it is correct then keep going
            If it is not then through it away
            If none is found then do a full search
            """
            if not found_solution:
                print(f"No found solution yet, decoding generation {i}")
                local_solutions = self.decode_generation(self.generations[i-1], self.generations[i])
                print(f'local solution: {local_solutions}')
                self.possible_solutions += local_solutions
                print(self.possible_solutions)
                # iterate through the possible solutions to see if it solves the next ones
                solutions = self.possible_solutions.copy()
                for solution in solutions:
                    for i in range(1, len(self.generations)):
                        if self.generate(self.generations[i - 1], solution) != self.generations[i]:
                            # print(f'Generations do not match\n{self.generate(self.generations[i - 1], solution)} -> {self.generations[i]}')
                            self.possible_solutions.remove(solution)
                            break
                        if i == (len(self.generations) - 1):
                            print(f'Found solution!: {solution}')
                            found_solution = True
                            if solution not in self.possible_solutions:
                                self.possible_solutions.append(solution)


        print("\n\nDone Find Possible Solutions")
        # common_rules = self.find_unique_consistent_dicts(self.possible_solutions[1:])
        return self.possible_solutions


    

    def decode_generation(self, previous_generation: str, current_generation: str):
        splits = self.split_string(current_generation, len(previous_generation) - 1)
        possible_rules = []
        if len(splits) == 1:
            return [{previous_generation: current_generation}]
        print("Filtering split string results")
        for split in splits:
            invalid_solution = False
            local_solution = {}
            for prev_node, curr_node in zip(previous_generation, split):
                # Check for rule contradictions
                if invalid_solution or (prev_node in local_solution.keys() and local_solution[prev_node] != curr_node):
                    invalid_solution = True
                    break
                local_solution[prev_node] = curr_node

            if not invalid_solution:
                possible_rules.append(dict(zip(previous_generation, split)))

        return possible_rules
    
    @staticmethod
    def generate(current_population:str, rules:dict) -> str:
        new_population = ""
        for i in current_population:
            if i in rules.keys():
                new_population += rules[i]
            else:
                new_population += i
        
        return new_population

    @staticmethod
    def split_string(input_string: str, n: int) -> List[str]:
        """
        Try splitting at where the previous generation occurs
        """


        print(f" - Splitting string: {input_string}")
        
        # Base case: if n is 0, return the whole string as the only "split"
        if n == 0:
            return [input_string]
        
        # List to hold all possible ways to split the string
        results = []
        
        # Generate all possible combinations of split points
        split_combinations = list(combinations(range(1, len(input_string)), n))
        print("Found all possible split combinations")

        # Initialize tqdm progress bar
        with tqdm(total=len(split_combinations), desc="Processing splits") as pbar:
            for split_points in split_combinations:
                # Initialize start index
                start = 0
                # List to hold parts of the current split
                split_parts = []
                for point in split_points:
                    # Add the substring from start to the split point
                    split_parts.append(input_string[start:point])
                    # Update start index
                    start = point
                # Add the final substring from the last split point to the end of the string
                split_parts.append(input_string[start:])
                # Add this split configuration to results
                results.append(split_parts)
                pbar.update(1)  # Update the progress bar
        
        return results
    
    @staticmethod
    def find_unique_consistent_dicts(lists):
        if not lists:
            return []

        # Group dictionaries by their size
        size_groups = defaultdict(list)
        for sublist in lists:
            for d in sublist:
                size_groups[len(d)].append(d)
        
        # To track unique consistent dictionaries
        unique_dicts = set()
        
        # Process each group of dictionaries with the same size
        for size, dicts in size_groups.items():
            # Track key-value pairs and their occurrences in each sublist
            kv_occurrences = defaultdict(lambda: defaultdict(int))
            
            for sublist in lists:
                seen_kvs = set()
                for d in sublist:
                    if len(d) == size:
                        for k, v in d.items():
                            if (k, v) not in seen_kvs:
                                kv_occurrences[k][v] += 1
                                seen_kvs.add((k, v))
            
            # Identify conflicting key-value pairs
            conflicting_kvs = set()
            total_sublists = len(lists)
            for k, v_counts in kv_occurrences.items():
                for v, count in v_counts.items():
                    if count != total_sublists:
                        conflicting_kvs.add((k, v))

            # Check if a dictionary contains conflicting key-value pairs
            def is_consistent(d):
                return not any((k, v) in conflicting_kvs for k, v in d.items())
            
            # Collect unique dictionaries that are consistent across all sublists
            for d in dicts:
                if is_consistent(d):
                    unique_dicts.add(frozenset(d.items()))
        
        # Convert frozensets back to dictionaries
        return [dict(fs) for fs in unique_dicts]








if __name__ == '__main__':
    decoder = Decoder('koch.txt')
    rules = decoder.decode()
    for ruleset in rules:
        print(f"{ruleset}\n\n")