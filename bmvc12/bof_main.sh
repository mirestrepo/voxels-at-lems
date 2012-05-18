 #!/bin/bash
#*******************************************************************************************************
#Created on May 3, 2012
#
#author:Isabel Restrepo
#
#A script that encapsulates all steps needed to run bag of features evaluation (bmvc12)
#*******************************************************************************************************

#*******************************************************************************************************
# SET UP ENVIROMENT
#*******************************************************************************************************
CONFIGURATION=Release;
export PYTHONPATH=/Projects/lemsvxl/bin/$CONFIGURATION/lib:/Projects/lemsvxl/src/contrib/dbrec_lib/dbrec3d/pyscripts:/Projects/voxels-at-lems-git/bmvc12/utils:$PYTHONPATH

#*******************************************************************************************************
# DEFINE STEPS TO BE RUN
#*******************************************************************************************************
compute_fpfh=false;
compute_shot=false;
compute_spin=false;
compute_shape_c=false;
pickle=false;
stack_features=false;
learn_codebook=false
quantize=false;
classify=false;
collect_validation_results=false;

#compute_fpfh=true;
#compute_shot=true;
#compute_spin=true;
#compute_shape_c=true;
#pickle=true;
#stack_features=true;
#learn_codebook=true
#quantize=true;
#classify=true;
collect_validation_results=true;


#*******************************************************************************************************
#Compute features
#*******************************************************************************************************
percentile=90;

if $compute_fpfh; then
  njobs=8;
  for radius in 10 15 20 30 45; do
     ./descriptors/compute_omp_descriptors.py -r $radius -p $percentile -d "FPFH" -j $njobs
  done
fi

if $compute_shot; then
  njobs=8;
  for radius in 10 15 20 30 45; do
     ./descriptors/compute_omp_descriptors.py -r $radius -p $percentile -d "SHOT" -j $njobs
  done
fi

if $compute_spin; then
  njobs=8;
  for radius in 10 15 20 30 45; do
      for site in 1 2 3 6 7 8 10 11 12 16 18 21 22 23 25 26 27; do
          python ./descriptors/compute_spin_images.py -s $site -r $radius -p $percentile -j $njobs
      done
  done
fi

if $compute_shape_c; then
  for radius in 10 15 20 30 45; do
      for site in 1 2 3 6 7 8 10 11 12 16 18 21 22 23 25 26 27; do
          python ./descriptors/compute_shape_context.py -s $site -r $radius -p $percentile
      done
  done
fi

#*******************************************************************************************************
#Feature Post Processing
#*******************************************************************************************************
if $pickle; then 
for radius in 20 30 45; do
    FEATURE="ShapeContext"
    njobs=2;
    python ./utils/pickle_descritor.py -r $radius -p 90 -d $FEATURE -j $njobs
done
fi

if $stack_features; then
  FEATURE="SpinImage"
  for trial in 1 2; do
    for radius in 10 20 30 45; do
       python ./utils/stack_train_features.py -r $radius -p 90 -t $trial -d $FEATURE
    done
  done
fi

#*******************************************************************************************************
# Bag of Features
#*******************************************************************************************************
FEATURE="SpinImage"
#FEATURE="SHOT"
#FEATURE="FPFH"
#FEATURE="FPFH"
#FEATURE="ShapeContext"
if $learn_codebook; then
  for radius in 10 20 30 45; do
    for K in 20 50 100 200 500; do
      for trial in 1 2; do
         python ./bof/learn_codebook.py -r $radius -p 90 -t $trial -d $FEATURE -k $K 
      done
    done
  done
fi

if $quantize; then
  for radius in 10 20 30 45; do
    for K in 20 50 100 200 500; do
      for trial in 1 2; do
         python ./bof/quantize_objects.py -r $radius -p 90 -t $trial -d $FEATURE -k $K &
       done
      wait
    done
  done
fi

if $classify; then
  for radius in 10 20 30 45; do
    for K in 20 50 100 200 500; do
      for trial in 1 2; do
         python ./bof/classify.py -r $radius -p 90 -t $trial -d $FEATURE -k $K &
       done
      wait
    done
  done
fi


if $collect_validation_results; then
  for radius in 10 20 30 45; do
    for K in 20 50 100 200 500; do
         python ./bof/collect_validation_results.py -r $radius -p 90 -d $FEATURE -k $K &
         python ./bof/read_min_max_accuracy.py -r $radius -p 90 -d $FEATURE -k $K -c "svm_gamma_10.0_C100.00" & 
    done
    wait
  done
fi


#if $collect_validation_results; then
#  for radius in 10 20 30 45; do
#    for K in 20 50 100 200 500; do
#         python ./bof/read_min_max_accuracy.py -r $radius -p 90 -d $FEATURE -k $K -c "svm_gamma_10.0_C100.00"  
#    done
#  done
#fi

if $collect_validation_results; then
  python ./bof/read_min_max_accuracy.py -r 30 -p 90 -d $FEATURE -k 500 -c "1nn"       
  python ./bof/read_min_max_accuracy.py -r 30 -p 90 -d $FEATURE -k 500 -c "bayes"       
  #python ./bof/read_min_max_accuracy.py -r 30 -p 90 -d $FEATURE -k 500 -c "svm_gamma_10.0_C100.00"       
fi


