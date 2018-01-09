from time import perf_counter as now
import problems
import david_solver
import robert_solver
import michael_solver

david_total_time = 0
robert_total_time = 0
michael_total_time = 0

if __name__ == '__main__':
    for problem_name, problem in problems.problems.items():
        start_time = now()
        david_solver.main(problem)
        run_time = now()-start_time
        david_total_time += run_time
        print(f'David took {run_time:.4f} seconds to run', problem_name)
        # print(david_solver.add_value_calls, 'add_value_calls')
        # print(david_solver.bad_guesses, 'bad_guesses')

    for problem_name, problem in problems.problems.items():
        start_time = now()
        robert_solver.main(problem)
        run_time = now()-start_time
        robert_total_time += run_time
        print(f'Robert took {run_time:.4f} seconds to run', problem_name)

    for problem_name, problem in problems.problems.items():
        start_time = now()
        if '2' not in problem_name:  # problem 2 takes too long to solve right now
            michael_solver.main(problem)
        run_time = now()-start_time
        michael_total_time += run_time
        print(f'Michael took {run_time:.4f} seconds to run', problem_name)

print('David total time:', david_total_time)
print('Robert total time:', robert_total_time)
print('Michael total time:', michael_total_time)
