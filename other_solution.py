from recordtype import recordtype
import glob
import time


LibraryInfo = recordtype("LibraryInfo", "number_of_books days_for_signup ship_factor books")


libraries = {}
books_scores = {}
checked_books = []


def comparator(days_remaining, library_id):
    score = calc_potential_score(days_remaining, libraries[library_id])

    if not score:
        inf = float("inf")

        return inf, inf, inf

    days_for_signup = libraries[library_id].days_for_signup / score
    ship_factor = libraries[library_id].ship_factor / score
    try:
        best_books_score = -books_scores[libraries[library_id].books[0]]
    except IndexError:
        best_books_score = float("inf")
    
    return days_for_signup, ship_factor, best_books_score


def sort_libraries(libraries_to_sort, days_remaining):
    for index in range(len(libraries_to_sort)):
        libraries[libraries_to_sort[index]].books = list(filter(lambda book_id: not checked_books[book_id], libraries[libraries_to_sort[index]].books))

    return sorted(libraries_to_sort, key=lambda library_id: comparator(days_remaining, library_id))


def calc_potential_score(days_for_scanning, library):
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
    true_score = calc_potential_score(days_remaining, library)
    sended_books = []
    index = 0

    while true_score > 0:
        sended_books += [books[index]]
        checked_books[books[index]] = True
        true_score -= books_scores[books[index]]
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


input_files = [input_file_name for input_file_name in glob.glob("input\\*.txt")]

init_time = time.time()

for input_file in input_files:
    start_time = time.time()
    process(input_file)
    print(f"{input_file} processed in {time.time() - start_time} seconds")

print(f"All files processed in {time.time() - init_time} seconds")