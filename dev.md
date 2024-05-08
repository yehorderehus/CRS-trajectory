**Command to visually format code (modify scripts/ with relative path to the file)**
```sh
autopep8 --max-line-length=999 --in-place scripts/
```

## Known bugs:
- While get.figure() is called, it resets the UI state of the graph (if the user currently dragging it, it doesn't save the state), and uirevisiong flag does not help because it works only for preserving the UI state which has been set in time, temporary solution is to unflag "Updating" before dragging the graph, but it will stop the retrieval and drawing.
- Graph may stop updating with period of time or after some button actions.

**TODOs:**
- Implement correct calculation of the trajectory based on altitude and acceleration with rotation. (Too costly task)