from recordtype import recordtype


LibraryInfo = recordtype("LibraryInfo", "number_of_books days_for_signup ship_factor books")


libraries = {}
books_scores = {}
checked_books = []


def sort_libraries(libraries_to_sort, days_remaining):
    for index in range(len(libraries_to_sort)):
        books = [book for book in libraries[libraries_to_sort[index]].books if not checked_books[book]]
        libraries[libraries_to_sort[index]].books = books

    return sorted(libraries_to_sort, key=lambda library_id: calc_potential_value(days_remaining, libraries[library_id]))[::-1]


def calc_potential_value(days_for_scanning, library):
    days_remaining = days_for_scanning - library.days_for_signup
    books = library.books
    ship_per_day = library.ship_factor
    index = 0
    value = 0
    exit_from_loop = False

    for _ in range(days_remaining):
        for _ in range(ship_per_day):
            try:
                value += books_scores[books[index]]
                index += 1
            except IndexError:
                exit_from_loop = True
                break

        if exit_from_loop:
            break
    
    return value


def send_books(library, days_remaining):
    global checked_books

    books = library.books
    true_value = calc_potential_value(days_remaining, library)
    sended_books = []
    index = 0

    while true_value > 0:
        sended_books += [books[index]]
        checked_books[books[index]] = True
        true_value -= books_scores[books[index]]
        index += 1
    
    return sended_books


def solve(libraries, books_scores, days_for_scanning):
    sorted_libraries = sort_libraries(list(libraries), days_for_scanning)
    solution = {}
    index = 0

    while index < len(sorted_libraries):
        days_for_scanning -= libraries[sorted_libraries[index]].days_for_signup
        if days_for_scanning <= 0:
            break
        solution[sorted_libraries[index]] = send_books(libraries[sorted_libraries[index]], days_for_scanning + libraries[sorted_libraries[index]].days_for_signup)
        sorted_libraries = sort_libraries(sorted_libraries[1:], days_for_scanning)

    return solution


def process(input_file_name):
    with open(input_file_name) as input_file:
        global libraries, books_scores, checked_books
        
        libraries, books_scores, checked_books = {}, {}, []

        number_of_books, number_of_libraries, days_for_scanning = [int(value) for value in input_file.readline().split()]
        books_scores = {int(book_id): int(score) for book_id, score in enumerate(input_file.readline().split())}
        checked_books = [False for _ in books_scores]
        
        for index, line in enumerate(input_file):
            number_of_books_of_the_library, signup_process, ship_factor = [int(value) for value in line.split()]
            books_in_library = sorted([int(book_id) for book_id in input_file.readline().split()], key=lambda book_id: books_scores[book_id])[::-1]
            libraries[index] = LibraryInfo(number_of_books_of_the_library, signup_process, ship_factor, books_in_library)
        
    solution = solve(libraries, books_scores, days_for_scanning)

    output_file_name = input_file_name.replace("txt", "out").replace("input", "output")
    with open(output_file_name, "w") as output_file:
        output_file.write(str(len(solution)) + "\n")
        for key in solution:
            output_file.write(str(key) + " " + str(len(solution[key])) + "\n")
            output_file.write(" ".join(str(value) for value in solution[key]) + "\n")


process("input\\a_example.txt") 

process("input\\b_read_on.txt")

process("input\\c_incunabula.txt")

process("input\\d_tough_choices.txt")

process("input\\e_so_many_books.txt")

process("input\\f_libraries_of_the_world.txt") 