# eki-study
All code and data associated with study described in: McKiernan EC. (2015) A genetic manipulation of motor neuron excitability does not alter locomotor output in <i>Drosophila</i> larvae. <i>PeerJ PrePrints</i> 3:e1434 https://dx.doi.org/10.7287/peerj.preprints.469v3

<h2>Raw recordings</h2>

Dual intracellular recordings were made from muscles in the body wall of <i>Drosophila</i> larvae, as described previously <a href="https://peerj.com/articles/57/">(McKiernan, 2013)</a> and in a preprint describing the current work <a href="https://peerj.com/preprints/469v3/">(McKiernan, 2015)</a>. The electrical activity of interest was spontaneous, rhythmic bursting activity underlying crawling. </p>

All raw recordings are available in both ABF (Axon) and SMR (Spike2) formats. Although these are proprietary file formats, the raw recordings can be read and plotted using the python package <a href="https://pythonhosted.org/neo/">Neo</a>. Please see the ipython notebook provided in this repository for instructions on how to read and plot recordings. </p> 

Burst start and end times were marked within the raw recordings and these time stamps exported to csv files. Please note that due to several factors, such as (1) electrode placement and stability and (2) the presence or absence of rhythmic bursting activity, only portions of each recording were included in the final analysis. The accompanying master csv spreasheet lists the analyzed burst times for each animal and recording channel. These burst times can be used to find the relevant activity within the raw recordings. For example, if the first burst time for that animal is listed at 200 and the last at 400, the relevant bursting activity within the recording is found between the 200- and 400-second marks. 

<h2>Spreadsheets</h2>
The master csv spreadsheet contains information on all larvae included in the final analysis. (Additional recordings were performed but excluded due to issues with electrode stability or lack of rhythmic activity.) The columns list the following information:

<ol type="1">    
<li>Date on which the recording was performed (yyyy-mm-dd format).</li>
<li>File number of the recording (in either ABF or SMR format) and the channel within the recording (Ch1=channel 1; Ch2=channel2). All recordings have two recorded channels. One channel contains a recording from a muscle innervated by control (wildtype) motor neurons, and the other channel contains a recording from a neighboring muscle innervated by at least one motor neuron expressing the genetic manipulation 'Electrical Knock-In' (EKI). For more information on the EKI line, see the preprint <a href="https://peerj.com/preprints/469v3/">(McKiernan, 2015)</a>.</li>   
<li>Animal or 'prep' (preparation) number in the sample. In total, thirteen larvae were included in this study. The prep number can be used for ease of seeing which recorded channels belong to which animal. Again, all animals have two recorded channels, a wiltype and an EKI channel.</li>
<li>Experimental condition, i.e. whether the recorded muscle was innervated by either wildtype motor neurons (control) or EKI-expressing (manipulated) motor neurons.</li>
<li>Motor neuron expressing the genetic manipulation EKI. EKI was expressed in either motor neuron MN1-Ib or MNISN-Is, or in both motor neurons (MN1-Ib+MNISN-Is) innervating the same segment.</li>
<li>Abdominal body wall segment in which the recording was made. The anterior-most recorded segment was abdominal segment 3, and the posterior-most was segment 6.</li>
<li>Burst time points (in seconds) extracted from the raw recordings. Each burst consists of a start and an end time, i.e. a pair of time points is associated with each burst. To facilitate identification of which start and end times belong to which bursts, each burst is marked with a letter in order of occurrence, i.e. the first burst is marked 'A' and consists of the time points 'Burst start A' and 'Burst end A'. Subsequent bursts are marked in alphabetic order up to the end of bursting activity. Each EKI and wildtype channel recorded from the same animal have the same number of bursts, and therefore the same number of burst start and end times. However, not all animals have the same number of bursts; this depends on the duration of rhythmic activity. For one animal, the last burst in the train may be burst 'H', while in another animal the last is burst 'X'. Blank cells within the burst times field indicate there was no more bursting activity to be quantified in that animal. </li>
</ol>

To illustrate how data were analyzed, spreadsheets containing only the burst data from WT and EKI channel in animals expressing the manipulation in at least one motor neuron have also been included. Please see the ipython notebook provided in this repository for details on how to analyze the bursting data.
