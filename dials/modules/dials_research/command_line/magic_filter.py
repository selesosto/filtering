#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:58:22 2018

@author: rze73714
"""
# __future__ import division, print_function

from __future__ import absolute_import, division
from dials.array_family import flex
import cPickle as pickle
import numpy 

# purely empirical filter based on a certain percentage of low resolution reflections and a certain percentage of large spots
def magic_filter(refl_in, refl_out, filtered):
  big_spot_size=10
  low_resolution=4
  f=open(filtered, "w")
  reflections = pickle.load(open(refl_in))
  print len(reflections)
  z = (reflections['xyzobs.px.value'].parts()[2])
  unique_z = list(sorted((set(z))))
  sel=flex.bool()
  im_to_filter=[]
  print unique_z
  for uz in unique_z:
        r_image = reflections.select(z == uz)  
        huge_spots = r_image.select(r_image['n_signal'] > big_spot_size)
        low_resol = r_image.select(r_image['d'] > low_resolution)
        if len(r_image)>0 and (len(huge_spots)!=0):
             a=len(huge_spots)/len(r_image)
             b=len(low_resol)/len(r_image)
             # filters out images which have more than 8.5% of reflections with more than 10 pixels,
             if a > 0.085:
                 f.write("image "+str(uz)+" filtered because the number of spots with more than 10 pixels was "+str(a)+". \n")
                 im_to_filter.append(uz)
             # filters images whose reflections have less than 5% low resolution
             elif b < 0.05:
                 f.write("image "+str(uz)+" filtered because the percentage of low resolution was "+str(b)+". \n")
                 im_to_filter.append(uz)
  for i in xrange(0, len(reflections)):
      if reflections[i]['xyzobs.px.value'][2] in im_to_filter:
          sel.append(False)
      else:
          sel.append(True)
  print len(sel)                                 
  f.close()
  filtered=reflections.select(sel)    # what I want to get back is a stronger.pickle file which is filtered for the images I don't want
  filtered.as_pickle(refl_out)
 

#return reflections.select(reflections['xyzobs.px.value'].parts()[2] not in to_filter)



#return to_filter