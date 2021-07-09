import numpy as np
import sys, getopt

command_args = sys.argv[1:]
options = 'p:i:'
longoptions = ['pulsars=','inputfile=']

try:
    opts, args = getopt.getopt(command_args, options, longoptions)
except getopt.GetoptError:
    print('ERROR: Something went wrong!!')
    sys.exit(2)

pulsar_input = False

for opt, arg in opts:
    if opt in ['-p', '--pulsars']:
        print("Setting pulsar file = ", arg)
        pulsar_input = True
        pulsar_file = arg
        
if not pulsar_input:
	print('ERROR: Please provide the pulsar input file!!')
	sys.exit(2)

input_file = False

for opt, arg in opts:
    if opt in ['-i', '--inputfile']:
        print("Setting input file = ", arg)
        input_file = True
        inp_file = arg


def flux_cal(name, t_start):
    f.write("\n******** Flux Calibration with {0} ********   {1}\n\n".format(name, t_start))
    f.write("/cmd3 \"gts \'%s\'\"" % name)
    f.write(
"""
/cmd3 "sndsacsrc(1,12h)"
/cmd3 "sndsacsrc(1,12h)"
/cmd3 "stabct"
/cmd3 "/(gotosrc 10m 3)"
time 5s

"""         
            )

    f.write("gts \'%s\'" % name)
    f.write(
"""
sndsacsrc(1,12h)
sndsacsrc(1,12h)
stabct
/(gotosrc 10m 4)
time 5s

"""         
            )
    if "OFF" not in name:
        f.write("/cmd3 \"strtndas\"\n")
        f.write("/cmd3 \"/phase_gwb.pl -r %s -s 3 -t 40 -p %sB\"\n" %(ref_ant_subarr3, project_name))
        f.write("time 5s\n")
        f.write("strtndas\n")
        f.write("/phase_gwb.pl -r %s -s 4 -t 40 -p %sA" %(ref_ant_subarr4, project_name))



        f.write(
"""
time 5s

/cmd3 "stpndas"
time 5s
stpndas
time 5s

"""
                )

    f.write(
"""
/cmd3 "strtndas"
time 5s
strtndas
time 5s


"""
            )

    if cdp_beam == "bm1":
        f.write("/gwbpsr.start %s %s 500 1460 1460 1460\n" %(padisk, name))
    elif cdp_beam == "bm2":
        f.write("/gwbpsr.start %s %s 1460 500 1460 1460\n" %(padisk, name))
    f.write("time 5s\n")
    f.write("/runsubband-cd-%s.pl 200.0 300.0 %d 2.5 %d -1\n" %(cdp_beam, nchan_runsubband, nchan_obs))
    f.write("time 5s\n")
    f.write("/write-cd-%s.pl %d %d 60.0 %s %s.%s.band3cdp.dat\n" %(cdp_beam, nchan_writecd, nint_writecd, cdpdisk, name, date))
    f.write(
"""
time 60s
/kill-vlt_gwb.pl
/gwbpsr.stop
/time 5s

/cmd3 "stpndas"
time 5s
stpndas
time 5s

"""
            )



