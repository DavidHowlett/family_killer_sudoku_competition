from time import perf_counter as now
import inspect
import hashlib
import problems
import david_1_solver
import david_2_solver
import robert_solver
import michael_solver

solvers = [
    ('David 1', david_1_solver),
    ('David 2', david_2_solver),
    ('Robert', robert_solver),
    ('Michael', michael_solver),
]

if __name__ == '__main__':
    for author, solver in solvers:
        solver.total_time_taken = 0
        for problem_name, problem in problems.problems.items():
            # this line makes things the same on windows and unix
            normalised_source = '\n'.join(inspect.getsource(solver).split())
            hash = hashlib.sha256(normalised_source.encode()).hexdigest()
            file_name = f'results cache/{hash} {problem_name}.txt'
            try:
                run_time = float(open(file_name).read())
            except FileNotFoundError:
                # in the event that the lookup fails actually run the test
                start_time = now()
                solver.main(problem)
                run_time = now()-start_time
                open(file_name, 'w').write(str(run_time))
            solver.total_time_taken += run_time
            print(f'{author} took {run_time:.4f} seconds to run {problem_name}')
            # print(david_solver.add_value_calls, 'add_value_calls')
            # print(david_solver.bad_guesses, 'bad_guesses')

    for author, solver in solvers:
        print(f'{author} total time: {solver.total_time_taken}')
