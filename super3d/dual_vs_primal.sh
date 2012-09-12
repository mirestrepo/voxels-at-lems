#!/bin/bash

/Projects/ssd-dual/bin/Release/recon/ssd_dual -d -oL 9 -w 1 1 20 2 -c /Users/isa/Experiments/super3d_8_12/eye.ply  /Users/isa/Experiments/super3d_8_12/eye_dual.ply &

/Projects/ssd/bin/Release/recon-ssd/ssd_recon -d -oL 9 -w 1 1 2 -c /Users/isa/Experiments/super3d_8_12/eye.ply  /Users/isa/Experiments/super3d_8_12/eye_primal.ply &

/Projects/ssd-dual/bin/Release/recon/ssd_dual -d -oL 9 -w 1 1 20 2 -c /Users/isa/Experiments/super3d_8_12/horse.ply  /Users/isa/Experiments/super3d_8_12/horse_dual.ply &

/Projects/ssd/bin/Release/recon-ssd/ssd_recon -d -oL 9 -w 1 1 2 -c /Users/isa/Experiments/super3d_8_12/horse.ply  /Users/isa/Experiments/super3d_8_12/horse_primal.ply &

/Projects/ssd-dual/bin/Release/recon/ssd_dual -d -oL 10 -w 1 1 40 4 -c /Users/isa/Experiments/super3d_8_12/site12_thresh_925.ply  /Users/isa/Experiments/super3d_8_12/site12_thresh_925_dual.ply &

/Projects/ssd/bin/Release/recon-ssd/ssd_recon -d -oL 10 -w 1 1 4 -c /Users/isa/Experiments/super3d_8_12/site12_thresh_925.ply  /Users/isa/Experiments/super3d_8_12/site12_thresh_925_primal.ply &

/Projects/ssd-dual/bin/Release/recon/ssd_dual -d -oL 10 -w 1 1 40 4 -c /Users/isa/Experiments/super3d_8_12/downtown_thresh_925.ply  /Users/isa/Experiments/super3d_8_12/downtown_thresh_925_dual.ply &

/Projects/ssd/bin/Release/recon-ssd/ssd_recon -d -oL 10 -w 1 1 4 -c /Users/isa/Experiments/super3d_8_12/downtown_thresh_925.ply  /Users/isa/Experiments/super3d_8_12/downtown_thresh_925_primal.ply &