def obs_pul(phase_cal_name, pulsar_name, dm, obstime, start_time):
    obs_sec = float(obstime * 60.0)
    f.write("\n****** Starting observation of PSR %s *******\t%s\n\n" %(pulsar_name, start_time))
    f.write("/cmd3 \"gts \'%s\'\"" %phase_cal_name)
    f.write(
"""
/cmd3 "sndsacsrc(1,12h)"
/cmd3 "sndsacsrc(1,12h)"
/cmd3 "stabct"
/cmd3 "/(gotosrc 10m 3)"
time 5s

"""         
            )

    f.write("gts \'%s\'" %phase_cal_name)
    f.write(
"""
sndsacsrc(1,12h)
sndsacsrc(1,12h)
stabct
/(gotosrc 10m 4)
time 5s

"""         
            )

    f.write("/cmd3 \"strtndas\"\n")
    f.write("/cmd3 \"/phase_gwb.pl -r %s -s 3 -t 40 -p %sB\"\n" %(ref_ant_subarr3, project_name))
    f.write("time 5s\n")
    f.write("strtndas\n")
    f.write("/phase_gwb.pl -r %s -s 4 -t 40 -p %sA" %(ref_ant_subarr4, project_name))



    f.write(
"""
time 5s

/cmd3 "stpndas"
time 5s
stpndas
time 5s

/cmd3 "strtndas"
time 5s
strtndas

time 40s

/cmd3 "stpndas"
time 5s
stpndas
time 5s

"""
            )

    f.write("/cmd3 \"gts \'%s\'\"" %pulsar_name)
    f.write(
"""
/cmd3 "sndsacsrc(1,12h)"
/cmd3 "sndsacsrc(1,12h)"
/cmd3 "stabct"
/cmd3 "/(gotosrc 10m 3)"
time 5s

"""         
            )

    f.write("gts \'%s\'" %pulsar_name)
    f.write(
"""
sndsacsrc(1,12h)
sndsacsrc(1,12h)
stabct
/(gotosrc 10m 4)
time 5s

/cmd3 "strtndasc"
time 5s
strtndasc
time 5s

"""         
            )

    if cdp_beam == "bm1":
        f.write("/gwbpsr.start %s %s 500 1460 1460 1460\n" %(padisk, pulsar_name))
    elif cdp_beam == "bm2":
        f.write("/gwbpsr.start %s %s 1460 500 1460 1460\n" %(padisk, pulsar_name))
    f.write("time 5s\n")
    f.write("/runsubband-cd-%s.pl 200.0 300.0 %d %f %d -1\n" %(cdp_beam, nchan_runsubband, dm, nchan_obs))
    f.write("time 5s\n")
    f.write("/write-cd-%s.pl %d %d %.1f %s %s.%s.band3cdp.dat\n"%(cdp_beam, nchan_writecd, nint_writecd, obs_sec, cdpdisk, pulsar_name, date))
    f.write("time %dm\n" %obstime)
    f.write(
"""
/kill-vlt_gwb.pl
/gwbpsr.stop
time 5s


/cmd3 "stpndasc"
time 5s
stpndasc
time 5s

"""
            )
    

def add_time(init_time, shift):
    act_time = init_time.split(':')
    hour = int(act_time[0])
    minutes = int(act_time[1])

    min_next = minutes + shift
    minutes = min_next % 60
    hour += min_next//60

    if hour >= 24:
        hour = hour - 24

    final_time = ':'.join([str(hour).zfill(2), str(minutes).zfill(2)])

    return final_time

if input_file:
	try:
		input_params = np.genfromtxt(inp_file, dtype=str)
		date = input_params[0]
		start_obs = input_params[1]
		track = input_params[2]
		pa_beam = input_params[3]
		padisk = input_params[4]
		cdp_beam = input_params[5]
		cdpdisk = input_params[6]
		fl_cal_beg = input_params[7]
		fl_cal_end = input_params[8]
	except:
		print("Warning: Error while reading file. Put the input parameters manually.\n")
		input_file = False
    
if not input_file:
	print("Kindly provide the following information. DON'T put the inputs within QUOTATIONS. \n")
	date = str(input("Enter the date of obs (format: 07Dec2019): "))
	start_obs = str(input("Enter starting time of obs (format: 00:00): "))
	track = str(input("outer or inner track (write \"outer\" or \"inner\"): "))
	pa_beam = str(input('Beam for PA observation (write "bm1", "bm2", "bm3" or "bm4"): '))
	padisk = str(input("Disk in which PA data will be written (format: dataN): "))
	cdp_beam = str(input("Beam for cdp pipeline (write \"bm1\" or \"bm2\"): "))
	cdpdisk = str(input("Disk in which CDP data will be written (format: dataN): "))
	fl_cal_beg = str(input("Flux calibrator at the beginning: "))
	fl_cal_end = str(input("Flux calibrator at the end: "))
	
	with open('{}_inputs.txt'.format(date), "w") as f3:
		print("\n....Writing your inputs to the file {}_inputs.txt".format(date))
		f3.write("You have given the following inputs:\n")
		f3.write("date = {}\nstart_obs = {}\ntrack = {}\npa_beam = {}\npadisk = {}\n".format(date, start_obs, track, pa_beam, padisk))
		f3.write("cdp_beam = {}\ncdpdisk = {}\nflux_cal_beg = {}\nflux_cal_end = {}".format(cdp_beam, cdpdisk, fl_cal_beg, fl_cal_end))


