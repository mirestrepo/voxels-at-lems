#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
A script that encapsulates 3d-registration algorithms in the PVM
September 12, 2012
"""

import os, sys, argparse
sys.path.append(os.pardir)
import reg3d

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir",       action="store",   type=str,
        dest="root_dir",
        default="",
        help="Path to root directory - where all sites are")
    parser.add_argument("--site",       action="store",   type=str,
        dest="site",
        default="",
        help="Name of the scene e.g downtown")
    parser.add_argument("--src_str",       action="store",   type=str,
        dest="src_str",
        default="",
        help="Identifying string for source site e.g 2011")
    parser.add_argument("--tgt_str",       action="store",   type=str,
        dest="tgt_str",
        default="",
        help="Identifying string for target site e.g 2011")
    parser.add_argument("--reg_ia",        action="store_true",
       dest="reg_ia",
       help="Run initial alignment")
    parser.add_argument("--reg_icp",       action="store_true",
       dest="reg_icp",
       help="Run ICP")
    parser.add_argument("--vis_ia",         action="store_true",
       dest="vis_ia",
       help="Visualize initial alignment")
    parser.add_argument("--vis_icp",        action="store_true",
       dest="vis_icp",
       help="Visualize ICP")
    parser.add_argument("--plot_Terror",    action="store_true",
       dest="plot_Terror",
       help="Plot Transformation errors")
    parser.add_argument("--descriptor",     action="store",   type=str,
       dest="descriptor",  default="FPFH",
       help="Trial number")
    parser.add_argument("--basename_in",     action="store",   type=str,
       dest="basename_in",  default="gauss_233_normals_pvn",
       help="string identifying .ply eg gauss_233_normals_pvn")
    parser.add_argument("--cropped",    action="store_true",
       dest="cropped",
       help="Are we using a cropped version?")
    parser.add_argument("--rej_normals",    action="store_true",
       dest="rej_normals",
       help="Reject normals?")
    parser.add_argument("--compute_scale",    action="store_true",
       dest="compute_scale",
       help="compute scale? or read it from gt_transfomation")
    parser.add_argument("--bound_scale",    action="store_true",
       dest="bound_scale",
       help="set upper and lower bound for scale")
    parser.add_argument("--bound_percentile",     action="store",   type=int,
        dest="bound_percentile", default=1,
        help="bound_percentile (on scale) to use")
    parser.add_argument("--verbose",        action="store_true",
       dest="verbose",
       help="Print or redirect to log file")
    parser.add_argument("--n_iter",         action="store",   type=int,
        dest="n_iter",      default=200,
        help="Number of iterations")
    parser.add_argument("--nsamples",         action="store",   type=int,
        dest="nsamples",      default=3,
        help="Number of iterations")
    parser.add_argument("--sample_distance",  action="store",   type=int,
        dest="sample_distance",      default=1,
        help="Min. RANSAC sample distance = this*radius*resolution")
    parser.add_argument("--geo",            action="store_true",
       dest="geo",
       help="Use reoregistered clouds?")
    parser.add_argument("--percentile",     action="store",   type=int,
        dest="percentile", default=99,
        help="percentile to use")

    args = parser.parse_args()

    print args

    gt_root_dir = args.root_dir + "/" + args.site + "_" + args.tgt_str + "/original"
    trial_root_dir = args.root_dir + "/" + args.site + "_" + args.src_str + "/original"
    descriptor_type = args.descriptor
    gt_fname = args.src_str + "-" + args.tgt_str + "_Hs.txt"
    radius = 30
    percentile = args.percentile
    verbose = args.verbose

    descriptor_string = "descriptors"
    aux_output_string = args.src_str + "-" + args.src_str
    # aux_output_string = args.src_str + "-" + args.src_str #+ "_" +  str(args.nsamples) + "_" + str(args.sample_distance)
    #Note: when I run the experiment the output files were labeled by mistake src-src
    # this is the correct name
    if args.compute_scale:
      aux_output_string = args.src_str + "-" + args.tgt_str + "_" +  str(args.nsamples) + "_" + str(args.sample_distance)

    if args.cropped:
      descriptor_string = descriptor_string + "_cropped"
      aux_output_string = aux_output_string + "-cropped"

      print descriptor_string, aux_output_string

    if args.compute_scale:
      aux_output_string = aux_output_string + "_scale"
      if args.bound_scale:
        aux_output_string = aux_output_string + "_bound_" + str(args.bound_percentile)

    print descriptor_string, aux_output_string


    if args.reg_ia:
        print "Running IA"
        ransac_scale, avg_scale = reg3d.register_ia(gt_root_dir       = gt_root_dir,
                                                    trial_root_dir    = trial_root_dir,
                                                    descriptor_type   = descriptor_type,
                                                    radius            = radius,
                                                    percentile        = percentile,
                                                    nr_iterations     = args.n_iter,
                                                    nsamples          = args.nsamples,
                                                    sample_distance   = args.sample_distance,
                                                    compute_scale     = args.compute_scale,
                                                    bound_scale       = args.bound_scale,
                                                    bound_percentile  = args.bound_percentile,
                                                    verbose           = verbose,
                                                    aux_output_string = aux_output_string,
                                                    descriptor_string = descriptor_string,
                                                    basename_in       = args.basename_in,
                                                    gt_fname          = gt_fname)


        print "ransac_scale: ", ransac_scale
        print "avg_scale: ", avg_scale

        # if args.compute_scale:

        #     reg3d.register_ia(gt_root_dir       = gt_root_dir,
        #                       trial_root_dir    = trial_root_dir,
        #                       descriptor_type   = descriptor_type,
        #                       radius            = radius,
        #                       percentile        = percentile,
        #                       nr_iterations     = args.n_iter,
        #                       nsamples          = 3,
        #                       sample_distance   = 1,
        #                       compute_scale     = False,
        #                       verbose           = verbose,
        #                       aux_output_string = aux_output_string + "_sac",
        #                       descriptor_string = descriptor_string,
        #                       basename_in       = args.basename_in,
        #                       gt_fname          = gt_fname,
        #                       scale             = ransac_scale)



    if args.reg_icp:
        print "Running ICP"
        reg3d.register_icp(gt_root_dir       = gt_root_dir,
                              trial_root_dir    = trial_root_dir,
                              descriptor_type   = descriptor_type,
                              radius            = radius,
                              percentile        = percentile,
                              nr_iterations     = args.n_iter,
                              compute_scale     = args.compute_scale,
                              use_max_nr_iter   = True,
                              verbose           = verbose,
                              aux_output_string = aux_output_string,
                              descriptor_string = descriptor_string,
                              basename_in       = args.basename_in)

        # if args.compute_scale:
        #   reg3d.register_icp(gt_root_dir       = gt_root_dir,
        #                         trial_root_dir    = trial_root_dir,
        #                         descriptor_type   = descriptor_type,
        #                         radius            = radius,
        #                         percentile        = percentile,
        #                         nr_iterations     = args.n_iter,
        #                         compute_scale     = args.compute_scale,
        #                         use_max_nr_iter   = True,
        #                         verbose           = verbose,
        #                         aux_output_string = aux_output_string + "_sac",
        #                         descriptor_string = descriptor_string,
        #                         basename_in       = args.basename_in)

    if args.vis_ia:

        print "Visualizing  IA"
        reg3d.visualize_reg_ia(gt_root_dir, trial_root_dir,
            descriptor_type, radius,
            percentile, args.n_iter, args.geo, aux_output_string, args.basename_in)

        # reg3d.visualize_reg_ia(gt_root_dir, trial_root_dir,
        #     descriptor_type, radius,
        #     percentile, args.n_iter, args.geo, aux_output_string + "_sac", args.basename_in)

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

