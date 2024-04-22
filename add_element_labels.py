#!/usr/bin/python

############################################################################### 
#                                                                          * F# 
#               DIST: A DIslocation-Simulation Toolkit                     2 R# 
# GNU License - Author: Zongrui Pei                       2015-06-10       0 A# 
# Version 1.0                                                              1 N# 
#                                                                          5 K# 
# Syntax:                                                                  0 F# 
# Please find the syntx in the howto.dat of the examples folder            6 U# 
# and the CPC paper: Zongrui Pei, DIST: A DIslocation-Simulation Toolkit,  1 R# 
# Computer Physics Communications 233(2018)44-50.                          0 T# 
#                                                                          * *# 
###############################################################################
from __future__ import print_function
import numpy as np
from numpy import pi,arctan
import sys
import random

class add_element_labels():
  """add element labels to model structure file POSCAR"""
  def __init__(self,filename):
    self.filename=filename
    self.latt_para=1.0
    self.w_coord=-1
    self.sys_name="" 
    self.coord_type="" #"Direct" #"Cartesian"
    self.coord=np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]) 
    self.atoms_pos=[] 
    self.N=[10,5] #default, will read from structural file
    self.n_unit=[]
    self.mag_coord=np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
    self.randStruct=[] 
    self.labels=[]
  def read_data(self):
    with open(self.filename,'r') as in_file:
      count=1
      for line in in_file:
        ll=line.split()
        if count==1: 
          if len(ll)>1:
            self.sys_name=ll[0]
            for i in range(1,len(ll)):
              self.labels.append(ll[i])
          else: 
            print("Error from the first line of input file!")
            return None
            break
        if count==2: self.latt_para=float(ll[0])
        if count>2 and count<6:
          self.coord[count-3]=np.array([float(ll[0]),float(ll[1]),float(ll[2])])
        if count==6:
          for i in ll:
            self.n_unit.append(int(i))
        if ('Cartesian' in line) or ('cartesian' in line):
           self.coord_type='Cartesian'
           break
        if ('Direct' in line) or ('direct' in line):
           self.coord_type='Direct'
           break
        count +=1
      for line in in_file:
        if line != '\n':
          ll = line.split()
          ll[0],ll[1],ll[2]=float(ll[0]),float(ll[1]),float(ll[2])
          self.atoms_pos.append(ll[0:3])
  def print_file(self):
    self.read_data()
    print(self.sys_name)
    print(self.latt_para)
    for i in range(0,3):
      print(format(self.coord[i,0],"03f"),"	",format(self.coord[i,1],"03f"),"	",\
            format(self.coord[i,2],"03f"))
    str_atom_num=""
    for i in self.n_unit:
      str_atom_num += str(i)+" "
    print(str_atom_num)
    print(self.coord_type)
    idx,begin_n=[],0
    for i in range(0,len(self.n_unit)):
      begin_n += self.n_unit[i]
      idx.append(begin_n)
    for j in range(0,len(self.atoms_pos)):
      i=self.atoms_pos[j]
      if j<idx[0]:
        print(format(i[0],"03f"),"   ",format(i[1], "03f")," ",format(i[2],"03f"),"	",str(self.labels[0]))
      for k in range(1,len(idx)):
        if j>idx[k-1]-1 and j<idx[k]:
          print(format(i[0],"03f"),"   ",format(i[1], "03f")," ",format(i[2],"03f"),"      ",str(self.labels[k]))

if __name__=="__main__":
  dist1=add_element_labels(sys.argv[1])#"unit_cell")
  dist1.print_file()
