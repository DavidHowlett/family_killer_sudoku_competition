from time import perf_counter as now
import problems
import davids_solver

if __name__ == '__main__':
    for problem, problem_name in ((problems.problem1, 'problem 1'), (problems.problem2, 'problem 2')):
        start_time = now()
        davids_solver.main(problem)
        run_time = now()-start_time
        print(f'{run_time:.4f} seconds to run for ', problem_name)
        print(davids_solver.add_value_calls, 'add_value_calls')
        print(davids_solver.bad_guesses, 'bad_guesses')
