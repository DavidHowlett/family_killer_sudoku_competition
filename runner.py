from time import perf_counter as now
import problems
import davids_solver

if __name__ == '__main__':
    start_time = now()
    for i in range(1):
        davids_solver.main(problems.problem1)
    run_time = now()-start_time
    print(run_time)