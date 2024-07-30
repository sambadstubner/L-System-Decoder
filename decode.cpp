#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <iterator>
#include <type_traits>

template <typename Key, typename Value>
class Decoder {
    static_assert(std::is_integral<Key>::value || std::is_same<Key, char>::value, "Key must be an integral type or char");

public:
    Decoder(const std::string& file_path) {
        std::ifstream file(file_path);
        if (file.is_open()) {
            std::ostringstream ss;
            ss << file.rdbuf();
            contents = ss.str();
            file.close();
        }

        std::istringstream iss(contents);
        generations = std::vector<std::string>((std::istream_iterator<std::string>(iss)),
                                                std::istream_iterator<std::string>());
    }

    std::vector<std::unordered_map<Key, Value> > decode() {
        rules.clear();
        axiom = generations[0];
        bool found_solution = false;
        for (size_t i = 1; i < generations.size(); ++i) {
            if (!found_solution) {
                std::cout << "No found solution yet, decoding generation " << i << std::endl;
                auto local_solutions = find_possible_solutions(generations[i - 1], generations[i]);

                update_possible_solutions(local_solutions);

                auto solutions = possible_solutions;
                for (const auto& solution : solutions) {
                    for (size_t j = 1; j < generations.size(); ++j) {
                        if (generate(generations[j - 1], solution) != generations[j]) {
                            break;
                        }

                        if (j == (generations.size() - 1)) {
                            std::cout << "Found solution: {";
                            for (const auto& pair : solution) {
                                std::cout << pair.first << ": " << pair.second << ", ";
                            }
                            std::cout << "}" << std::endl;
                            found_solution = true;
                            if (std::find(valid_solutions.begin(), valid_solutions.end(), solution) == valid_solutions.end()) {
                                valid_solutions.push_back(solution);
                            }
                        }
                    }
                }
            }
        }
        return valid_solutions;
    }

private:
    std::string contents;
    std::vector<std::string> generations;
    std::unordered_map<Key, Value> rules;
    std::string axiom;
    std::vector<std::unordered_map<Key, Value> > possible_solutions;
    std::vector<std::unordered_map<Key, Value> > valid_solutions;

    void update_possible_solutions(const std::vector<std::unordered_map<Key, Value> >& new_solutions) {
        auto previous_solutions = possible_solutions;
        possible_solutions.clear();

        for (const auto& new_sol : new_solutions) {
            bool has_subset = false;
            for (auto& prev_sol : previous_solutions) {
                if (is_dict_subset(prev_sol, new_sol)) {
                    has_subset = true;
                    for (const auto& pair : new_sol) {
                        prev_sol[pair.first] = pair.second;
                    }
                    possible_solutions.push_back(prev_sol);
                }
            }
            if (!has_subset) {
                possible_solutions.push_back(new_sol);
            }
        }
    }

    bool is_dict_subset(const std::unordered_map<Key, Value>& dict_a,
                        const std::unordered_map<Key, Value>& dict_b) const {
        for (const auto& [key_a, value_a] : dict_a) {
            auto it = dict_b.find(key_a);
            if (it != dict_b.end() && it->second != value_a) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::unordered_map<Key, Value> > find_possible_solutions(const std::string& previous_generation,
                                                                        const std::string& current_generation) {
        auto splits = split_generation(previous_generation, current_generation);
        std::vector<std::unordered_map<Key, Value> > solutions;
        for (const auto& split : splits) {
            std::unordered_map<Key, Value> solution;
            for (size_t i = 0; i < previous_generation.size(); ++i) {
                solution[previous_generation[i]] = split[i];
            }
            solutions.push_back(solution);
        }
        return solutions;
    }

    std::string generate(const std::string& current_population,
                         const std::unordered_map<Key, Value>& rules) const {
        std::string new_population;
        for (char c : current_population) {
            if (rules.find(c) != rules.end()) {
                new_population += rules.at(c);
            } else {
                new_population += c;
            }
        }
        return new_population;
    }

    std::vector<std::vector<std::string> > split_generation(const std::string& previous_generation,
                                                           const std::string& current_generation) const {
        std::vector<std::vector<std::string> > all_splits;
        split_recursive(previous_generation, current_generation, {}, {}, all_splits);
        return all_splits;
    }

    void split_recursive(const std::string& A, const std::string& B,
                         std::vector<std::string> current_split,
                         std::unordered_map<Key, Value> char_to_part,
                         std::vector<std::vector<std::string> >& all_splits) const {
        if (A.empty()) {
            if (B.empty()) {
                all_splits.push_back(current_split);
            }
            return;
        }

        char char_a = A[0];
        for (size_t i = 1; i <= B.size() - A.size() + 1; ++i) {
            std::string part = B.substr(0, i);
            if (is_valid_partial_split(part, char_a, char_to_part)) {
                auto new_char_to_part = char_to_part;
                new_char_to_part[char_a] = part;
                auto new_current_split = current_split;
                new_current_split.push_back(part);
                split_recursive(A.substr(1), B.substr(i), new_current_split, new_char_to_part, all_splits);
            }
        }
    }

    bool is_valid_partial_split(const std::string& part, char char_a,
                                const std::unordered_map<Key, Value>& char_to_part) const {
        auto it = char_to_part.find(char_a);
        if (it != char_to_part.end()) {
            return it->second == part;
        }
        return true;
    }
};

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <file_path>" << std::endl;
        return 1;
    }

    Decoder<char, std::string> decoder(argv[1]);
    auto rules = decoder.decode();
    std::cout << "Rules:" << std::endl;
    for (const auto& ruleset : rules) {
        for (const auto& pair : ruleset) {
            std::cout << pair.first << "->" << pair.second << std::endl;
        }
        std::cout << std::endl;
    }

    return 0;
}
