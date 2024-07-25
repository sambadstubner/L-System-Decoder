def split_string(A, B):
    # Helper function to check if all parts corresponding to a repeated character in A are the same
    def is_valid_split(parts, A):
        char_to_part = {}
        for char, part in zip(A, parts):
            if char in char_to_part:
                if char_to_part[char] != part:
                    return False
            else:
                char_to_part[char] = part
        return True

    # Recursive function to generate all possible splits
    def split_recursive(A, B, current_split, all_splits):
        if not A:
            if not B:
                all_splits.append(current_split)
            return
        
        for i in range(1, len(B) - len(A) + 2):
            part = B[:i]
            new_split = current_split + [part]
            split_recursive(A[1:], B[i:], new_split, all_splits)
    
    all_splits = []
    split_recursive(A, B, [], all_splits)
    
    # Filter valid splits
    valid_splits = [split for split in all_splits if is_valid_split(split, A)]
    
    return valid_splits

# Example usage
A = "1[0]0"
B = "11[1[0]0]1[0]0"
result = split_string(A, B)
for split in result:
    print(split)
