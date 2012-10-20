#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
A script that encapsulates 3d-registration algorithms in the PVM
September 12, 2012
"""

import os, sys, argparse
import reg3d

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir",       action="store",   type=str,
        dest="root_dir",
        default="/Users/isa/Experiments/reg3d_eval/downtown_dan",
        help="Path to root directory")
    parser.add_argument("--t_basename",     action="store",   type=str,
        dest="t_basename",       default="trial",
        help="Basename of trial directory e.g trial , trial_pert_005")
    parser.add_argument("--trial",          action="store",   type=int,
        dest="trial",       default=0,
        help="Trial number")
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
    trial_root_dir = args.root_dir + "/" + args.t_basename + "_" + str(trial_number)
    descriptor_type = args.descriptor
    radius = 30
    percentile = 99
    verbose = args.verbose

    if args.reg_ia:
        print "Running IA"
        reg3d.register_ia(gt_root_dir, trial_root_dir, descriptor_type,
            radius, percentile, args.n_iter, verbose)

    if args.reg_icp:
        print "Running ICP"
        reg3d.register_icp(gt_root_dir, trial_root_dir, descriptor_type,
            radius, percentile, args.n_iter, args.rej_normals,
            verbose, True)

    if args.vis_ia:
        print "Visualizing  IA"
        reg3d.visualize_reg_ia(gt_root_dir, trial_root_dir,
            descriptor_type, radius,
            percentile, args.n_iter, args.geo)

    if args.vis_icp:
        print "Visualizing  ICP"
        reg3d.visualize_reg_icp(gt_root_dir, trial_root_dir,
            descriptor_type, radius,
            percentile, args.n_iter, args.rej_normals, args.geo,
            trial_number)

    if args.plot_Terror:
        print "Saving Terror plots"
        import compute_transformation_error as TE
        TE.main()
        import plot_ICP_iterations
        plot_ICP_iterations.main()
        import compute_trans_geo_accuracy as TE_GEO
        TE_GEO.main()

