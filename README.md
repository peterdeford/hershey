# hershey

This folder let's you track the patterns in the roller coaster wait times for Hershey Park, in Hershey PA.

### Usage:

To automatically query the wait times and store them in a file, simply run:

```
python hershey_wait.py
```

To generate graphs to analyze the data, use the command:

```
bokeh serve --show analyze_waits.py
```

This script slows down after using the drop down menu a few times. If this happens, it is better to just quit the script and restart the server.
