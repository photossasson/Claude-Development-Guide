#!/usr/bin/env python3
import json, sys, os
d = json.load(sys.stdin)
rec = {k: d.get(k) for k in ("hook_event_name","file_path","memory_type","load_reason","globs","trigger_file_path")}
with open(os.path.join(os.environ.get("CLAUDE_PROJECT_DIR","."), "instructions.log"), "a") as f:
    f.write(json.dumps(rec) + "\n")
