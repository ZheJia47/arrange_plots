from PIL import Image
import numpy as np
import arrange_plots

# Arrange_plots ########################################################################
def Arrange_plots(plot_list, h_num = 1, v_num = 1, size_times = 1, plot_name = 'plot', white_bkg=0, option='sp'):
    # this func arrange same number of plots for each row     
    plot_list = [ Image.open(plot_list[i]) for i in range(len(plot_list))]
    x_size_list = [ plot_list[i].size[0] for i in range(len(plot_list)) ]
    y_size_list = [ plot_list[i].size[1] for i in range(len(plot_list)) ]    
    
    y_len = int( round( np.mean( y_size_list ),0 ) ) # each row y length    
    # scale all plots to same y length   
    for i in range(len(plot_list)):
        plot_list[i] = plot_list[i].resize( ((round( x_size_list[i]*y_len/y_size_list[i],0) ), y_len), Image.ANTIALIAS )
            
    # x_len = the row which has maximum x length ##############    
    x_len = [] 
    for i in range(v_num):
        x_len += [ sum( x_size_list[i*h_num+j] for j in range(h_num) ) ]
    x_len = max(x_len)

    # new_plot ################################################    
    new_plot = Image.new( 'RGB', (x_len, v_num*y_len ) )
    loc_list = []
    for i in range(v_num):
        for j in range(h_num):
            loc_list += [ ( int(round((j/h_num)*x_len,0)) , i*y_len) ]
    # paste ################        
    for i in range(v_num):    
        for j in range(h_num):
            new_plot.paste( plot_list[i*h_num+j], loc_list[i*h_num+j] )
    # resize ############################################     
    new_plot = new_plot.resize( (int(round(size_times*x_len)), int(round(size_times*v_num*y_len))), Image.ANTIALIAS )
    # option ############################################
    if 'p' in option:    
        new_plot.show()
    if 's' in option:    
        new_plot.save('%s.png' % plot_name)

# Arrange_plots_v2 #####################################################################
# white_bkg_plot = Image.open('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/arrange_plots/white_bkg.png')
white_bkg_plot = Image.open((arrange_plots.__path__[0])+'/white_bkg.png')

def Arrange_plots_v2(plot_list, h_num_list = [1], bkg_plot = white_bkg_plot,size_times = 1, plot_name = 'plot', option='sp'):   
    # this func let you decide how many plots in which row you like
    # plot arrangement:
    # first row has h_num_list[0] plots
    # second row has h_num_list[1] plots, and so on...
    plot_list = [ Image.open(plot_list[i]) for i in range(len(plot_list))]

    x_size_list = [ plot_list[i].size[0] for i in range(len(plot_list)) ]
    y_size_list = [ plot_list[i].size[1] for i in range(len(plot_list)) ]    
    
    y_len = int( round( np.mean( y_size_list ),0 ) ) # each row y length    
    # scale all plots to same y length   
    for i in range(len(plot_list)):
        plot_list[i] = plot_list[i].resize( ((round( x_size_list[i]*y_len/y_size_list[i],0) ), y_len), Image.ANTIALIAS )
            
    # x_len = the row which has maximum x length ##############    
    v_num = len(h_num_list)
    #h_num = sum(h_num_list)
    x_len = [] 

    for i in range(v_num):
        x_len += [ sum( x_size_list[i*h_num_list[i-1]+j] for j in range(h_num_list[i]) ) ]
       
    x_len = max(x_len)
    # new_plot ################################################    
    new_plot = Image.new( 'RGB', (x_len, v_num*y_len ) )
    loc_list = []    
    for i in range(v_num):   
        # x1 is 邊寬
        x1 = (x_len - sum( x_size_list[i*h_num_list[i-1]+j] for j in range(h_num_list[i])))/2  

        for j in range(h_num_list[i]):        
            x2 = sum( x_size_list[i*h_num_list[i-1]+j1] for j1 in range(j) )         
            loc_list += [ ( int(round(x1+x2,0)) , i*y_len) ]            
    # paste ################      
    bkg_plot = bkg_plot.resize( (int(round(size_times*x_len)), int(round(size_times*v_num*y_len))), Image.ANTIALIAS )
    new_plot.paste(bkg_plot, (0,0))       
    for i in range(sum(h_num_list)):
        new_plot.paste( plot_list[i], loc_list[i])
    # resize ############################################     
    new_plot = new_plot.resize( (int(round(size_times*x_len)), int(round(size_times*v_num*y_len))), Image.ANTIALIAS )
    # option ############################################
    if 'p' in option:    
        new_plot.show()    
    if 's' in option:    
        new_plot.save('%s.png' % plot_name)
        
if __name__ == "__main__":
    main()
        

