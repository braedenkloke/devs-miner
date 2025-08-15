# DEVS-miner
Process mining algorithms for [DEVS](https://en.wikipedia.org/wiki/DEVS) models.

# Usage

*Tested with Python 3.11*

With `$PYTHON_PATH` set to `$PWD`, run
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
python3 examples/discover_atomic_devs_model_of_manufacturing_sys.py` 
```

Your output will be
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
