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
        solver.total_bad_guesses = 0
        for problem_name, problem in problems.problems.items():
            # this line makes things the same on windows and unix
            normalised_source = '\n'.join(inspect.getsource(solver).split())
            hash = hashlib.sha256(normalised_source.encode()).hexdigest()
            file_name = f'results cache/{hash} {problem_name}.txt'
            try:
                file = open(file_name)
                run_time = float(file.readline())
                bad_guesses = int(file.readline())
            except (FileNotFoundError, ValueError):
                # in the event that the lookup fails actually run the test
                start_time = now()
                result, bad_guesses = solver.main(problem)
                run_time = now()-start_time
                open(file_name, 'w').write(f'{run_time}\n{bad_guesses}\n{result}')
            solver.total_time_taken += run_time
            solver.total_bad_guesses += bad_guesses
            print(f'{author} took {run_time:.4f} seconds and {bad_guesses} bad guesses to run {problem_name}')
            # print(david_solver.add_value_calls, 'add_value_calls')
            # print(david_solver.bad_guesses, 'bad_guesses')

    for author, solver in solvers:
        print(f'{author} took a total of {solver.total_time_taken:.3f} seconds '
              f'and {solver.total_bad_guesses} bad guesses. Each bad guess took '
              f'{1000*solver.total_time_taken/solver.total_bad_guesses:.3f} milliseconds on average')
