# omscentral_data_visualizer

This is an interactive 3D plot meant to help visualize the average metrics (difficulty, workload, rating) that students use to review courses on OMSCentral which can be found here:
https://omscentral.com/courses.

See it in action [here](https://klott.xyz/omscs_visualizer/omscs_plotly_visualizer.html). A snapshot of what the tool looks like can be seen below:

![image](https://klott.xyz/omscs_visualizer/visualizer-preview.png)

## How to use this tool?

You will need to run the script (without arguments) with the corresponding data file in the same directory to produce a new html file. After loading it in a browser, you can rotate the plot around by clicking and dragging with mouse, then zoom with scroll wheel. Clicking individual points takes you to the respective course page on OMSCentral. You may also filter courses by department by clicking on the legend. Individual icon sizes reflect how many people have reviewed the class.

## Why make this tool?

While one can sort courses on OMSCentral based on difficulty, ratings, or workload, it can be difficult to comprehend these metrics all at once when choosing classes. I often found myself filtering courses from one criteria, then another, then going in circles. Being able to see these metrics in three dimensions made these pairwise comparisons much less neccessary.

## What exactly is the tool?

In its current form, this is an interactive 3D scatter plot. Specifically, an HTML document embedded with a lot of Javascript - all of which was generated using Plotly. You can read more about Plotly here:
https://plotly.com/.

## Limitations

It should be noted that not every single course is displayed here: I have chosen to ommit courses with too few reviews (<5) or ones that are outliers at the time of making it. Outliers in this case means courses with > 40 hour/week workload or having reviews less than 2/5. This only ommitted two classe when I made it.

Additionally, this data was parsed very crudely: it's just a sample that was manually made and is not current.
As time goes on, this data will become stale and need to be updated. Having this tool point to the same database that OMSCentral uses would be a logical next step.

## A gentle reminder to users

It should be noted that courses can change semester to semester. While this plot can help identify a group of courses you'd like to take or stay away from, it is best to verify the reviews by actually reading them. It is not uncommon for classes with average historical reviews of 4+/5 to suddently become 2/5 in recent semesters... or negative reviews from students who didn't even read
the course requirements. It's best to think of the plot as a starting point.

I created this tool to make my own life easier during registration - hopefully it does the same for you!
