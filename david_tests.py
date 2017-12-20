import timeit
import davids_solver as ds

for loc in range(81):
    assert len(ds.group_memberships[loc]) == 3
    assert len(ds.friends[loc]) == 20


print(timeit.timeit("{3,4,5}.__iter__().__next__()", number=1_000_000))
print(timeit.timeit("min({3,4,5})", number=1_000_000))

print('it all works!')

