#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
A script that encapsulates all steps to evaluate
3d-registration algorithms in the PVM under camera perturbation errors
September 12, 2012
"""
import os, sys, argparse

#set up enviroment
CONFIGURATION= "Release";

sys.path.append("/Projects/vxl/bin/" +CONFIGURATION +"/lib");
sys.path.append("/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts");

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir",       action="store",   type=str,
        dest="root_dir",
        default="/Users/isa/Experiments/reg3d_eval/downtown_dan",
        help="Path to root directory")
    parser.add_argument("--trial",          action="store",   type=int,
        dest="trial",       default=0,
        help="Trial number")
    parser.add_argument("--si",          action="store",   type=int,
        dest="si",       default=0,
        help="Sigma index, where sigma = [0.05, 0.1, 0.15] ")
    parser.add_argument("--perturb",         action="store",   type=bool,
       dest="perturb",      default=False,
       help="Run initial alignment")
    parser.add_argument("--reg_ia",         action="store",   type=bool,
       dest="reg_ia",      default=False,
       help="Run initial alignment")
    parser.add_argument("--reg_icp",        action="store",   type=bool,
       dest="reg_icp",     default=False,
       help="Run ICP")
    parser.add_argument("--vis_ia",         action="store",   type=bool,
       dest="vis_ia",      default=False,
       help="Visualize initial alignment")
    parser.add_argument("--vis_icp",        action="store",   type=bool,
       dest="vis_icp",     default=False,
       help="Visualize ICP")
    parser.add_argument("--plot_Terror",    action="store",   type=bool,
       dest="plot_Terror",     default=False,
       help="Plot Transformation errors")
    parser.add_argument("--descriptor",     action="store",   type=str,
       dest="descriptor",  default="FPFH",
       help="Trial number")
    parser.add_argument("--rej_normals",    action="store",   type=bool,
       dest="rej_normals", default=False,
       help="Reject normals?")
    parser.add_argument("--verbose",        action="store",   type=bool,
       dest="verbose",     default=False,
       help="Print or redirect to log file")
    parser.add_argument("--n_iter",         action="store",   type=int,
        dest="n_iter",      default=200,
        help="Number of iterations")
    parser.add_argument("--geo",            action="store",   type=bool,
       dest="geo",         default=False,
       help="Use reoregistered clouds?")

    args = parser.parse_args()

    print args

    gt_root_dir = args.root_dir + "/original"
    trial_number = args.trial
    sigma = [0.05, 0.1, 0.15]
    sigma_str = ["005", "01", "015"]
    trial_root_dir = args.root_dir + "/pert_" + sigma_str[args.si] + "_" + str(args.trial)
    descriptor_type = args.descriptor
    radius = 30
    percentile = 99
    verbose = args.verbose

    if args.perturb:
        import perturb_cameras
        from bbas_adaptor import *

        rng = initialize_rng(); #init random number generator
        print "Peturbing cameras"
        for si in range(0, len(sigma)):
            for ti in range(0, 10):
                root_in = gt_root_dir
                root_out = args.root_dir + "/pert_" + sigma_str[si] + "_" + str(ti)
                perturb_cameras.perturb_cams(root_in, root_out, sigma[si], rng)

    if args.reg_ia:
        import reg3d
        print "Running IA"
        reg3d.register_ia(gt_root_dir, trial_root_dir, descriptor_type,
            radius, percentile, args.n_iter, verbose)

    if args.reg_icp:
        import reg3d
        print "Running ICP"
        reg3d.register_icp(gt_root_dir, trial_root_dir, descriptor_type,
            radius, percentile, args.n_iter, args.rej_normals,
            verbose, True)

    if args.vis_ia:
        import reg3d
        print "Visualizing  IA"
        reg3d.visualize_reg_ia(gt_root_dir, trial_root_dir,
            descriptor_type, radius,
            percentile, args.n_iter, args.geo)

    if args.vis_icp:
        import reg3d
        print "Visualizing  ICP"
        reg3d.visualize_reg_icp(gt_root_dir, trial_root_dir,
            descriptor_type, radius,
            percentile, args.n_iter, args.rej_normals, args.geo,
            trial_number)

