import itertools

from improbable_cpr.generators import CprGenerator


for cpr in itertools.islice(CprGenerator(), 100):
    print(cpr)
