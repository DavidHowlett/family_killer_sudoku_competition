from time import perf_counter as now
import problems
import davids_solver

start_time = now()
davids_solver.main(problems.problem1)
run_time = now()-start_time
print(run_time)