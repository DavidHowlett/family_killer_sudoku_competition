from time import perf_counter as now
import problems
import david_solver
import robert_solver

if __name__ == '__main__':
    for problem_name, problem in problems.problems.items():
        start_time = now()
        # for i in range(5):
        david_solver.main(problem)
        run_time = now()-start_time
        print(f'{run_time:.4f} seconds to run', problem_name)
        # print(david_solver.add_value_calls, 'add_value_calls')
        # print(david_solver.bad_guesses, 'bad_guesses')
    ct = now()
    robert_solver.main("problem 2")
    print(now()-ct)