setup = np.genfromtxt("setup.in", dtype=str)
project_name = setup[0]
source_list = setup[1]
ref_ant_subarr4 = setup[2]
ref_ant_subarr3 = setup[3]
nchan_obs = int(setup[4])
nchan_runsubband = int(setup[5])
nchan_writecd = int(setup[6])
nint_pa = int(setup[7])
nint_writecd = int(setup[8])
nbits_pa = int(setup[9])
nbits_cdp = int(setup[10])
PFB = setup[11]

pa_int = 5.12 * nint_pa
cdp_int = (1.0/(2.0*200)) * 4 * nchan_writecd * nint_writecd


params = np.genfromtxt(pulsar_file, dtype=str)
data_vol_pa = 0
data_vol_cdp = 0
if len(params.shape)==1:
    params = np.asarray([params])


with open("%s_%s.cmd.txt" %(project_name, date),"w") as f:

    f.write("*** Command file for InPTA pulsar Observation ***\n")
    f.write("*** Prepared using a python script written by Lankeswar Dey ***\n")
    f.write("*** 10/May/2021 Modified for Cycle 40 by BCJ/Lankeswar Dey ***\n")

    f.write(
"""

cmode 1
lnkndasq
time 5s
/cmd3 "lnkndasq"
time 5s

dellist 2
time 5s
/cmd3 "dellist 2"
time 5s

subar 4
time 5s
/cmd3 "subar 3"
time 5s

"""
    )

    if track == "outer":
        f.write(
"""
goout
gosacout
time 5s
/cmd3 "goout"
/cmd3 "gosacout"
time 5s

"""
            )


    elif track == "inner":
        f.write(
"""
goin
gosacin
time 5s
/cmd3 "goin"
/cmd3 "gosacin"
time 5s

"""
                )

    f.write("addlist \'/odisk/gtac/source/bcj/%s\'\n" %(source_list))
    f.write("time 5s\n")
    f.write("/cmd3 \"addlist \'/odisk/gtac/source/bcj/%s\'\"\n" %(source_list))
    f.write("time 5s\n\n")
    f.write("/gwbpsr.init\n")

    time_str = add_time(start_obs, 100)



    if fl_cal_beg and fl_cal_beg != 'None':
        flux_cal(fl_cal_beg, time_str)
        flux_cal(fl_cal_beg + "OFF", add_time(time_str, 2))
        time_str = add_time(time_str, 15)

    for i, inp_psrs in enumerate(params):
        pulsar_name, phase_cal_name, dm, obstime, slew_time, start_time = inp_psrs
        time_str = add_time(time_str, int(slew_time))
        obs_pul(phase_cal_name, pulsar_name, float(dm), float(obstime), time_str)
        time_str = add_time(time_str, int(obstime)+5)
        data_vol_pa += (int(obstime)*60e6/pa_int)*nchan_obs*(nbits_pa/8)/1024**3
        data_vol_cdp += (int(obstime)*60e6/cdp_int)*nchan_writecd*(nbits_cdp/8)/1024**3

    if fl_cal_end and fl_cal_end != 'None':
        time_str = add_time(time_str, 5)
        flux_cal(fl_cal_end, time_str)
        flux_cal(fl_cal_end + "OFF", add_time(time_str, 2))

    f.write("**********  End of Obs ***************\n\nend")







#####
## Creating setup and observstion plan file
#####

subarr4_data_rate =  (60e6/pa_int)*nchan_obs*(nbits_pa/8)/1024**3
subarr3_data_rate = (60e6/cdp_int)*nchan_writecd*(nbits_cdp/8)/1024**3

data_vol_pa = int(data_vol_pa)
data_vol_cdp = int(data_vol_cdp)
data_vol_pa_tot = data_vol_pa + 60
data_vol_cdp_tot = data_vol_cdp + 60
total_data = data_vol_pa_tot + data_vol_cdp_tot

subarr4_data_vol = '{} GB'.format(data_vol_pa_tot)
subarr3_data_vol = '{} GB'.format(data_vol_cdp_tot)
total_data_vol = '{} GB'.format(total_data)

if data_vol_pa_tot >= 1024:
	temp4 = data_vol_pa_tot/1024
	subarr4_data_vol = '{data_vol:.2f} TB'.format(data_vol = temp4)
	
if data_vol_cdp_tot >= 1024:
	temp3 = data_vol_cdp_tot/1024
	subarr3_data_vol = '{data_vol:.2f} TB'.format(data_vol = temp3)
	
