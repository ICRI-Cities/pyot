#
# PyoT (Main)
#
# Michael Rosen
# mrrosen
# 15-10-2015
#

import os

# Generate list of all python scripts in the directory
scripts = [];
for f in os.listdir("scripts"):
  if (f.endswith(".py")):
    print("-M- Found script '%s'" % f);
    try:
      with open(f[:-3] + ".arg") as fh:
        args = fh.readline().replace("\n", "");
        print("-M- Found args '%s'" % args);
    except:
      args = "";
      print("-M- No argument file found");
      
    scripts.append({'script': f, 'args': args});

# Run all the found commands    
for s in scripts:
  cmd = "python scripts/" + s['script'] + " " + s['args'] + " &";
  print("-M- Running: %s" % cmd);
  os.system(cmd);