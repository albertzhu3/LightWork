import pandas as pd
from LightWork.helper import filterExercises
from LightWork.weightGenerators import makeCalisthenicsRoutine, \
    makeFullBodyRoutine, makeWeightRoutine


class Workout(object):
    """
    Workout class objects are objects with all necessary inputs from
    the user to make a full workoutself.
    generate(Warmup/Routine) are used to make content as they start empty.
    formatFullRoutine is used to assign reps and sets.
    """

    # Make workout class
    def __init__(self, data, target, allParts, repRanges, gear):
        """
        Input data: pandas DataFrameself.
        target - string: if a cardio workout - has to be workout type. Else,
        a target muscle group - has to be in data.
        allParts: list of strings - containing all sub muscle groups. If
        cardio, should be a None type.
        repRanges: list - of rep ranges in ascending order.
        gear: string - Level of gym equipment available.
        """
        super(Workout, self).__init__()

        # Data (All exercises)
        self.data = data

        # Target body part
        self.target = target

        # Muscle group muscles
        self.parts = allParts

        # Get available rep ranges
        self.rr = repRanges

        # Init warmup exercises
        self.warmup = {}

        # Init workout exercises
        self.routine = {}

        # Assign gear for debugging
        self.gear = gear

    # Getters & Setters
    # Data
    def getData(self):
        return self.data

    def setData(self, newData):
        self.data = newData

    # Target
    def setTarget(self, newTarget):
        self.target = newTarget

    def getTarget(self):
        return self.target

    # Parts
    def setParts(self, newParts):
        self.parts = newParts

    def getParts(self):
        return self.parts

    # Rep Ranges
    def setRepRanges(self, newRepRanges):
        self.rr = newRepRanges

    def getRepRanges(self):
        return self.rr

    # Warmup
    def getWarmup(self):
        return self.warmup

    def setWarmup(self, newWarmup):
        self.warmup = newWarmup

    # Routine
    def setRoutine(self, newRoutine):
        self.routine = newRoutine

    def getRoutine(self):
        return self.routine

    # Gear
    def getGear(self):
        return self.gear

    # Generate Warmup dict
    def generateWarmup(self):
        """
        Uses class properties to output a workout warmup. Returns a dict,
        of key:value pairs where key is an warmup exercise with a value of
        of one set's worth of work
        """

        # Get necessary properties
        # print("Get data")
        genData = self.getData()

        # Create warmup
        # Filter data for plyo and calisthenics options
        # print("Filter warmup exercises")
        warmupData = filterExercises(genData, ["ExerciseType"],
                                     [["Calisthenics", "Plyo"]])

        # Get warmup rep ranges
        # print("Warmup rep ranges")
        warmupRR = ["5 seconds", "10 seconds", "15 seconds"]

        # Get 3 exercises
        # Cardio exercise for warmup
        # print("Get cardio warmup exercise")
        fbWarmupExercise = filterExercises(genData,
                                           ["MuscleGroup", "MainLift"],
                                           [["Full"], ["No"]]
                                           ).Exercise.sample(1).tolist()

        # Assign to final list
        # print("Add to list")
        warmupExercises = fbWarmupExercise

        # Extend by two local exercises
        # print("Add on warmup exercises")
        warmupExercises.extend(warmupData.Exercise.sample(2).tolist())

        # Assign each with reps / sets
        # print("Initialise dict")
        warmup = {}

        # Assign reps to exercise
        for i in range(3):
            # print("Add exercise")
            warmup[warmupExercises[i]] = warmupRR

        # print("Successfully created warmup")

        #  Set self.warmup as new warmup
        self.setWarmup(warmup)

        # print("Successfully set warmup\n")

    # Generate routine dict
    def generateRoutine(self):
        """
        Uses class properties to output a workout warmup. Returns a dict,
        of key:value pairs where key is an exercise with a value of an
        of one set's worth of work
        """

        # Get necessary properties
        genData = self.getData()
        target = self.getTarget()
        allParts = self.getParts()
        repRanges = self.getRepRanges()
        gear = self.getGear()
        # print("Got internal variables")

        # Create main routine
        # Init return object
        routine = {}
        # print("Initialised routine")

        # Check that allParts is not None (If None, gen cardio workout)
        # If Cardio (similar to warmup, 10 Exercise cirucuit or 36mins of
        # cardio)
        if allParts is None:
            # print("Cardio workout")

            # Mixed cardio workout
            if target == "both":

                # print("Mixed routine")
                routine = makeMixedRoutine(genData, repRanges)

            elif target == "regular":

                # print("Regular routine")
                routine = makeRegularRoutine(genData, repRanges, gear)

            elif target == "hiit":

                # print("HIIT routine")
                routine = makeHiitRoutine(genData, repRanges)

            # Set as routine
            self.setRoutine(routine)
            # print("Cardio Routine Set\n")

        # Calisthenics workout i.e. no gym
        elif gear == "gymless":

            # print("Calisthenics workout")
            routine = makeCalisthenicsRoutine(genData, target, repRanges)

            # print("Successfully generated routine")
            self.setRoutine(routine)

            # Set as routine
            # print("Successfully set routine\n")

        # Else weight training (Each part in part should be the major focus
        # of at least one exercise and the minor focus in at least one more.)
        else:

            # print("Weight Routine")
            # If full body, get 6 exercises and assign reps
            if target == "full":

                # print("Full Body Weight Routine")
                routine = makeFullBodyRoutine(genData, repRanges)

                # print("Successfully generated routine")
                self.setRoutine(routine)

                # Set as routine
                # print("Successfully set routine\n")

            else:

                # Make routine
                routine = makeWeightRoutine(genData, target, repRanges,
                                            allParts)

                # print("Successfully generated routine")
                self.setRoutine(routine)
                # Set as routine
                # print("Successfully set routine\n")

    # Format warmup & routine as dataframe and assign appropriate sets
    def formatFullRoutine(self):
        """
        Requires routine & warmup to be generated. Returns 2 dataframes,
        in a list, one created from the warmup and one from the routine, both
        will contain all exercises, the contents of a set & the number of sets
        per exercise.
        """

        # print("Format routine into dataframes")
        # Get routine and warmup
        routine = self.getRoutine()
        # print("Got routine")
        warmup = self.getWarmup()
        # print("Got warmup")

        # Ensure routine &/| warmup exists
        # print("Check for empty attributes")
        if {} in [routine, warmup]:

            raise ValueError("""
                             Routine & warmup must not be empty: generate
                             using generateWarmup() or generateRoutine()."""
                             )

        # Convert dicts into DataFrames
        # print("Covert to initial dataframes")
        warmupDF = pd.DataFrame.from_dict(warmup, orient="index")
        routineDF = pd.DataFrame.from_dict(routine, orient="index")

        # Add rest row
        # print("Create warmup rests")
        rests = pd.DataFrame.from_dict({
            "Rest": ["15 seconds", "30 seconds", "45 seconds"]
            }, orient="index")

        # Also add index col as exercise list
        # print("Add to warmup dataframe")
        warmupDF = warmupDF.append(rests).reset_index(drop=False)

        # Change column names of warmup
        # print("Fix column names")
        warmupDF = warmupDF.rename(index=str, columns={
            0: "Circuit 1",
            1: "Circuit 2",
            2: "Circuit 3",
            "index": "Exercise"
            })

        # Make set -> reps map dict
        # print("Created setmap")
        setMap = {
            # Weight options
            "5": 5,
            "3-5": 5,
            "8-12": 3,
            "10-15": 4,
            "12-15": 4,

            # Cardio options
            "8 mins": 1,
            "15 seconds":  4,
            "10 seconds": 3,
            "5 mins": 2,
            "30 seconds": 2
            }

        # Get set counts
        # print("Create sets and retrieve values")
        setCount = routineDF.iloc[:, 0].apply(lambda reps: setMap[reps])

        # Add set numbers to routine
        # print("Insert into dataframe")
        routineDF.insert(0, "Sets", setCount, allow_duplicates=True)

        # Add exercises as column from index
        # print("Reset dataframe indicies")
        routineDF = routineDF.reset_index(drop=False)

        # Fix column names
        # print("Rename columns")
        routineDF = routineDF.rename(index=str, columns={
            "index": "Exercise",
            0: "Reps"})

        # return lists of 2 DFs
        # print("Finish & Return")
        return [warmupDF, routineDF]


