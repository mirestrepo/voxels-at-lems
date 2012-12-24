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
        default="",
        help="Path to root directory")
    parser.add_argument("--flight",          action="store",   type=int,
        dest="flight",       default=4,
        help="Flight number e.g 2,4,5")
    parser.add_argument("--gt_flight",          action="store",   type=int,
        dest="gt_flight",       default=2,
        help="Ground truth flight, i.e flight is registered to gt_flight")
    parser.add_argument("--site",          action="store",   type=int,
        dest="site",       default=1,
        help="Site number")
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
    parser.add_argument("--basename_in",     action="store",   type=str,
       dest="basename_in",  default="gauss_233_normals_pvn",
       help="string identifying .ply eg gauss_233_normals_pvn")
    parser.add_argument("--cropped",    action="store",   type=bool,
       dest="cropped", default=False,
       help="Are we using a cropped version?")
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
    parser.add_argument("--percentile",     action="store",   type=int,
        dest="percentile", default=99,
        help="percentile to use")

    args = parser.parse_args()

    print args

    gt_root_dir = args.root_dir + "/flight" + str(args.gt_flight) + "_sites/site_" + str(args.site)
    trial_root_dir = args.root_dir + "/flight" + str(args.flight) + "_sites/site_" + str(args.site)
    descriptor_type = args.descriptor
    gt_fname = "f" + str(args.flight)+ "-f" +str(args.gt_flight) + "_Hs.txt"
    radius = 30
    percentile = args.percentile
    verbose = args.verbose

    if args.cropped:
      descriptor_string = "descriptors_cropped"
      aux_output_string = "f" + str(args.flight)+ "-f" +str(args.gt_flight) + "-cropped"

    else:
      descriptor_string = "descriptors"
      aux_output_string = "f" + str(args.flight)+ "-f" +str(args.gt_flight)


    if args.reg_ia:
        print "Running IA"
        reg3d.register_ia(gt_root_dir, trial_root_dir, descriptor_type,
            radius, percentile, args.n_iter, verbose, aux_output_string,
            descriptor_string, args.basename_in, gt_fname)

    if args.reg_icp:
        print "Running ICP"
        reg3d.register_icp(gt_root_dir, trial_root_dir, descriptor_type,
            radius, percentile, args.n_iter, args.rej_normals,
            verbose, True, aux_output_string, args.basename_in)

    if args.vis_ia:
        print "Visualizing  IA"
        reg3d.visualize_reg_ia(gt_root_dir, trial_root_dir,
            descriptor_type, radius,
            percentile, args.n_iter, args.geo, aux_output_string, args.basename_in)

    if args.vis_icp:
        print "Visualizing  ICP"
        reg3d.visualize_reg_icp(gt_root_dir, trial_root_dir,
            descriptor_type, radius,
            percentile, args.n_iter, args.rej_normals, args.geo,
            aux_output_string, args.basename_in)

    if args.plot_Terror:
        print "Saving Terror plots"
        import compute_transformation_error as TE
        TE.main()
        import plot_ICP_iterations
        plot_ICP_iterations.main()
        import compute_trans_geo_accuracy as TE_GEO
        TE_GEO.main()

