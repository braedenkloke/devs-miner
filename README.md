# DEVS-miner
Process mining discovery algorithms for [DEVS](https://en.wikipedia.org/wiki/DEVS) models.

# Usage
Run
```
import devs_miner

if __name__ == "__main__":
    event_log = devs_miner.read_csv('<path-to-csv-event-log-file.csv>')
    state_log = devs_miner.read_csv('<path-to-csv-state-log-file.csv>')
    X, Y, S, q_init, ta, ext_trans, int_trans, output = devs_miner.discover_devs(event_log, state_log)
```

# Acknowledgements
- [Sanja Lazarova-Molnar](https://lazarova-molnar.net/) and the [SYDSEN Research Group](https://sydsen.aifb.kit.edu/) 
- [Gabriel Wainer](https://www.sce.carleton.ca/faculty/wainer/doku.php) and the [ARSLab](https://arslab.sce.carleton.ca/) 
- [Mitacs Globalink Research Award](https://www.mitacs.ca/our-programs/globalink-research-award/)

# See Also
- [PM4PY](https://github.com/process-intelligence-solutions/pm4py) 
- [PySPN](https://github.com/jo-chr/pyspn)
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [hackergrrl/art-of-readme](https://github.com/hackergrrl/art-of-readme)

# License
[MIT](https://choosealicense.com/licenses/mit/)
