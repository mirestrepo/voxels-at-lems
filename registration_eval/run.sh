#!/bin/bash

n_iter_ia=100;
n_iter_icp=100;

for t in 0 1 2 3 4; do
  ./reg3d_main.py --trial $t --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia &
done
wait

for t in 0 1 2 3 4; do
  ./reg3d_main.py --trial $t --reg_icp true --descriptor "FPFH" --n_iter $n_iter_icp &
done
wait
for t in 0 1 2 3 4; do
  ./reg3d_main.py --trial $t --reg_icp true --descriptor "FPFH" --rej_normals true --n_iter $n_iter_icp &
done
wait

for t in 0 1 2 3 4; do
  ./reg3d_main.py --trial $t --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia &
done
wait

for t in 0 1 2 3 4; do
  ./reg3d_main.py --trial $t --reg_icp true --descriptor "SHOT" --n_iter $n_iter_icp &
done
wait
for t in 0 1 2 3 4; do
  ./reg3d_main.py --trial $t --reg_icp true --descriptor "SHOT" --rej_normals true --n_iter $n_iter_icp &
done
wait