## Computational Tools for Adaptive Resolution Molecular Dynamics Simulation 

Applicability of Gaussian Processing (GP) can be tested by using GP testcase which is provided here.

- GPYTest direcotry contains small python file to test GP.

Here, the atomistic trajectories are analyized to build:

- Coarse Grained particle based on the centers of mass of the molecules:

		CG_1B_Steps: An 1-Bead Coarse-Grained potentials from Radial distribution function.
					- including an example to apply this method to Water molecueles.

		CG_IE_Steps: Coarse-Grained potentials from intermolecular interactions.
					- including an example to apply this method to Water molecueles.
					
- To calculate the Thermodyanmic force for AdResS method, 
		
		TF_Calculations: All necessary scripts to generate the potentials are in ./scripts directory.
		
		Since all necessary tools are written in Python, you can call these codes from ESPResSo++ program.
		ESPResSo++: [http://www.espresso-pp.de]

- If you have questions, please contact Masa Watanabe [masa.watanabe@stmary.edu]
