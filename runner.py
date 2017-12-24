from time import perf_counter as now
import problems
import davids_solver

if __name__ == '__main__':
    start_time = now()
    for i in range(1):
        davids_solver.main(problems.problem2)
    run_time = now()-start_time
    print(f'{run_time:.4f} seconds to run')
    print(davids_solver.add_value_calls, 'add_value_calls')
