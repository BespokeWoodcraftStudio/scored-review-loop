#!/usr/bin/env python3
# Bake a settings file into a copy of a workflow script, so a run is launched by path with no pasted args.
# Usage: python3 make-run.py <script.js> <settings.json> <out.js> [name-suffix]
# The copy replaces `const A = args || {}` with the settings (keep the settings file you baked with the run's record).
import json, sys, re
src, settings, out = sys.argv[1], sys.argv[2], sys.argv[3]
suffix = sys.argv[4] if len(sys.argv) > 4 else json.load(open(settings)).get('name', 'run')
s = open(src).read()
assert 'const A = args || {}' in s, 'script has no args line'
s = s.replace('const A = args || {}', 'const A = ' + json.dumps(json.load(open(settings))) + '  // baked from ' + settings, 1)
s = re.sub(r"name: '([^']+)',", lambda m: "name: '" + m.group(1) + "-" + re.sub(r'[^a-z0-9-]', '-', suffix.lower()) + "',", s, count=1)
open(out, 'w').write(s)
print(out)
