 #!/bin/bash
#*******************************************************************************************************
#Created on March 25, 2013
#
#author:Isabel Restrepo
#
#A script that encapsulates all steps needed to run bag of features evaluation following similar techniques
# used for bmvc12 but adding a "no object" category
#*******************************************************************************************************

#*******************************************************************************************************
# SET UP ENVIROMENT
#*******************************************************************************************************
CONFIGURATION=Release;
export PYTHONPATH=/Projects/vpcl/bin_make/$CONFIGURATION/lib:/Projects/vpcl/vpcl/pyscripts:/Projects/voxels-at-lems-git/bmvc12/utils:$PYTHONPATH

#*******************************************************************************************************
# DEFINE STEPS TO BE RUN
#*******************************************************************************************************
compute_fpfh=false;
compute_shot=false;
pickle=false;
stack_features=false;
quantize=false;
classify=false;
collect_validation_results=false;

# compute_fpfh=true;
# compute_shot=true;
# pickle=true;
# stack_features=true;
# quantize=true;
classify=true;
# collect_validation_results=true;


#*******************************************************************************************************
#Compute features
#*******************************************************************************************************
percentile=90;
radius=30;

if $compute_fpfh; then
  njobs=8;
  python ./descriptors/compute_omp_descriptors_no_object.py -r $radius -p $percentile -d "FPFH" -j $njobs
fi

if $compute_shot; then
  njobs=8;
  python ./descriptors/compute_omp_descriptors_no_object.py -r $radius -p $percentile -d "SHOT" -j $njobs
fi


#*******************************************************************************************************
#Feature Post Processing
#*******************************************************************************************************
if $pickle; then
  FEATURE="FPFH"
  njobs=2;
  python ./utils/pickle_descritor_no_object.py -r $radius -p $percentile -d $FEATURE -j $njobs
  FEATURE="SHOT"
  njobs=2;
  python ./utils/pickle_descritor_no_object.py -r $radius -p $percentile -d $FEATURE -j $njobs
fi

#I actually don't need this step because we are not relearning the codebook
# if $stack_features; then
#   for trial in 0 1 2 3 4; do
#        python ./utils/stack_train_features_no_object.py -r $radius -p 90 -t $trial -d "FPFH"
#        python ./utils/stack_train_features_no_object.py -r $radius -p 90 -t $trial -d "SHOT"
#   done
# fi

# #*******************************************************************************************************
# # Bag of Features
# #*******************************************************************************************************
K=500
if $quantize; then
    for trial in 0 1 2 3 4; do
       python ./bof/quantize_objects_no_object.py -r $radius -p 90 -t $trial -d "FPFH" -k $K &
       python ./bof/quantize_objects_no_object.py -r $radius -p 90 -t $trial -d "SHOT" -k $K
       wait
    done
fi

if $classify; then
  for trial in 0 1 2 3 4; do
     python ./bof/classify_no_object.py -r $radius -p 90 -t $trial -d "FPFH" -k $K &
     python ./bof/classify_no_object.py -r $radius -p 90 -t $trial -d "SHOT" -k $K
     wait
  done
fi


if $collect_validation_results; then
   python ./bof/collect_validation_results_no_object.py -r $radius -p 90 -d "FPFH" -k $K
   python ./bof/collect_validation_results_no_object.py -r $radius -p 90 -d "SHOT" -k $K
fi


# #if $collect_validation_results; then
# #  for radius in 10 20 30 45; do
# #    for K in 20 50 100 200 500; do
# #         python ./bof/read_min_max_accuracy.py -r $radius -p 90 -d $FEATURE -k $K -c "svm_gamma_10.0_C100.00"
# #    done
# #  done
# #fi

# if $collect_validation_results; then
#   python ./bof/read_min_max_accuracy.py -r 30 -p 90 -d $FEATURE -k 500 -c "1nn"
#   python ./bof/read_min_max_accuracy.py -r 30 -p 90 -d $FEATURE -k 500 -c "bayes"
#   #python ./bof/read_min_max_accuracy.py -r 30 -p 90 -d $FEATURE -k 500 -c "svm_gamma_10.0_C100.00"
# fi


