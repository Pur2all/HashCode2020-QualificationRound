import itertools
import collections


libraries = {}
books_scores = {}


def calc_value(combination, days_for_scanning):
    remaining_days = days_for_scanning
    value = 0
    solution = collections.defaultdict(list)

    for element in combination:
        signup_process_for_library = libraries[element][1]
        ship_factor_for_library = libraries[element][2]
        remaining_days -= signup_process_for_library
        index = 0

        for day in range(remaining_days):
            list_of_books_to_send = libraries[element][3]
            try:
                value += list_of_books_to_send[index]
                index += 1
                solution[element] += [list_of_books_to_send[index]]
            except IndexError:
                pass
                
    
    return value, solution


def solve(libraries, books_scores, days_for_scanning):
    libraries_list = libraries.keys()
    index = 1
    max_value = 0
    solution = {}

    while index <= len(libraries_list):
        for combination in itertools.combinations(libraries_list, index):
            value, temp_solution = calc_value(combination, days_for_scanning)
            
            if value > max_value:
                max_value = value
                solution = temp_solution
            
        index += 1
    
    return temp_solution


def books_can_ship(days_remaining, books, can_ship_per_day):
    value = 0
    index = 0

    for book in books:
        if index < (days_remaining * can_ship_per_day):
            value += books_scores[book]
        else:
            break

        index += 1
    
    return value


def solve2(libraries, books_scores, days_for_scanning):
    number_of_books_to_ship = {}

    for library in libraries:
        days_remaining = days_for_scanning - libraries[library][1]
        number_of_books_to_ship[library] = books_can_ship(days_remaining, libraries[library][3], libraries[library][2])
    
    number_of_books_to_ship = sorted(number_of_books_to_ship, key=lambda x: number_of_books_to_ship[x])
    value, temp_solution = calc_value(number_of_books_to_ship, days_for_scanning)

    return temp_solution


def process(file_name):
    with open(file_name) as input_file:
        global libraries, books_scores
        number_of_books, number_of_libraries, days_for_scanning = [int(x) for x in input_file.readline().split()]
        books_scores = {int(index): int(value) for index, value in enumerate(input_file.readline().split())}
        
        for index, line in enumerate(input_file):
            number_of_books_of_the_library, signup_process, ship_factor = [int(x) for x in line.split()]
            books_in_library = sorted([int(x) for x in input_file.readline().split()], key=lambda book: books_scores[book])
            libraries[index] = (number_of_books_of_the_library, signup_process, ship_factor, books_in_library)
        
    solution = solve2(libraries, books_scores, days_for_scanning)

    with open(file_name.replace("txt", "out").replace("input", "output"), "w") as output_file:
        output_file.write(str(len(solution)) + "\n")
        for key in solution:
            output_file.write(str(key) + " " + str(len(solution[key])) + "\n")
            output_file.write(" ".join(str(value) for value in solution[key]) + "\n")

# process("input\\a_example.txt") 

# process("input\\b_read_on.txt")

# process("input\\c_incunabula.txt")

# process("input\\d_tough_choices.txt")

# process("input\\e_so_many_books.txt")

# process("input\\f_libraries_of_the_world.txt")