def returnWorkout(data, goal, groupOrCardio, gear):
    """
    Returns a workout class object from inputed args from user
    """
    # Go through every column and filter out all the data we need per the
    # user inputs

    # Initialise reference dicts for body parts and for goals
    bodyDict = {
        "chest": ["Pec Major", "Pec Minor"],
        "shoulders": ["Rear Delt", "Mid Delt", "Front Delt"],
        "back": ["Upper Back", "Mid Back", "Lower Back", "Lats", "Traps"],
        "legs": ["Quads", "Hamstrings", "Calves"],
        "arms": ["Biceps", "Triceps"],
        "core": ["Core", "Obliques"],
        "full": ["Full Body"]
    }

    allRanges = {
        "low": ["3-5"],
        "mix": ["5", "8-12", "10-15"],
        "high": ["12-15"],

        "cardio": {
            "regular": ["8 mins"],
            "hiit": ["15 seconds"],
            "both": {
                "Plyo": "10 seconds",
                "Cardio": "5 mins"
            }
        }
    }

    # Initially filter down by gear

    if gear == "gymless":

        data = filterExercises(data, ["GymLevel"], [["Gymless"]])

    elif gear == "basic":

        data = filterExercises(data, ["GymLevel"],
                               [["None", "Gymless", "Basic"]])

    # Get repRanges for the specified goal
    repRanges = allRanges[goal]

    # Cardio process is different so check the goal input
    if goal == "cardio":

        # Check the cardio value for rep range
        repRanges = repRanges[groupOrCardio]

        # Assign body parts variable (For object) to None
        allParts = None

        # Filter for cardio exercises only

        data = filterExercises(data, ["ExerciseType"], [["Cardio", "Plyo"]])

    else:

        # Get full body exercise for warmup
        fullBody = filterExercises(data, ["MuscleGroup"],
                                   [["Full"]])
        # Filter data for body part
        data = filterExercises(data, ["MuscleGroup"],
                               [[groupOrCardio.capitalize()]])

        # Drop deadlift
        fullBody.drop(fullBody[fullBody.MainLift == "Yes"].index)

        # Append together
        data = data.append(fullBody, ignore_index=True)

        # All parts assigned from bodyDict
        allParts = bodyDict[groupOrCardio]

    # Finalise Workout object args
    target = groupOrCardio

    workoutObj = Workout(data, target, allParts, repRanges, gear)

    return workoutObj