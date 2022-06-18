---
title: Health check a server with 'nohup $(cmd) &'
date: 2022-04-18
tags: Unix
---

While working on a project with [EdgeDB](https://www.edgedb.com/) and
[FastAPI](https://fastapi.tiangolo.com/), I wanted to perform health checks against the
FastAPI server in the GitHub CI. This would notify me about the working state of the
application. The idea is to—

* Run the server in the background.
* Run the commands against the server that'll denote that the app is in a working state.
* Perform cleanup.

The following shell script demonstrates a similar workflow with a Python HTTP server. This script—

* Runs a Python web server in the background.
* Waits for 2 seconds for the server to be ready to accept requests.
* Makes an HTTP request against the server and ensures that it returns HTTP 200 (ok).
* Shuts down the Python process.

```bash
#!/bin/bash

set -euo pipefail

# Run the Python server in the background.
nohup python3 -m http.server 5000 >> /dev/null &

# Give the server enough time to be ready before accepting requests.
sleep 2

# Run the health check.
if [[ $(curl -I http://localhost:5000 2>&1) =~ "200 OK" ]]; then
    echo "Health check passed!"
else
    echo "Health check failed!"
    exit 1
fi

# Cleanup.
pkill -9 -ecfi python
```

The `nohup` before the `python3 -m http.server 5000` makes sure that the `SIGHUP` signal
can't reach the server and shut down the process. The ampersand `&` after the command
runs the process in the background. Afterward, the script waits for two seconds to allow
the server to be ready to process the health check requests. If the health check command
fails, that terminates the script with `exit 1`. Otherwise, the `pkill` command cleans
up the background processes with `SIGKILL` and the script exits with code 0.

Finally, I would add the script invocation command to the CI file to make it automatic.

## References

* [What's the difference between nohup and ampersand](https://stackoverflow.com/questions/15595374/whats-the-difference-between-nohup-and-ampersand)
