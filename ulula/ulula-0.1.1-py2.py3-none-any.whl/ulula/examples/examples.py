###################################################################################################
#
# Ulula -- examples.py
#
# Example applications for the Ulula code
#
# by Benedikt Diemer
#
###################################################################################################

import ulula.simulation as ulula_sim
import ulula.run as ulula_run
import ulula.setups.advection as setup_advect
import ulula.setups.kelvin_helmholtz as setup_kh
import ulula.setups.sedov_taylor as setup_sedov
import ulula.setups.shocktube as setup_shocktube

###################################################################################################

# Default hydro scheme
def_hydro_scheme = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', 
						riemann = 'hll', time_integration = 'hancock', cfl = 0.8)

###################################################################################################

def main():
	
	#advectionTest()
	
	#shocktubeTest()

	#kelvinHelmholtzTest()
	#kelvinHelmholtzMovie()
	
	#sedovTest()

	return

###################################################################################################

def advectionTest():
	"""
	Test of different solvers in 2D advection problem
	
	This function produces four runs of the same top-hat advection problem. An initial overdense
	disk is moving with the fluid towards the top right of the domain. The edges of the disk 
	diffuse into the surrounding fluid at a rate that depends on the hydro solver. When using the
	MC limiter with an Euler (first-order) time integration, the test fails entirely.
	"""

	setup = setup_advect.SetupAdvect()
	kwargs = dict(nx = 100, tmax = 2.5, movie = False, save = True, q_plot = ['DN'])

	hs = ulula_sim.HydroScheme(reconstruction = 'const', cfl = 0.8)
	ulula_run.run(setup, hydro_scheme = hs, fn_suffix = '_const', **kwargs)

	hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'minmod', time_integration = 'euler', cfl = 0.8)
	ulula_run.run(setup, hydro_scheme = hs, fn_suffix = '_linear_minmod_euler', **kwargs)

	hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', time_integration = 'euler', cfl = 0.8)
	ulula_run.run(setup, hydro_scheme = hs, fn_suffix = '_linear_mc_euler', **kwargs)

	hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', time_integration = 'hancock', cfl = 0.8)
	ulula_run.run(setup, hydro_scheme = hs, fn_suffix = '_linear_mc_hancock', **kwargs)
	
	return

###################################################################################################

def shocktubeTest():
	"""
	1D test of hydro solver with shock tube
	
	This function executes a shocktube test in pseudo-1D (by creating a domain that is much longer
	in x than in y, and by making it symmetric in y). The function creates outputs for piecewise-
	constant states and piecewise-linear reconstruction.
	"""

	setup = setup_shocktube.SetupSodX()
	kwargs = dict(tmax = 0.2, nx = 100, save = True, plot1d = True, q_plot = ['DN', 'VX', 'PR'])
	
	hs = ulula_sim.HydroScheme(reconstruction = 'const', cfl = 0.5)
	ulula_run.run(setup, hydro_scheme = hs, fn_suffix = '_const', **kwargs)

	hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'vanleer', riemann = 'hll', 
							time_integration = 'hancock', cfl = 0.5)
	ulula_run.run(setup, hydro_scheme = hs, fn_suffix = '_linear', **kwargs)
	
	return

###################################################################################################

def kelvinHelmholtzTest():
	"""
	The Kelvin-Helmholtz instability
	
	This function creates an interactive plot of the Kelvin-Helmholtz instability. It should take
	less than a minute to run on a modern laptop.
	"""

	kwargs = dict(tmax = 2.0, nx = 200, q_plot = ['DN', 'VX'], movie = False, save = False)
	hs = ulula_sim.HydroScheme(reconstruction = 'linear', time_integration = 'hancock', limiter = 'mc', cfl = 0.9)
	
	setup = setup_kh.SetupKelvinHelmholtz(n_waves = 1)
	ulula_run.run(setup, hydro_scheme = hs, **kwargs)

	return

###################################################################################################

def kelvinHelmholtzMovie():
	"""
	Movie of the Kelvin-Helmholtz instability
	
	This function demonstrates how to make movies with Ulula. By passing the ``movie`` parameter,
	the function outputs frames at a user-defined rate and combines them into a movie at the end
	of the simulation.
	"""

	kwargs = dict(tmax = 4.0, nx = 200, q_plot = ['DN', 'VX'], movie = True, plot_every = 4)
	hs = ulula_sim.HydroScheme(reconstruction = 'linear', time_integration = 'hancock', limiter = 'mc', cfl = 0.9)
	
	setup = setup_kh.SetupKelvinHelmholtz(n_waves = 1)
	ulula_run.run(setup, hydro_scheme = hs, **kwargs)

	return

###################################################################################################

def sedovTest():
	"""
	Test of Sedov-Taylor explosion against analytic solution
	
	This function demonstrates another style of 1D plotting where the solution is averaged in 
	radial bins.
	"""

	setup = setup_sedov.SetupSedov()
	kwargs = dict(tmax = 0.02, nx = 200, q_plot = ['DN', 'PR', 'VT'], save = True, plot1d = True, plot_type = 'radius')
	#kwargs = dict(tmax = 0.02, nx = 200, q_plot = ['DN', 'PR'], movie = False, save = False, plot1d = False)

	hs = ulula_sim.HydroScheme(reconstruction = 'linear', time_integration = 'hancock', limiter = 'mc', cfl = 0.9)
	ulula_run.run(setup, hydro_scheme = hs, fn_suffix = '', **kwargs)
	
	return

###################################################################################################
# Trigger
###################################################################################################

if __name__ == "__main__":
	main()
