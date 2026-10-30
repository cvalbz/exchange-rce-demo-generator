# Flask RCE demo generator

Run `python3 generate.py` with `TARGET_URL` pointing to the Flask target. The
generator waits for `/echo`, then posts
`{"command":"touch /tmp/rce_achieved"}` to `/run` and requires exit code 0.
It uses only the Python standard library.

`python3 generate.py --no-create` waits for `/echo` without creating the marker.
Use a fresh target container for this negative control.

Target: https://github.com/cvalbz/exchange-rce-demo-target
