import random


def calculate_fitness(chromosome, subjects, rows, cols):
    """
    chromosome: permutation of student IDs
    subjects: dictionary {student_id: subject_code}
    rows, cols: seating grid dimensions

    Counts adjacent students having the same subject.
    Adjacent means horizontal + vertical.
    """

    conflicts = 0

    grid = [
        chromosome[i * cols:(i + 1) * cols]
        for i in range(rows)
    ]

    
    for r in range(rows):
        for c in range(cols):

            current_student = grid[r][c]
            current_subject = subjects[current_student]

            if c + 1 < cols:
                right_student = grid[r][c + 1]

                if current_subject == subjects[right_student]:
                    conflicts += 1

            if r + 1 < rows:
                bottom_student = grid[r + 1][c]

                if current_subject == subjects[bottom_student]:
                    conflicts += 1


    return 1 / (1 + conflicts)



def create_population(students, population_size):
    population = []

    for _ in range(population_size):
        chromosome = students.copy()
        random.shuffle(chromosome)
        population.append(chromosome)

    return population


def selection(population, subjects, rows, cols, tournament_size=3):

    tournament = random.sample(
        population,
        tournament_size
    )


    winner = max(
        tournament,
        key=lambda chromosome:
        calculate_fitness(chromosome, subjects, rows, cols)
    )

    return winner.copy()




def order_crossover(parent1, parent2):

    size = len(parent1)


    start, end = sorted(
        random.sample(range(size), 2)
    )


    child = [None] * size


    child[start:end] = parent1[start:end]


    remaining = [
        student
        for student in parent2
        if student not in child
    ]

    index = 0

    for i in range(size):

        if child[i] is None:
            child[i] = remaining[index]
            index += 1

    return child




def swap_mutation(chromosome, mutation_rate=0.1):

    if random.random() < mutation_rate:

        i, j = random.sample(
            range(len(chromosome)), 2
        )

        chromosome[i], chromosome[j] = (
            chromosome[j],
            chromosome[i]
        )

    return chromosome



def genetic_algorithm(
        students,
        subjects,
        rows,
        cols,
        population_size=100,
        generations=500,
        mutation_rate=0.1,
        elite_size=2):

    population = create_population(
        students,
        population_size
    )

    best_solution = None
    best_fitness = -1

    for generation in range(generations):


        population.sort(
            key=lambda chromosome:
            calculate_fitness(
                chromosome,
                subjects,
                rows,
                cols
            ),
            reverse=True
        )

        current_best = population[0]

        current_fitness = calculate_fitness(
            current_best,
            subjects,
            rows,
            cols
        )


        if current_fitness > best_fitness:

            best_fitness = current_fitness
            best_solution = current_best.copy()


        if best_fitness == 1.0:
            print(
                f"Perfect solution found at generation "
                f"{generation}"
            )
            break

     

        new_population = []

        for i in range(elite_size):
            new_population.append(
                population[i].copy()
            )

      
        while len(new_population) < population_size:

            parent1 = selection(
                population,
                subjects,
                rows,
                cols
            )

            parent2 = selection(
                population,
                subjects,
                rows,
                cols
            )

           
            child = order_crossover(
                parent1,
                parent2
            )

            # Swap mutation
            child = swap_mutation(
                child,
                mutation_rate
            )

            new_population.append(child)

        population = new_population

    return best_solution, best_fitness


# ---------------------------------------------------------
# 7. DISPLAY SEATING CHART
# ---------------------------------------------------------

def print_seating_chart(
        chromosome,
        subjects,
        rows,
        cols):

    print("\nSeating Chart")
    print("-" * (cols * 15))

    for r in range(rows):

        row = chromosome[
            r * cols:(r + 1) * cols
        ]

        for student in row:
            print(
                f"{student}({subjects[student]})",
                end="\t"
            )

        print()

    print("-" * (cols * 15))


# ---------------------------------------------------------
# 8. MAIN PROGRAM
# ---------------------------------------------------------

if __name__ == "__main__":

    # Student IDs
    students = [
        "S1", "S2", "S3", "S4",
        "S5", "S6", "S7", "S8",
        "S9", "S10", "S11", "S12"
    ]

    # Subject code of each student
    subjects = {
        "S1": "CS",
        "S2": "CS",
        "S3": "CS",

        "S4": "EC",
        "S5": "EC",
        "S6": "EC",

        "S7": "ME",
        "S8": "ME",
        "S9": "ME",

        "S10": "EE",
        "S11": "EE",
        "S12": "EE"
    }

    # Exam hall size
    rows = 3
    cols = 4

    # Run Genetic Algorithm
    best_solution, best_fitness = genetic_algorithm(
        students=students,
        subjects=subjects,
        rows=rows,
        cols=cols,
        population_size=100,
        generations=500,
        mutation_rate=0.1,
        elite_size=2
    )

    # Display result
    print("\nBest Fitness:", best_fitness)

    print_seating_chart(
        best_solution,
        subjects,
        rows,
        cols
    )
