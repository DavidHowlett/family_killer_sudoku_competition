from time import perf_counter as now
import copy
import problems
import david_solver
import robert_solver
import micheal_solver

david_total_time = 0
robert_total_time = 0
micheal_total_time = 0

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
        micheal_solver.main(copy.deepcopy(problem))
        run_time = now()-start_time
        micheal_total_time += run_time
        print(f'Micheal took {run_time:.4f} seconds to run', problem_name)

    for problem_name, problem in problems.problems.items():
        start_time = now()
        robert_solver.main(problem_name)
        run_time = now()-start_time
        robert_total_time += run_time
        print(f'Robert took {run_time:.4f} seconds to run', problem_name)

print('David total time:', david_total_time)
print('Robert total time:', robert_total_time)
print('Micheal total time:', micheal_total_time)