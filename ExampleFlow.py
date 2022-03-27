import FlowModule as F

S1 = F.Segment(h = 0,\
                  q = F.CumecConvert(5).gpm(),\
                  d = F.pipe_size['1_10'],\
                  nu = .001,\
                  epsilon = F.surface_roughness['Drawn tubing'],\
                  lg = 3,\
                  n_elb45 = 2,\
                  n_elb90 = 2)



print('Velocity:', round(S1.v(),2), '[m/s]')
print('Reynolds Number:', round(S1.re(),2),'[-]')
print('Friction Factor:', round(S1.friction_factor(),2),'[-]\n')
print('Minor Losses:', round(S1.l_m(),2), '[m]')
print('Friction Losses:', round(S1.l_f(),2), '[m]')
print('Total Losses:',round(S1.l_t(),2), '[m]')