if total_data >= 1024:
	temp = total_data/1024
	total_data_vol = '{data_vol:.2f} TB'.format(data_vol = temp)

beam_dict = {'bm1': 'Beam 1',
             'bm2': 'Beam 2',
             'bm3': 'Beam 3',
             'bm4': 'Beam 4'
             }

machine_dict = {'bm1': 'gwbh7',
                'bm2': 'gwbh8',
                'bm3': 'gwbh9',
                'bm4': 'gwbh10'
               }

def exclude_beam(pa_beam, cdp_beam):
	ex_beam = ''
	for x in beam_dict:
		if x != pa_beam and x != cdp_beam:
			ex_beam = ex_beam + x[-1]
	return ex_beam[0] + '/' + ex_beam[-1]


def print_pulsar(psr_name, phase_cal_name, obstime, slew_time, t_start):
    t_start = add_time(t_start, int(slew_time))
    f1.write('      Phase on {}      5 min \t {}\n'.format(phase_cal_name, t_start))
    t_psr = add_time(t_start, 5)
    f1.write('      PSR {}        {} min \t {}\n'.format(psr_name, obstime, t_psr))
    t_end = add_time(t_psr, int(obstime))
    return t_end


with open("%s_setup_%s.txt" %(project_name, date),"w") as f1:
    f1.write(
"""*****  Setup and obsplan file for InPTA Observation (setup.txt)  *****
*****  Prepared using a python script written by Lankeswar Dey  *****
*****  10/May/2021 Modified for Cycle 40 by BCJ/Lankeswar Dey ***** 


"""
            )
    f1.write('Project Code 		: {}\n'.format(project_name))
    f1.write(
"""Project Title 		: Indian Pulsar Timing Array
  
User's Name 		: Bhal Chandra Joshi, A. Gopakumar, M. Bagchi, Y. Gupta, Shantanu Desai, T. Prabu, 
Abhimanyu S, Lankeswar Dey, Nobleson K, Jaikhomba Singha, Suryarao Bethapudi, Dhruv Pathak, M. A. Krishnakumar, 
Neelam Dhanda, Arpita Choudhary, Arun Kumar Naidu, Kishalay Dey, Mayuresh Surnis, Yogesh Maan, P K Manoharan, 
Raghav Girgaonkar, Avishek Basu, Sai Chaitanya, Adarsh Bathula, Ashwin Pandey, Keitaro Takahashi, Neel Kolhe, 
Kotaro Niinuma, Nikita agarwal, Pratik Tarafdar, Prerna Rana, Ryo Kato, Subhajit Dandapat, Tomonosuke Kikunaga, 
Shinnosuke Hisano, Saito Toshiyuki, Arul Pandian, Piyush M, Divyansh Kharbanda


User's email 		: bcj@ncra.tifr.res.in,gopu.tifr@gmail.com,manjari.bagchi@gmail.com,ygupta@ncra.tifr.res.in,
shntn05@gmail.com,prabu@rri.res.in,abhisrkckl@gmail.com,lanky441@gmail.com,nobleson.phy@gmail.com,mjaikhomba@gmail.com,
shining.surya.d8@gmail.com,pathakdhruv9786@gmail.com,kk.ambalappat@gmail.com,neelam.dhanda@gmail.com,arp.astro@gmail.com,
arunnaidu123@gmail.com,kde@caltech.edu,msurnis@gmail.com,ymaan4@gmail.com,mano.rac@gmail.com, raghav.girgaonkar@gmail.com,
avishekbs3@gmail.com,saichaitanya16@iisertvm.ac.in, ms18109@iisermohali.ac.in,me17btech11049@iith.ac.in,keitaro@kumamoto-u.ac.jp,
neel.kolhe@xaviers.edu.in,niinuma@yamaguchi-u.ac.jp,nikitaagar2503@gmail.com, pratikta16@gmail.com,prerna.rana92@gmail.com,
rkato@sci.osaka-cu.ac.jp, subhajit.phy97@gmail.com,amqmysuto@gmail.com,145s3023hs@gmail.com, worldund315@icloud.com,
arulpandian05101995@gmail.com,pmarmat@ph.iitr.ac.in,ep19btech11002@iith.ac.in


"""         )
    
    f1.write('Date of Obs 		: {} {}, {}\n'.format(date[:2], date[2:5], date[5:]))
    f1.write('Start Time(IST hours) 	: {}\n\n'.format(start_obs))

    f1.write('1. Make sure that {}:/{} and {}:/{} have at least {} and {} disk space, respectively\n'.format(machine_dict[pa_beam], padisk, machine_dict[cdp_beam], cdpdisk, subarr4_data_vol, subarr3_data_vol))

    f1.write(
"""
2. This is a TWO beam observations. The antenna will be scattered in two 
   subarrays and two beams.
"""         )

    f1.write('    suba 4 - Band 5 - {}/{} PA mode\n'.format(beam_dict[pa_beam], exclude_beam(pa_beam, cdp_beam)))
    f1.write('    suba 3 - Band 3 - {} Voltage mode - CD pipeline\n'.format(beam_dict[cdp_beam]))
    
    f1.write(
"""
3. Pointing is needed ONLY in Band 5. 
   Then UPDATE BY HAND POINTING OFFSETS FOR 325 ANTENNAS from results 
   of previous pointing offset determination
"""
            )
    f1.write('4. The total data volume for this session is likely to be {} for all beams\n'.format(total_data_vol))
    f1.write('so we need {} and {} in {}:/{} and {}:/{}, respectively\n\n'.format(subarr4_data_vol, subarr3_data_vol,machine_dict[pa_beam], padisk, machine_dict[cdp_beam], cdpdisk))
    f1.write('--------------------------------------------------------------------------\n')
    f1.write('LTA file : /gwbifrdata/{0}/{1}A,{1}B\n'.format(date[:5].lower(), project_name))
    f1.write('source list : /odisk/gtac/source/bcj/{}\n'.format(source_list))
    f1.write('cmdfile : /odisk/gtac/cmd/bcj/{}_{}.cmd\n'.format(project_name, date))
    f1.write('-----------------------------------------------------------------------\n')

    f1.write(
"""
===========================================================================
GWB Settings

MODE            : REALTIME
LTA             : 8    (5 sec)
ACQ BW          : 200 MHz
"""         )
    f1.write('NO OF CHAN      : {}'.format(nchan_obs))
    f1.write(
"""
STOKES          : 2 Total Intensity
TPA SELECTION   : MANUAL
GAIN            : ON
FSTOP           : ON
BITS            : 8
DDC             : 0 (Narrow band mode OFF)

"""			)
    if PFB == 'ON':
        f1.write('PFB             : ON\n')
        f1.write('PFB_TAPS        : 4\n')
    elif PFB == 'OFF':
        f1.write('PFB             : OFF\n')

    f1.write('\n\nSubarr  4\n')
    f1.write('{}          : PA beam'.format(beam_dict[pa_beam]))
    f1.write(
"""
GAC Config      : C00 C04 C05 C10 C13 W01 W02 W03 W04 E02 E03 E04 S01 
                  S02 S03 S04                  Ref : C05  = 16
BAND            : BAND 5 (1000 - 1460)
SIDEBAND        : LSB
SUBBAND FILTER  : Full band
RF              : 1460-1260 MHz WB feed, RF ON, NG OFF
GAB             : 200 MHz ALC OFF
Ist LO          : 1460 MHz
TPA             : Manual (Set so as to get band from 1460 to 1260 MHz)
                  1460 1460 1530 1530  70 70  
Optical Fibre   : Attn. of 5 dB for the OFC.
"""         )
    f1.write('LTA File        : {}A\n'.format(project_name))
    f1.write('Beam recording  : {} bit - Total intensity mode\n'.format(nbits_pa))
    f1.write('Beam Integ      : {} us (NFFT={}) ({sub4_data_rate:.1f} GB/min)\n'.format(pa_int, nint_pa, sub4_data_rate=subarr4_data_rate))
    f1.write('Data Volume     : {} + 60 GB = {} GB'.format(data_vol_pa, data_vol_pa_tot))
    f1.write(
"""

Subarr  3 
"""         )
    f1.write('{}          : Voltage PA beam CD pipeline'.format(beam_dict[cdp_beam]))
    f1.write(
"""
GAC Config      : C01 C02 C06 C08 C09 C11 C12 C14 Ref : C09 = 8
BAND            : BAND 3 (250-500)
RF              : 500-300 MHz WB feed, RF ON, NG OFF
SIDEBAND        : LSB
GAB             : 200 MHz ALC OFF
Ist LO          : 500 MHz 
TPA             : Manual (Set so as to get band from 500 to 300 MHz)
                  500 500 570 570 70 70 
Optical Fibre   : Attn. of 13 dB for the OFC.
"""         )
    f1.write('LTA File        : {}B\n'.format(project_name))
    f1.write('Beam recording  : {} bit - Total intensity mode\n'.format(nbits_cdp))
    f1.write('Beam Integ      : {} us (NFFT={}) ({sub3_data_rate:.1f} GB/min)\n'.format(cdp_int, nint_writecd, sub3_data_rate=subarr3_data_rate))
    f1.write('CD Pipeline1    : ./runsubband-cd.pl 200 300 {} <DM> {} -1\n'.format(nchan_runsubband, nchan_obs))
    f1.write('CD Pipeline1    : ./write-cd.pl {} {} <time> <datadir> B1937+21.{}.band3cdp.dat\n'.format(nchan_writecd, nint_writecd, date))
    f1.write('Data Volume     : {} + 60 GB = {} GB'.format(data_vol_cdp, data_vol_cdp_tot))
    f1.write(
"""

==========================================================================

Plan
"""         )
    f1.write('{} Feed rotation, Cross pointing Band 5, Update pointing by hand'.format(start_obs))
    f1.write("""
      NLDANTO.001 with previous offsets for Band 3 and newly determined 
      offsets for Band 5. Check correct feed rotation
      
"""         )

    t_split_ant = add_time(start_obs, 50)
    f1.write('{} Split antennas into 2 subarrays, define project codes for each subarray\n'.format(t_split_ant))
    f1.write('     suba 4 - Band 5 - {} PA mode - {} int - {} - {}\n'.format(beam_dict[pa_beam], nint_pa, machine_dict[pa_beam], padisk))
    f1.write('     suba 3 - Band 3 - {} Voltage mode - CD pipeline - {} - {}\n\n'.format(beam_dict[cdp_beam], machine_dict[cdp_beam], cdpdisk))

    t_gab = add_time(t_split_ant, 10)
    f1.write('{} setup GAB and GWB to record LTA and pulsar data in subarrays\n\n'.format(t_gab))

    t_pow_eq = add_time(t_gab, 5)
    f1.write('{} Power Equalize on {} 150/200 counts subarr 3,4\n\n'.format(t_pow_eq, fl_cal_beg))

    t_chk_band = add_time(t_pow_eq, 15)
    f1.write('{} Check bandshapes and remove antenna with bad bandshapes\n      Start correlators and check fringes and remove antenna with no fringe\n'.format(t_chk_band))
    f1.write('      Check disk space for {} in {} and {} in {} - at least {} in each required'.format(padisk, machine_dict[pa_beam], cdpdisk, machine_dict[cdp_beam], subarr4_data_vol))
    f1.write("""
      Modify command file to reflect the chosen disk
      Finalize GAC beams
      Record final RF, GAC, USB/LSB, Beam integration for each subarray 
      in LOGFILE
      
"""         )

    t_cmd = add_time(t_chk_band, 10)

    if fl_cal_beg and fl_cal_beg != 'None':
        t_phase = add_time(t_chk_band, 10)
        f1.write('{} Phase on {}\n\n'.format(t_phase, fl_cal_beg))
        t_cmd = add_time(t_phase, 10)

    f1.write('{} Start the command file, source order as below\n'.format(t_cmd))

    t_pul_strt = t_cmd

    if fl_cal_beg and fl_cal_beg != 'None':
        f1.write('      {} on 1 min\n'.format(fl_cal_beg))
        f1.write('      {} off 1 min\n      Slew 11 min\n'.format(fl_cal_beg))
        t_pul_strt = add_time(t_cmd, 13)

    for i, inp_psrs in enumerate(params):
        pulsar_name, phase_cal_name, dm, obstime, slew_time, start_time = inp_psrs
        t_pul_strt = print_pulsar(pulsar_name, phase_cal_name, obstime, slew_time, t_pul_strt)

    t_end = t_pul_strt

    if fl_cal_end and fl_cal_end != 'None':
        f1.write('      Slew 5 min\n')
        f1.write('      {0} on 1 min\n      {0} off 1 min\n\n'.format(fl_cal_end))
        t_end = add_time(t_pul_strt, 7)
    f1.write('{} End of observation\n'.format(t_end))
