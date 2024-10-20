################################################
#
#  Extract formants from annotated textgrids
#
################################################
#
# Preparation: 
# work with a recording that contains the vowels 
#     that you want to analyze
#
# Create a formant object for that sound,
# and do it carefully
#  (ensure the formant settings are appropriate 
#    for the individual talker's voice)
#
# Mark the intervals that you want to analyze
#   in a Textgrid, like this:
#
#    ~~~~~~~~------~~~~~~~---~~~~~~~---
#   __________________________________
#    |   ah  |     |  ih  |  |  eh  |
#
################################################
#
# Name of the Textgrid file that you annotated
# (should also be the name of the Formant object)
	name$ = "name_of_your_object"

# How many timepoints?
	num_timepoints = 10

# Which tier are your annotations?
	v_tier = 1

# Make the table
	Create Table with column names: "formants", 0, "vowel time_index v_time time_abs F1 F2 F3"
	row_index = 0

# Count the intervals
	select TextGrid 'name$'
	num_intervals = Get number of intervals: v_tier

# Loop through the intervals
   for interval_index from 1 to num_intervals
	select TextGrid 'name$'
	label$ = Get label of interval: v_tier, interval_index

	# proceed if the label isn't empty
	if label$ <> ""
		t_start = Get start time of interval: 1, interval_index
		t_end = Get end time of interval: 1, interval_index
		time_interval = (t_end - t_start)/(num_timepoints-1)

		selectObject: "Formant 'name$'"

		# Loop through the timepoints
		   for time_index from 1 to num_timepoints
			time_re_onset = (time_index-1)*time_interval
			current_time =  t_start + time_re_onset
			select Formant 'name$'
			f1 = Get value at time: 1, current_time, "hertz", "Linear"
			f2 = Get value at time: 2, current_time, "hertz", "Linear"
			f3 = Get value at time: 3, current_time, "hertz", "Linear"

		     # Add info to the table
			select Table formants
			Insert row: row_index + 1
			row_index = row_index + 1
			Set string value: row_index, "vowel", label$
			Set numeric value: row_index, "time_index", time_index
			Set numeric value: row_index, "v_time", 'time_re_onset:3'
			Set numeric value: row_index, "time_abs", 'current_time:3'
			if f1 != undefined
				Set numeric value: row_index, "F1", 'f1:0'
			else
				Set string value: row_index, "F1", "NA"
			endif
			if f2 != undefined
				Set numeric value: row_index, "F2", 'f2:0'
			else
				Set string value: row_index, "F2", "NA"
			endif
			if f3 != undefined
				Set numeric value: row_index, "F3", 'f3:0'
			else
				Set string value: row_index, "F3", "NA"
			endif

		   endfor

	# end conditional if label isn't blank
	endif

   # end loop through the intervals
   endfor
