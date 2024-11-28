from improbable_cpr.generators import CprGenerator
import itertools

for cpr in itertools.islice(CprGenerator(), 100):
    print(cpr)