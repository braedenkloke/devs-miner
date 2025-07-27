# DEVS-miner
Process mining discovery algorithms for [DEVS](https://en.wikipedia.org/wiki/DEVS) models.

# Usage
Here is a simple example for how to use this library
```
from devs_miner import read_file, discover_atomic_devs_of_ms

if __name__ == "__main__":
    event_log = read_file.read_csv('<path-to-csv-event-log-file.csv>')
    state_log = read_file.read_csv('<path-to-csv-state-log-file.csv>')
    X, Y, S, q_init, ta, ext_trans, int_trans, output = discover_atomic_devs_of_ms.execute(event_log, state_log)
```

`examples/main.py` implements the above code for a event and state log of a manufacturing system.
Running the example outputs
```
X: {'enter'}
Y: {'end'}
S: {'busy', 'idle'}
ta: {('busy', 5.0), ('idle', inf)}
ext_trans: {(('idle', 'enter'), 'busy')}
int_trans: {('busy', 'idle')}
output: {('busy', 'end')}
```

# Acknowledgements
- [Sanja Lazarova-Molnar](https://lazarova-molnar.net/) and the [SYDSEN Research Group](https://sydsen.aifb.kit.edu/) 
- [Gabriel Wainer](https://www.sce.carleton.ca/faculty/wainer/doku.php) and the [ARSLab](https://arslab.sce.carleton.ca/) 
- [Mitacs Globalink Research Award](https://www.mitacs.ca/our-programs/globalink-research-award/)

# See Also
- [Manufacturing system DEVS model and simulation](https://github.com/braedenkloke/smart-manufacturing-system-devs-model)
- [PM4PY - Process mining for Python](https://github.com/process-intelligence-solutions/pm4py)
- [hackergrrl/art-of-readme](https://github.com/hackergrrl/art-of-readme)

# License
[MIT](https://choosealicense.com/licenses/mit/)
