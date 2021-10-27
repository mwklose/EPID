# Meetings.MD
## Sep 30th meeting
    - Review of Sierra Plots
        - Updated pictures, makes better sense, more interpretable?
        - Case when plateau: SE show better?
    - Letter
        - Alternative ways to visualize confidence intervals
            - ex1
            - ex2
    - Distributions:
        - Dividing two: ratio distribution (Cauchy Distribution special case)
            - Found that always slightly above expectation?
        - Multiplying two: product distribution
            - Found that always slightly below expectation (but less so)
            - https://en.wikipedia.org/wiki/Distribution_of_the_product_of_two_random_variables
                - "extra stuff"
    Meet:
    - Sierra Plots
        - Go back to pure coloring/scale
            - 3x as much
            - Smooth scaling
                - Write in Python+one more
        - Letter: 600 words max, AJE and Epidemiology
            - Epidemiology: most recent issue, look for Kaplan Meier curves, Risk Difference function by time, 
            - Letter say: descriptions: turn, cite Paul, degradation of random error, generalize P-value plot to time. 

    - Next things:
        - Attributable Fractions? Exploration/writeup: how to make inference - Bootstrap, Delta Method (data fusion), 

        - Lead: data repository, datasets+code book (short piece to advertise space), count as practicum
            - Build contributory trials

        - Daniel: Causal Consistency assumption, (710, 715), 

        - Baric:
            - Herd immunity + interference
                - Difficult without potential outcomes
            - Herd immunity + interference of COVID19 (Halloran's work)
            - Modern take on Herd Immunity, Interference

            Main ideas: 
            - Therapeutic antibodies: role in controlling COVID19 pathogenesis.
            - Paramyxovirus genus Henipavirus: Emerging Disease Potential.

            - Follow structure pretty straightforward
            - 
## Sep 16th meeting
    - Review of Sierra Plots
        - Questions from last time:
            - Always normally distributed? NO
        - Generalizable when given function, take in mean+sd+point query (aka could give uniform distribution = Twister plot)
        - Not 100% vectorized
    - TODO: documentation, more generalizable
    - Questions:
        - Confirm: risk difference has normal distribution, risk ratio has lognormal distribution/pseudo lognormal?
        - What other distributions are possible/wanted?

    - Next steps: 

    - Data Scrapping/Intro to Internet:
        - HTTP requests/how is data sent over websites?
        - Scrape data based on that?
        - How to find elgible websites/examples? (aka not Tableau IIRC)

        - Focus on survival functions!/figures/back data out from there
        - Epi focus on data when deciding to collect/how to collect it (wrong timeframe type deal)

    - Classes:
        - Baric: material super advanced
        - CS Minor? 
            - Pros: combine with research, capability to do so, crossover knowledge, expect to use later, fellowship opportunities?
            - Cons: extended classes into 4th year realistically (1/semester * 5 semesters), one course subset not perfect

## Next steps 9/16:
    - Letter: summarizing of alternative ways to express confidence intervals, break away from interval+point paradigm/understanding?
        - Expected pushback: how to decide shaded at what point?
            - 
    - Descent of gradient sharper? 
        - Triple standard error for working for example
        - So maybe in cases with low SE, this plot not best option?
    - Make graph --> go SUPER far out (.9999 -> 4 SE), add lines for 95% confidence interval
        - Increase SE for example? (Another dataset/false dataset?)
        - Check another colormap
        - Output as .eps file for AJE (does not support transparencies) more NOTE
            - Colormap to get color specifically

    - Case: plateau --> set of answers given data/design complex. If case, have black line if ridge, plateau = no line

    - Attributable Fraction --> 2003 Greenland+  ---> Simulation to get CLimits. What happens with varying values of 'a'. Sharpness of probability known/unknown
        - Delta Method (Taylor Series expansion other ways)
        - Closed form analytic, simulation approach

    - Before: assumed constant across W (same population), but what if population changes, W different in two settings (transportability/generalizability problem)




## Agenda:
    - Ultimate purpose:
        - SER workshop? Deadline September 10th? NOT FOR ME. 
        - What are next steps needed?
    - Adding more?
    - Going forwards: 

If time:
    - BIOS662
        - Not getting much out of it, recorded lectures
        - Worth coming to meetings for an hour? 
    - BIOS minor common --> What about CS minor? Would it be worth it?

## Results so far:
    - Trial 1: failure (misunderstood)
    - Trial 2: overlapping step functions
        - Alright, but relies on a couple of assumptions
            - Even, normal distribution around true value and CIs
            - Is this always the case? NO???
    - Trial 3: shading rectangles
        - Allows finer control
        - Not straightforward/reproducible way to do this (imshow seems most promising)
            
    - Trial 4: will have to be bit mapping
        - Although very computationally intensive, only way to more or less guarantee
        - Also allows for stronger control of shading


Next step: Seaborn heatmaps as way to go forward.  