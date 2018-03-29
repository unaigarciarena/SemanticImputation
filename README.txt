To run an experiment:

	1- Run the python command with the following arguments:
		a) "distances.py"
		b) The distance that will be used to rank the IMs [0,7]
		c) The instance. The identifier that the output will contain in its name
		For example "python distances.py 0 aa"
		This will create the "{Short|Long}TS[0-3]D[0-7]<instance>.csv" files.
		These files contain the distances between the original TS and each one of the imputed ones.
	2- Then run "python unir.py" to merge all results into "{Short|Long}TS[0-3]D[0-7].csv" files.
		These files contain the result of 10 runs of the distance between the original TS and its imputed versions.
	3-Run "tests.py" to create the matrix composed by statistical test differences.
	
See the "WorkFlowDiagram.png" for an in depth understanding of the program. The top part works in a counterclockwise direction, 
starting from the top left call to toyDB.py.


Functions used in chronological order:

	1.- distanceTable in distances.py
	
		2.- toyGenerator in toyDB.py provides the multivariate TS that will be used in the experiment
			Either generates the synthetic TS or calls
			
				3.- TSdist{1,2,3}.r to import one of the three TSs available in the TSdist package of R
			
			Then it returns the complete TS and other copy with MD in it (Short or Long)
			
		4.- discretize in discretization.py. Takes the DB with MD as an argument, and returns other matrix with the discretized values.
		
		5.-MIMatrix in mutualInfo.py takes the TS and returns a square matrix with the mutual information between the variables.
		
		6.- linearInterpolation in interpolation.py. Takes a copy of the TS with MD and imputes it
		
		7.- pchipInterpolation in interpolation.py. Takes a copy of the TS with MD and imputes it
		
		8.- quadInterpolation in interpolation.py. Takes a copy of the TS with MD and imputes it
		
		9.- splineInterpolation in interpolation.py. Takes a copy of the TS with MD and imputes it
		
		10.- tsImputation in imputation.py. Takes a copy of the TS with MD and calls
		
			11.- kalman.r, which imputes the TS.
			
		12.- simple in imputation.py (with the "0" argument). Takes a copy of the TS with MD and calls
		
			13.- EM.r, which imputes the TS.
		
		14.- simple in imputation.py (with the "1" argument). Takes a copy of the TS with MD and calls
		
			15.- mice.r, which imputes the TS.
			
		16.- regression in imputation.py (with the "0" in the "fullreg" argument and the EM-imputed DB as input). Returns the DB imputed by regression based on EM
			
		17.- regression in imputation.py (with the "1" argument and the Kalman-imputed DB as input). Takes a copy of the TS with MD and calls
		
			18.- bySimilarity in obSel, which returns the similar observations for the polished models.
			
			19.- obsIndex in obSel, which groups the missing spots by the model they will be predicted from, and which observations the model will be built from.
			
		20.- Distances in distances.py, with all the imputed TSs and the original one. It returns the dissimilarity between them and the original.
		
		21.- savetxt, to write the results.
		
	22.- unir.py, which merges all the instances in one file for each distance and each TS.
	
	23.- tests.py, which performs the statistical tests.